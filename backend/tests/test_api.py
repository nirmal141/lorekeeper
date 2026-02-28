import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.core.models import SimulationResult, WorldEvent


@pytest.fixture
def client(tmp_path):
    os.environ["GEMINI_API_KEY"] = "fake-key"
    os.environ["DB_PATH"] = str(tmp_path / "test.db")
    os.environ["INDEX_DIR"] = str(tmp_path / "indexes")

    with patch("backend.main.Client") as mock_client_cls, \
         patch("backend.services.npc_service.genai") as mock_genai, \
         patch("backend.services.npc_service.GeminiEmbedding"):
        mock_genai.Client.return_value = MagicMock()
        mock_temporal = AsyncMock()
        mock_client_cls.connect = AsyncMock(return_value=mock_temporal)

        from llama_index.core.embeddings import MockEmbedding
        import backend.main as main_mod
        main_mod.npc_service = main_mod.NPCService(main_mod.settings, embed_model=MockEmbedding(embed_dim=8))

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

    @patch("backend.services.npc_service.NPCService.chat")
    def test_chat_success(self, mock_chat, client):
        from backend.core.models import ChatResponse
        mock_chat.return_value = ChatResponse(
            npc_id="aldric", npc_dialogue="Welcome!", memories_retrieved=[]
        )
        c, _ = client
        resp = c.post("/npc/aldric/chat", json={"player_message": "Hello"})
        assert resp.status_code == 200
        assert resp.json()["npc_dialogue"] == "Welcome!"


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
