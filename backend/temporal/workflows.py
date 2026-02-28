import json
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow

with workflow.unsafe.imports_passed_through():
    from backend.core.config import Settings
    from backend.core.models import NPC, SimulationResult, WorldEvent, WorldState


@dataclass
class SimulateInput:
    world_state_json: str
    npcs_json: str
    settings_json: str


@dataclass
class UpdateNPCInput:
    npc_id: str
    event_json: str
    settings_json: str


@activity.defn
async def generate_world_event_activity(input: SimulateInput) -> str:
    from backend.services.world_service import WorldService

    settings = Settings(**json.loads(input.settings_json))
    world_state = WorldState(**json.loads(input.world_state_json))
    npcs = [NPC(**n) for n in json.loads(input.npcs_json)]

    service = WorldService(settings)
    result = service.generate_world_event(world_state, npcs)
    return result.model_dump_json()


@activity.defn
async def update_npc_memory_activity(input: UpdateNPCInput) -> None:
    from backend.services.npc_service import NPCService

    settings = Settings(**json.loads(input.settings_json))
    event = WorldEvent(**json.loads(input.event_json))

    service = NPCService(settings)
    service.add_world_event_to_npc(input.npc_id, event)


@workflow.defn
class WorldSimulationWorkflow:
    @workflow.run
    async def run(self, input: SimulateInput) -> str:
        result_json = await workflow.execute_activity(
            generate_world_event_activity,
            input,
            start_to_close_timeout=timedelta(seconds=30),
        )

        result = SimulationResult(**json.loads(result_json))
        settings_json = input.settings_json

        for npc_id in result.event.affected_npc_ids:
            await workflow.execute_activity(
                update_npc_memory_activity,
                UpdateNPCInput(
                    npc_id=npc_id,
                    event_json=result.event.model_dump_json(),
                    settings_json=settings_json,
                ),
                start_to_close_timeout=timedelta(seconds=15),
            )

        return result_json
