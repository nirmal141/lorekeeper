import json

from google import genai

from backend.core.config import Settings
from backend.core.models import NPC, GossipItem, NarrativeRecap, SimulationResult, WorldEvent, WorldState


class WorldService:
    def __init__(self, settings: Settings):
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return text

    def generate_world_event(self, world_state: WorldState, npcs: list[NPC]) -> SimulationResult:
        npc_descriptions = "\n".join(
            f"- {n.personality.name} (id={n.id}, {n.personality.role}): mood={n.current_mood}, goals={', '.join(n.personality.goals)}"
            for n in npcs
        )
        npc_ids = [n.id for n in npcs]

        prompt = f"""You are a game world simulator. Time is passing in a fantasy trading post world.

CURRENT WORLD STATE: {world_state.description}

RECENT EVENTS: {', '.join(world_state.recent_events) if world_state.recent_events else 'Nothing notable.'}

HOURS PASSED SO FAR: {world_state.hours_passed}

NPCs IN THE WORLD:
{npc_descriptions}

Generate ONE new world event AND gossip between NPCs. The event should:
1. Be dramatic but grounded (bandits, weather, trade disputes, mysterious strangers)
2. Directly affect at least one NPC
3. Change the world state in a meaningful way

Also generate 1-2 pieces of gossip — things NPCs told each other about recent events or about the player.

Respond in this EXACT JSON format (no markdown, no code blocks):
{{"event_description": "What happened in 2-3 sentences", "affected_npc_ids": ["npc_id1"], "npc_reactions": {{"npc_id1": "How this NPC reacted in 2-3 sentences"}}, "gossip": [{{"from_npc": "npc_id1", "to_npc": "npc_id2", "content": "What they told the other NPC"}}]}}

Only use these NPC IDs: {npc_ids}"""

        response = self._client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        data = json.loads(self._clean_json(response.text))

        event = WorldEvent(
            description=data["event_description"],
            affected_npc_ids=data["affected_npc_ids"],
        )

        gossip = [
            GossipItem(from_npc=g["from_npc"], to_npc=g["to_npc"], content=g["content"])
            for g in data.get("gossip", [])
            if g.get("from_npc") in npc_ids and g.get("to_npc") in npc_ids
        ]

        return SimulationResult(
            event=event,
            npc_reactions=data.get("npc_reactions", {}),
            gossip=gossip,
        )

    def generate_recap(self, world_state: WorldState, npcs: list[NPC]) -> NarrativeRecap:
        if not world_state.recent_events:
            return NarrativeRecap(summary="The trading post is quiet. Your story is just beginning.", key_moments=[])

        npc_status = ", ".join(f"{n.personality.name} ({n.current_mood})" for n in npcs)
        events_text = "\n".join(f"- {e}" for e in world_state.recent_events[:5])

        prompt = f"""You are a narrator for a fantasy RPG. Write a dramatic "Previously on..." recap.

WORLD: {world_state.description}
HOURS PASSED: {world_state.hours_passed}
NPC STATUS: {npc_status}

RECENT EVENTS:
{events_text}

Write a recap in this EXACT JSON format (no markdown, no code blocks):
{{"summary": "A dramatic 3-4 sentence narrative recap of what has happened so far, written like a TV show narrator", "key_moments": ["moment 1 in one sentence", "moment 2 in one sentence", "moment 3 in one sentence"]}}"""

        response = self._client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        data = json.loads(self._clean_json(response.text))

        return NarrativeRecap(
            summary=data["summary"],
            key_moments=data.get("key_moments", []),
        )
