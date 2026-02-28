# Lorekeeper — Technical Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     React Frontend                            │
│          TypeScript + RetroUI + Motion + Typewriter            │
│                                                               │
│  IntroScreen → ScenarioSelect → GameWorld → DialogueBox       │
│                                      ↕                        │
│                              CinematicOverlay                 │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTP (REST)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                             │
│                                                               │
│  ┌────────────┐   ┌──────────────┐   ┌─────────────────┐    │
│  │  Gemini    │   │  LlamaIndex  │   │    Temporal      │    │
│  │ 2.5 Flash  │   │  Per-NPC     │   │   Durable       │    │
│  │            │   │  Vector      │   │   Workflows      │    │
│  │ Dialogue   │   │  Memory      │   │                  │    │
│  │ World Sim  │   │  Indexes     │   │ Event Gen        │    │
│  │ Choices    │   │              │   │ Memory Update    │    │
│  │ Recap      │   │ Semantic     │   │ Gossip Spread   │    │
│  │ Gossip     │   │ Retrieval    │   │                  │    │
│  └────────────┘   └──────────────┘   └─────────────────┘    │
│                                                               │
│                  SQLite (per scenario)                         │
└──────────────────────────────────────────────────────────────┘
```

---

## How Gemini Works in Lorekeeper

We use **Gemini 2.5 Flash** for four distinct generation tasks:

### 1. NPC Dialogue Generation

When the player chats with an NPC, Gemini receives a structured prompt containing:

```
PERSONALITY: Name, role, backstory, goals
MOOD: Current emotional state (neutral, affected, worried...)
WORLD STATE: What's happening in the world right now
RECENT EVENTS: What events have occurred recently
MEMORIES: Top 5 semantically relevant memories from this NPC's history

PLAYER MESSAGE: What the player just said

INSTRUCTION: Respond in character. Return JSON with dialogue + 3 choice suggestions.
```

Gemini returns structured JSON:
```json
{
  "dialogue": "The NPC's in-character response",
  "choices": [
    "Suggested player response 1",
    "Suggested player response 2",
    "Suggested player response 3"
  ]
}
```

The **choices** are RPG-style conversation options that drive the story forward. Players can click one or type freely.

### 2. World Event Simulation

When "Pass Time" is triggered, Gemini simulates what happens next:

```
WORLD STATE: Current description + recent events + hours passed
ALL NPCs: Name, role, mood, goals for every NPC

INSTRUCTION: Generate one dramatic world event + NPC reactions + gossip between NPCs.
```

Returns:
```json
{
  "event_description": "Bandits raided the trading post...",
  "affected_npc_ids": ["aldric"],
  "npc_reactions": {
    "aldric": "Aldric is shaken. His storage shed was ransacked..."
  },
  "gossip": [
    {
      "from_npc": "aldric",
      "to_npc": "mira",
      "content": "Aldric told Mira about a stranger asking about dragons"
    }
  ]
}
```

### 3. Narrative Recap

Before showing the new event, Gemini generates a "Previously on..." recap:

```
WORLD STATE + NPC MOODS + RECENT EVENTS

INSTRUCTION: Write a dramatic TV-narrator-style recap of the story so far.
```

Returns a narrative summary and key moments — shown with typewriter animation in the cinematic overlay.

### 4. Gossip Generation

Gossip is generated as part of the world simulation (not a separate call). Gemini decides which NPCs would logically share information based on:
- What events just happened
- What NPCs know about the player
- NPC relationships and proximity

---

## How LlamaIndex Works in Lorekeeper

LlamaIndex provides **per-NPC episodic memory** using vector embeddings.

### Architecture

```
data/indexes/
├── ashwood/           ← Scenario isolation
│   ├── aldric/        ← One vector index per NPC
│   │   ├── docstore.json
│   │   ├── default__vector_store.json
│   │   └── index_store.json
│   └── mira/
│       ├── docstore.json
│       ├── default__vector_store.json
│       └── index_store.json
├── starfall/
│   ├── reyes/
│   └── lian/
└── ...
```

### Memory Types

Each memory is stored as a `Document` with metadata:

| Type | When Created | Example |
|------|-------------|---------|
| `player_interaction` | After every chat | `"Player said: 'I need a blade'. I responded: 'Show me you're serious.'"` |
| `world_event` | After simulation | `"World event: Bandits raided the storage shed."` |
| `npc_gossip` | After simulation | `"Gossip from aldric: Aldric told Mira about a stranger asking about dragons"` |

### Retrieval Flow

When the player says something to an NPC:

1. **Query**: The player's message becomes the search query
2. **Embedding**: Gemini Embedding model (`gemini-embedding-001`) converts the query to a vector
3. **Similarity Search**: LlamaIndex finds the top 5 most similar memories from that NPC's index
4. **Context Injection**: Retrieved memories are injected into the Gemini prompt
5. **Response**: Gemini generates dialogue that naturally references relevant memories

**Key insight**: This is **semantic** retrieval, not keyword matching. Asking "do you remember the dragon?" retrieves a memory about "heading north to hunt the beast" because the meanings are similar — even if the exact words are different.

### Persistence

Indexes are persisted to disk after every write. On server restart, indexes are loaded from disk. Memories survive across sessions indefinitely.

---

## How Temporal Works in Lorekeeper

Temporal provides **durable workflow orchestration** for world simulation.

### Why Temporal?

World simulation is a multi-step pipeline:
1. Generate a world event (Gemini API call — can fail, timeout, rate limit)
2. Store the event in each affected NPC's memory (LlamaIndex writes)
3. Distribute gossip to receiving NPCs (more LlamaIndex writes)

If step 1 succeeds but step 2 fails (server crash, network error), you need step 2 to retry **without re-running step 1**. That's exactly what Temporal's durable execution model provides.

### Workflow Architecture

```
WorldSimulationWorkflow
│
├── Activity 1: generate_world_event_activity (30s timeout)
│   └── Calls Gemini → returns SimulationResult (event + reactions + gossip)
│
├── Activity 2: update_npc_memory_activity (15s timeout) × N affected NPCs
│   └── Stores world event in each affected NPC's LlamaIndex memory
│
└── Activity 3: update_npc_gossip_activity (15s timeout) × N gossip items
    └── Stores gossip in each receiving NPC's LlamaIndex memory
