import asyncio
from unittest.mock import MagicMock, patch

import pytest
from llama_index.core.embeddings import MockEmbedding

from backend.core.config import Settings
from backend.core.models import ChatRequest, NPC, NPCPersonality, WorldEvent, WorldState
from backend.services.npc_service import NPCService


@pytest.fixture
def settings(tmp_path):
    return Settings(
        gemini_api_key="fake-key",
        db_path=str(tmp_path / "test.db"),
        index_dir=str(tmp_path / "indexes"),
    )


@pytest.fixture
def npc():
    return NPC(
        id="aldric",
        personality=NPCPersonality(
            name="Aldric",
            role="merchant",
            backstory="Old trader",
            goals=["survive"],
        ),
    )


@pytest.fixture
def world_state():
    return WorldState(description="A quiet village")


@pytest.fixture
def mock_service(settings):
    with patch("backend.services.npc_service.genai") as mock_genai:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Welcome, traveler."
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        service = NPCService(settings, embed_model=MockEmbedding(embed_dim=8))
        yield service, mock_client


class TestNPCService:
    def test_chat_returns_response(self, mock_service, npc, world_state):
        service, mock_client = mock_service
        result = asyncio.run(service.chat(npc, world_state, ChatRequest(player_message="Hello")))

        assert result.npc_id == "aldric"
        assert result.npc_dialogue == "Welcome, traveler."
        assert isinstance(result.memories_retrieved, list)
        mock_client.models.generate_content.assert_called_once()

    def test_chat_prompt_includes_context(self, mock_service, npc, world_state):
        service, mock_client = mock_service
        asyncio.run(service.chat(npc, world_state, ChatRequest(player_message="Tell me about the dragon")))

        call_kwargs = mock_client.models.generate_content.call_args[1]
        assert "Tell me about the dragon" in call_kwargs["contents"]
        assert "Aldric" in call_kwargs["contents"]
        assert "merchant" in call_kwargs["contents"]

    def test_memory_persists_across_chats(self, mock_service, npc, world_state):
        service, _ = mock_service
        asyncio.run(service.chat(npc, world_state, ChatRequest(player_message="I am looking for the dragon")))
        result = asyncio.run(service.chat(npc, world_state, ChatRequest(player_message="Do you remember me?")))

        assert len(result.memories_retrieved) > 0

    def test_add_world_event(self, mock_service):
        service, _ = mock_service
        event = WorldEvent(description="Bandits raided the market", affected_npc_ids=["aldric"])
        service.add_world_event_to_npc("aldric", event)

        memories = service._retrieve_memories("aldric", "bandits")
        assert len(memories) > 0
        assert any("Bandits" in m for m in memories)
