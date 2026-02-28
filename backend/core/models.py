from datetime import datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class NPCPersonality(BaseModel):
    name: str
    role: str
    backstory: str
    goals: list[str]


class NPC(BaseModel):
    id: str
    personality: NPCPersonality
    current_mood: str = "neutral"


class Memory(BaseModel):
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    memory_type: Literal["player_interaction", "world_event", "npc_gossip"]


class WorldState(BaseModel):
    description: str
    recent_events: list[str] = []
    hours_passed: int = 0


class WorldEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    affected_npc_ids: list[str]


class ChatRequest(BaseModel):
    player_message: str


class ChatResponse(BaseModel):
    npc_id: str
    npc_dialogue: str
    memories_retrieved: list[str]
    choices: list[str] = []


class GossipItem(BaseModel):
    from_npc: str
    to_npc: str
    content: str


class SimulationResult(BaseModel):
    event: WorldEvent
    npc_reactions: dict[str, str]
    gossip: list[GossipItem] = []


class NarrativeRecap(BaseModel):
    summary: str
    key_moments: list[str] = []


class ScenarioSummary(BaseModel):
    id: str
    name: str
    genre: str
    tagline: str