```

### Execution Guarantees

| Scenario | What Happens |
|----------|-------------|
| Server crashes after event generation | Temporal retries only the memory update activities |
| Gemini API times out | Temporal retries event generation with backoff |
| One NPC memory write fails | Only that specific NPC's update is retried |
| Server restarts completely | Temporal resumes the workflow from the last completed activity |
| Network partition during gossip | Gossip activities are retried independently |

### Infrastructure

- **Temporal Server**: Runs locally via `temporal server start-dev` (includes Web UI at port 8233)
- **Task Queue**: `lorekeeper` — all activities registered on this queue
- **Worker**: Separate Python process (`python -m backend.temporal.worker`) that polls the queue
- **Visibility**: All workflow executions visible in Temporal Web UI with full activity history

---

## The Coordination: How All Three Work Together

### Chat Flow (Player talks to NPC)

```
Player Message
    │
    ▼
[LlamaIndex] Query NPC's memory index for relevant memories (top 5)
    │
    ▼
[Gemini 2.5 Flash] Generate dialogue with:
    - NPC personality + mood
    - Retrieved memories
    - World state + recent events
    - Player message
    │
    ▼
[LlamaIndex] Store new interaction as memory
    │
    ▼
Response with dialogue + 3 choices
```

### Simulation Flow (Pass Time)

```
Player clicks "Pass Time"
    │
    ▼
[Temporal] Start WorldSimulationWorkflow
    │
    ├──▶ [Gemini] Generate world event + NPC reactions + gossip
    │
    ├──▶ [LlamaIndex] Store event in each affected NPC's memory
    │
    └──▶ [LlamaIndex] Store gossip in each receiving NPC's memory
    │
    ▼
[Gemini] Generate "Previously on..." narrative recap
    │
    ▼
Frontend shows three-phase cinematic overlay:
    1. "Previously on Lorekeeper..." (recap)
    2. "While you were away..." (new event + reactions)
    3. "Meanwhile, whispers spread..." (gossip)
```

### Cross-Session Memory Flow

```
Session 1: Player tells Aldric about the dragon
    └── [LlamaIndex] Stores in Aldric's memory

Pass Time: World simulation runs
    ├── [Gemini] Generates event: bandits raid
    ├── [LlamaIndex] Stores raid in Aldric's memory
    ├── [Gemini] Generates gossip: Aldric tells Mira about dragon hunter
    └── [LlamaIndex] Stores gossip in Mira's memory

Session 2: Player talks to Mira about dragons
    ├── [LlamaIndex] Retrieves gossip memory: "Aldric mentioned a dragon hunter"
    ├── [LlamaIndex] Retrieves raid memory: "Bandits attacked the post"
    └── [Gemini] Generates response weaving both memories naturally
```

### Per-Scenario Isolation

```
Scenario: ashwood
    ├── Database: data/ashwood.db (world state, events, NPC moods)
    └── Memory:   data/indexes/ashwood/{npc_id}/ (LlamaIndex vectors)

Scenario: starfall
    ├── Database: data/starfall.db (completely separate)
    └── Memory:   data/indexes/starfall/{npc_id}/ (completely separate)
```

Switching scenarios changes which database and index directory the backend reads from. No data bleeds between worlds.

---

## Tech Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **LLM** | Gemini 2.5 Flash | Latest | Dialogue, world sim, recap, choices |
| **Embeddings** | Gemini Embedding | gemini-embedding-001 | Vector embeddings for memory retrieval |
| **Memory** | LlamaIndex | 0.14.x | Per-NPC vector stores with semantic search |
| **Orchestration** | Temporal | 1.23.x | Durable world simulation workflows |
| **API** | FastAPI | 0.134.x | REST endpoints with Pydantic validation |
| **Database** | SQLite | Built-in | World state, events, NPC data |
| **Frontend** | React + TypeScript | 19.x | Game interface |
| **UI Library** | pixel-retroui | Latest | Pixel-art styled components |
| **Animation** | Motion (Framer Motion) | Latest | Spring animations, transitions |
| **Typewriter** | react-simple-typewriter | Latest | Narrative text effects |
| **Validation** | Pydantic | 2.12.x | Strict type validation throughout |
| **Testing** | pytest | 9.x | 31 unit tests |
