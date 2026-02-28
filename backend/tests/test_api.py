import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.core.models import SimulationResult, WorldEvent


@pytest.fixture
def client(tmp_path):
    os.environ["GEMINI_API_KEY"] = "fake-key"

    from backend.core.config import Settings
    test_settings = Settings(
        gemini_api_key="fake-key",
        db_path=str(tmp_path / "test.db"),
        index_dir=str(tmp_path / "indexes"),
    )

    def mock_scoped():
        return test_settings

    with patch("backend.main.Client") as mock_client_cls, \
         patch("backend.services.npc_service.genai") as mock_genai, \
         patch("backend.services.npc_service.GeminiEmbedding"), \
         patch("backend.main._scoped", mock_scoped), \
         patch("backend.main.seed_all"):
        mock_genai.Client.return_value = MagicMock()
        mock_temporal = AsyncMock()
        mock_client_cls.connect = AsyncMock(return_value=mock_temporal)

        # Seed the test DB manually
        from backend.core.database import get_db, init_db
        from backend.core.seed import seed_scenario
        conn = get_db(test_settings)
        init_db(conn)
        conn.execute(
            "INSERT OR IGNORE INTO world_state (id, description, hours_passed) VALUES (1, 'Test world', 0)"
        )
        import json as j
        conn.execute(
            "INSERT OR IGNORE INTO npcs (id, name, role, backstory, goals, current_mood) VALUES (?, ?, ?, ?, ?, ?)",
            ("aldric", "Aldric", "merchant", "Old trader", j.dumps(["survive"]), "neutral"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO npcs (id, name, role, backstory, goals, current_mood) VALUES (?, ?, ?, ?, ?, ?)",
            ("mira", "Mira", "blacksmith", "Strong smith", j.dumps(["forge"]), "neutral"),
        )
        conn.commit()
        conn.close()

        from backend.main import app
        with TestClient(app) as c:
            yield c, mock_temporal


class TestWorldEndpoints:
    def test_get_world(self, client):
        c, _ = client
        resp = c.get("/world")
        assert resp.status_code == 200
        data = resp.json()
        assert "description" in data
        assert "hours_passed" in data

    def test_get_events_empty(self, client):
        c, _ = client
        resp = c.get("/world/events")
        assert resp.status_code == 200
        assert resp.json() == []


class TestNPCEndpoints:
    def test_list_npcs(self, client):
        c, _ = client
        resp = c.get("/npcs")
        assert resp.status_code == 200
        npcs = resp.json()
        assert len(npcs) == 2
        ids = {n["id"] for n in npcs}
        assert "aldric" in ids
        assert "mira" in ids

    def test_get_single_npc(self, client):
        c, _ = client
        resp = c.get("/npc/aldric")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "aldric"
        assert data["current_mood"] == "neutral"

    def test_get_single_npc_not_found(self, client):
        c, _ = client
        resp = c.get("/npc/nobody")
        assert resp.status_code == 404

    def test_chat_not_found(self, client):
        c, _ = client
        resp = c.post("/npc/nobody/chat", json={"player_message": "Hello"})
        assert resp.status_code == 404

    def test_chat_success(self, client):
        from backend.core.models import ChatResponse
        mock_response = ChatResponse(
            npc_id="aldric", npc_dialogue="Welcome!", memories_retrieved=[]
        )
        with patch("backend.main._npc_service") as mock_fn:
            mock_svc = MagicMock()
            mock_svc.chat = AsyncMock(return_value=mock_response)
            mock_fn.return_value = mock_svc
            c, _ = client
            resp = c.post("/npc/aldric/chat", json={"player_message": "Hello"})
            assert resp.status_code == 200
            assert resp.json()["npc_dialogue"] == "Welcome!"


class TestScenarios:
    def test_list_scenarios(self, client):
        c, _ = client
        resp = c.get("/scenarios")
        assert resp.status_code == 200
        scenarios = resp.json()
        assert len(scenarios) == 5
        ids = {s["id"] for s in scenarios}
        assert "ashwood" in ids
        assert "starfall" in ids
        assert "dusty-gulch" in ids
        assert "holloway" in ids
        assert "byte-brew" in ids


class TestSimulate:
    def test_simulate_triggers_temporal(self, client):
        c, mock_temporal = client
        event = WorldEvent(description="Storm hit", affected_npc_ids=["aldric"])
        result = SimulationResult(event=event, npc_reactions={"aldric": "worried"})
        mock_temporal.execute_workflow = AsyncMock(return_value=result.model_dump_json())

        resp = c.post("/world/simulate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["event"]["description"] == "Storm hit"
        assert "aldric" in data["npc_reactions"]
