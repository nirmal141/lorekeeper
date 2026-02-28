const BASE = "http://localhost:8000";

export interface NPCPersonality {
  name: string;
  role: string;
  backstory: string;
  goals: string[];
}

export interface NPC {
  id: string;
  personality: NPCPersonality;
  current_mood: string;
}

export interface WorldState {
  description: string;
  recent_events: string[];
  hours_passed: number;
}

export interface ChatResponse {
  npc_id: string;
  npc_dialogue: string;
  memories_retrieved: string[];
}

export interface WorldEvent {
  id: string;
  description: string;
  timestamp: string;
  affected_npc_ids: string[];
}

export interface SimulationResult {
  event: WorldEvent;
  npc_reactions: Record<string, string>;
}

export async function getWorld(): Promise<WorldState> {
  const res = await fetch(`${BASE}/world`);
  return res.json();
}

export async function getNPCs(): Promise<NPC[]> {
  const res = await fetch(`${BASE}/npcs`);
  return res.json();
}

export async function chatWithNPC(
  npcId: string,
  message: string
): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/npc/${npcId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_message: message }),
  });
  return res.json();
}

export async function simulateWorld(): Promise<SimulationResult> {
  const res = await fetch(`${BASE}/world/simulate`, { method: "POST" });
  return res.json();
}

export async function getEvents(): Promise<WorldEvent[]> {
  const res = await fetch(`${BASE}/world/events`);
  return res.json();
}

export async function getNPC(npcId: string): Promise<NPC> {
  const res = await fetch(`${BASE}/npc/${npcId}`);
  return res.json();
}
