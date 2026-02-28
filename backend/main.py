import json
import shutil
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from temporalio.client import Client

from backend.core.config import Settings
from backend.core.database import get_db, get_npc, get_npcs, get_world_state, init_db, save_world_event, update_npc_mood
from backend.core.models import ChatRequest, ChatResponse, NarrativeRecap, NPC, ScenarioSummary, SimulationResult, WorldEvent, WorldState
from backend.core.scenarios import SCENARIOS
from backend.core.seed import seed_all
from backend.services.npc_service import NPCService
from backend.services.world_service import WorldService
from backend.temporal.workflows import SimulateInput, WorldSimulationWorkflow

TASK_QUEUE = "lorekeeper"

settings = Settings()
active_scenario_id: str = "ashwood"


def _scoped() -> Settings:
    return settings.for_scenario(active_scenario_id)


def _npc_service() -> NPCService:
    return NPCService(_scoped())


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_all(settings)
    app.state.temporal_client = await Client.connect(settings.temporal_host)
    yield


app = FastAPI(title="Lorekeeper", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def health():
    return {"status": "healthy", "service": "Lorekeeper", "active_scenario": active_scenario_id}


@app.get("/scenarios", response_model=list[ScenarioSummary])
def list_scenarios():
    return [
        ScenarioSummary(id=s["id"], name=s["name"], genre=s["genre"], tagline=s["tagline"])
        for s in SCENARIOS
    ]


@app.post("/scenarios/{scenario_id}/activate")
def activate_scenario(scenario_id: str):
    global active_scenario_id
    scenario = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")

    active_scenario_id = scenario_id
    scoped = _scoped()
    conn = get_db(scoped)
    init_db(conn)

    if conn.execute("SELECT COUNT(*) FROM npcs").fetchone()[0] == 0:
        from backend.core.seed import seed_scenario
        seed_scenario(settings, scenario_id)

    conn.close()
    return {"status": "activated", "scenario": scenario_id}


@app.get("/world", response_model=WorldState)
def get_world():
    conn = get_db(_scoped())
    try:
        return get_world_state(conn)
    finally:
        conn.close()


@app.get("/npcs", response_model=list[NPC])
def list_npcs():
    conn = get_db(_scoped())
    try:
        return get_npcs(conn)
    finally:
        conn.close()


@app.get("/npc/{npc_id}", response_model=NPC)
def get_single_npc(npc_id: str):
    conn = get_db(_scoped())
    try:
        npc = get_npc(conn, npc_id)
        if not npc:
            raise HTTPException(status_code=404, detail=f"NPC '{npc_id}' not found")
        return npc
    finally:
        conn.close()


@app.post("/npc/{npc_id}/chat", response_model=ChatResponse)
async def chat_with_npc(npc_id: str, request: ChatRequest):
    scoped = _scoped()
    conn = get_db(scoped)
    try:
        npc = get_npc(conn, npc_id)
        if not npc:
            raise HTTPException(status_code=404, detail=f"NPC '{npc_id}' not found")
        world_state = get_world_state(conn)
    finally:
        conn.close()

    return await _npc_service().chat(npc, world_state, request)


@app.post("/world/simulate", response_model=SimulationResult)
async def simulate_world():
    scoped = _scoped()
    conn = get_db(scoped)
    try:
        world_state = get_world_state(conn)
        npcs = get_npcs(conn)
    finally:
        conn.close()

    client: Client = app.state.temporal_client
    result_json = await client.execute_workflow(
        WorldSimulationWorkflow.run,
        SimulateInput(
            world_state_json=world_state.model_dump_json(),
            npcs_json=json.dumps([n.model_dump() for n in npcs]),
            settings_json=scoped.model_dump_json(),
        ),
        id=f"simulate-{uuid4()}",
        task_queue=TASK_QUEUE,
    )

    result = SimulationResult.model_validate_json(result_json)

    conn = get_db(scoped)
    try:
        save_world_event(conn, result.event)
        for npc_id in result.npc_reactions:
            update_npc_mood(conn, npc_id, "affected")
    finally:
        conn.close()

    return result


@app.get("/world/events", response_model=list[WorldEvent])
def get_events():
    conn = get_db(_scoped())
    try:
        rows = conn.execute(
            "SELECT * FROM world_events ORDER BY timestamp DESC LIMIT 20"
        ).fetchall()
        return [
            WorldEvent(
                id=r["id"],
                description=r["description"],
                timestamp=r["timestamp"],
                affected_npc_ids=json.loads(r["affected_npc_ids"]),
            )
            for r in rows
        ]
    finally:
        conn.close()


@app.get("/world/recap", response_model=NarrativeRecap)
def get_recap():
    scoped = _scoped()
    conn = get_db(scoped)
    try:
        world_state = get_world_state(conn)
        npcs = get_npcs(conn)
    finally:
        conn.close()

    ws = WorldService(scoped)
    return ws.generate_recap(world_state, npcs)
