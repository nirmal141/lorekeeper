import json

from google import genai

from backend.core.config import Settings
from backend.core.models import NPC, SimulationResult, WorldEvent, WorldState


class WorldService:
    def __init__(self, settings: Settings):
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def generate_world_event(self, world_state: WorldState, npcs: list[NPC]) -> SimulationResult:
        npc_descriptions = "\n".join(
            f"- {n.personality.name} ({n.personality.role}): mood={n.current_mood}, goals={', '.join(n.personality.goals)}"
            for n in npcs
        )

        prompt = f"""You are a game world simulator. Time is passing in a fantasy trading post world.

CURRENT WORLD STATE: {world_state.description}

RECENT EVENTS: {', '.join(world_state.recent_events) if world_state.recent_events else 'Nothing notable.'}

HOURS PASSED SO FAR: {world_state.hours_passed}

NPCs IN THE WORLD:
{npc_descriptions}

Generate ONE new world event that happened while the player was away. The event should:
1. Be dramatic but grounded (bandits, weather, trade disputes, mysterious strangers)
2. Directly affect at least one NPC
3. Change the world state in a meaningful way

Respond in this EXACT JSON format (no markdown, no code blocks):
{{"event_description": "What happened in 2-3 sentences", "affected_npc_ids": ["npc_id1"], "npc_reactions": {{"npc_id1": "How this NPC was affected and what they think about it"}}}}

Only use these NPC IDs: {[n.id for n in npcs]}"""

        response = self._client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        data = json.loads(text)

        event = WorldEvent(
            description=data["event_description"],
            affected_npc_ids=data["affected_npc_ids"],
        )

        return SimulationResult(
            event=event,
            npc_reactions=data.get("npc_reactions", {}),
        )
