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
  choices: string[];
}

export interface WorldEvent {
  id: string;
  description: string;
  timestamp: string;
  affected_npc_ids: string[];
}

export interface GossipItem {
  from_npc: string;
  to_npc: string;
  content: string;
}

export interface SimulationResult {
  event: WorldEvent;
  npc_reactions: Record<string, string>;
  gossip: GossipItem[];
}

export interface NarrativeRecap {
  summary: string;
  key_moments: string[];
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

export async function getRecap(): Promise<NarrativeRecap> {
  const res = await fetch(`${BASE}/world/recap`);
  return res.json();
}

export interface ScenarioSummary {
  id: string;
  name: string;
  genre: string;
  tagline: string;
}

export async function getScenarios(): Promise<ScenarioSummary[]> {
  const res = await fetch(`${BASE}/scenarios`);
  return res.json();
}

export async function activateScenario(id: string): Promise<void> {
  await fetch(`${BASE}/scenarios/${id}/activate`, { method: "POST" });
}

export async function getStarters(): Promise<Record<string, string[]>> {
  const res = await fetch(`${BASE}/scenarios/active/starters`);
  return res.json();
}
