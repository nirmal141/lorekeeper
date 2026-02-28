from datetime import datetime

import pytest
from pydantic import ValidationError

from backend.core.models import (
    ChatRequest,
    ChatResponse,
    Memory,
    NPC,
    NPCPersonality,
    SimulationResult,
    WorldEvent,
    WorldState,
)


class TestNPCPersonality:
    def test_valid(self):
        p = NPCPersonality(name="Aldric", role="merchant", backstory="Old trader", goals=["survive"])
        assert p.name == "Aldric"
        assert p.goals == ["survive"]

    def test_missing_required(self):
        with pytest.raises(ValidationError):
            NPCPersonality(name="Aldric", role="merchant")


class TestNPC:
    def test_defaults(self):
        p = NPCPersonality(name="Aldric", role="merchant", backstory="Old trader", goals=["survive"])
        npc = NPC(id="aldric", personality=p)
        assert npc.current_mood == "neutral"


class TestMemory:
    def test_valid_types(self):
        m = Memory(content="Player said hello", memory_type="player_interaction")
        assert m.memory_type == "player_interaction"
        assert isinstance(m.timestamp, datetime)

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            Memory(content="test", memory_type="invalid")


class TestWorldEvent:
    def test_auto_fields(self):
        e = WorldEvent(description="Bandits attacked", affected_npc_ids=["aldric"])
        assert e.id
        assert isinstance(e.timestamp, datetime)


class TestWorldState:
    def test_defaults(self):
        ws = WorldState(description="A quiet village")
        assert ws.recent_events == []
        assert ws.hours_passed == 0


class TestChatRequest:
    def test_valid(self):
        r = ChatRequest(player_message="Hello there")
        assert r.player_message == "Hello there"


class TestChatResponse:
    def test_valid(self):
        r = ChatResponse(npc_id="aldric", npc_dialogue="Welcome", memories_retrieved=["met before"])
        assert r.memories_retrieved == ["met before"]


class TestSimulationResult:
    def test_valid(self):
        event = WorldEvent(description="Storm", affected_npc_ids=["aldric"])
        result = SimulationResult(event=event, npc_reactions={"aldric": "worried about stock"})
        assert result.npc_reactions["aldric"] == "worried about stock"
