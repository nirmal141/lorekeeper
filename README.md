# Lorekeeper

**A game world that doesn't stop when you leave.**

NPCs remember everything you've ever said. The world simulates itself while you're offline. When you return, the NPCs weave your personal history with world events into one coherent response.

Built for the Cerebral Valley Hackathon — **Gemini and Gaming** track.

---

## The Problem

Every game world freezes when you log off. NPCs stand in place. Nothing changes. Talk to an NPC 100 times and they greet you like a stranger every time.

Lorekeeper solves three things no current game does well together:

1. **NPCs with genuine episodic memory** — Tell an NPC you're hunting a dragon. Come back 3 sessions later and they'll ask if you found it.
2. **Persistent world simulation** — Hit "Pass Time" and the world keeps going. Bandits raid, storms hit, trade disputes escalate — all without you.
3. **NPCs react to events they witnessed** — When bandits raid a merchant's shop, that merchant remembers it and brings it up in conversation.

## Demo Flow

```
1. Enter the world → meet NPCs at a trading post
2. Talk to Mira the blacksmith → "I need a blade for the dragon hunt"
3. She remembers → challenges you to prove your worth
4. Hit "Pass Time" → Temporal simulates a bandit raid overnight
5. Talk to Mira again → she references BOTH your blade request AND the raid
```

The NPC weaves your personal history with world events naturally. That's the magic.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│         React + TypeScript + RetroUI + Motion           │
│                  Pixel RPG aesthetic                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Gemini    │  │  LlamaIndex  │  │   Temporal     │  │
│  │  2.5 Flash  │  │  Vector RAG  │  │  Workflows     │  │
│  │             │  │              │  │               │  │
│  │ NPC dialogue│  │ Per-NPC      │  │ World sim     │  │
│  │ World sim   │  │ episodic     │  │ runs as       │  │
│  │ generation  │  │ memory index │  │ durable       │  │
│  │             │  │              │  │ workflow      │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
│                    SQLite + Pydantic                     │
└─────────────────────────────────────────────────────────┘
```

### Why Each Tool Fits

| Tool | Role | Why it's not forced |
|------|------|-------------------|
| **Gemini 2.5 Flash** | Generates NPC dialogue + world events | Long context fits full NPC history in one prompt |
| **LlamaIndex** | Per-NPC vector memory index | Semantic retrieval — "remember the dragon?" finds the right memory even after 50 other conversations |
| **Temporal** | Runs world simulation as durable workflow | If the server crashes mid-simulation, Temporal picks up exactly where it left off |

## Project Structure

```
lorekeeper/
├── backend/
│   ├── .env                    # Gemini API key
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app + routes
│   ├── core/                   # Models, config, database, seed
│   ├── services/               # NPC service (Gemini + LlamaIndex)
│   │                           # World service (Gemini world sim)
│   ├── temporal/               # Workflow definitions + worker
│   └── tests/                  # 30 tests, all passing
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Intro → Game World router
│   │   ├── api.ts              # Backend API client
│   │   └── components/
│   │       ├── IntroScreen     # Typewriter narrative intro
│   │       ├── GameWorld       # NPC selection + world sidebar
│   │       ├── DialogueBox     # RPG-style dialogue with memory cards
│   │       ├── CinematicOverlay # "While you were away..." reveal
│   │       ├── HowItWorks     # Architecture diagram for judges
│   │       └── ...
├── start.sh                    # Start all services
└── stop.sh                     # Stop all services
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Temporal CLI](https://docs.temporal.io/cli#install)
- [Gemini API key](https://aistudio.google.com/apikey) (free tier)

### Install

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install google-genai

# Frontend
cd ../frontend
npm install

# Environment
cp ../.env.example ../backend/.env
# Edit backend/.env and add your GEMINI_API_KEY
```

### Run

```bash
# From project root — starts everything
./start.sh

# Or manually in 4 terminals:
temporal server start-dev                                          # Terminal 1
source backend/venv/bin/activate && python -m backend.temporal.worker  # Terminal 2
source backend/venv/bin/activate && uvicorn backend.main:app --reload --port 8000  # Terminal 3
cd frontend && npm run dev                                         # Terminal 4
```

Open **http://localhost:5173**

### Test

```bash
source backend/venv/bin/activate
python -m pytest backend/tests/ -v    # 30 tests
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/world` | Current world state |
| `GET` | `/npcs` | List all NPCs |
| `GET` | `/npc/{id}` | Single NPC with mood |
| `POST` | `/npc/{id}/chat` | Chat with NPC (memory read + write + Gemini) |
| `POST` | `/world/simulate` | Trigger world simulation via Temporal |
| `GET` | `/world/events` | Recent world events |

## Tech Stack

- **Backend:** FastAPI, Pydantic, SQLite
- **AI:** Google Gemini 2.5 Flash, LlamaIndex (vector embeddings + RAG)
- **Orchestration:** Temporal (durable workflow engine)
- **Frontend:** React, TypeScript, RetroUI (pixel-art components), Motion (animations)
- **Testing:** pytest, 30 unit tests

## License

MIT
