# Lorekeeper — Demo Script for Judges

## The Pitch (30 seconds)

> "Every game world freezes when you leave. NPCs forget you. Nothing changes. We built **Lorekeeper** — a game engine where NPCs have genuine long-term memory, the world simulates itself while you're offline, and NPCs gossip about you behind your back. It works across any genre — fantasy, sci-fi, western, noir, modern — and every world is fully isolated with its own timeline and NPC relationships."

## Demo Flow (3-4 minutes)

### Act 1: The Setup (30 sec)

1. Open the app. Show the **intro screen** — typewriter text explains the concept.
2. Click **"Choose Your World"** — show the 5 scenario cards with pixel art images.
3. Say: *"Each of these worlds has its own database, its own NPC memories, its own timeline. They're fully isolated. Let me show you the fantasy one."*
4. Click **The Ashwood Post**.

### Act 2: Memory in Action (60 sec)

5. Click **Aldric** the merchant. Note the 3 starter choices — *"These are context-aware suggestions generated from the scenario."*
6. Click or type: **"I'm heading north to hunt the dragon. Do you have supplies?"**
7. Wait for response. Say: *"Aldric is responding in character — gruff, protective, suspicious of travelers. This is Gemini 2.5 Flash generating dialogue."*
8. Ask a follow-up: **"I promise I'll come back. Can you save me some rope?"**
9. Point out the **"memories recalled"** accordion — *"See this? LlamaIndex just retrieved his memory of our first exchange and wove it into the response. He remembers the dragon."*

### Act 3: The World Moves On (60 sec)

10. Click **← Back** to return to the world view.
11. Click **"Pass Time"** — *"Now Temporal runs a durable workflow. Gemini simulates what happens in the world while we're away."*
12. Watch the cinematic overlay:
    - **"Previously on Lorekeeper..."** — narrative recap
    - **"While you were away..."** — a world event unfolds (e.g., bandits raid)
    - **NPC reactions** — how Aldric and Mira were affected
    - **"Meanwhile, whispers spread..."** — gossip: *Aldric told Mira about a stranger asking about dragons*
13. Click **"Return to World"**

### Act 4: The Payoff (60 sec)

14. Now click **Blacksmith Mira**. Say: **"Have you heard about anyone hunting dragons around here?"**
15. **This is the wow moment.** Mira knows about the dragon — even though you never told her. Aldric gossiped. Point this out: *"I never mentioned dragons to Mira. But Aldric told her during the world simulation. The gossip was stored in her memory through LlamaIndex."*
16. Go back. Click **Aldric** again. Say: **"I'm back. What happened while I was gone?"**
17. He references BOTH the dragon conversation AND the bandit raid. *"He remembers our relationship AND what happened in the world independently. Two separate memory sources, one coherent response."*

### Act 5: The Architecture (30 sec)

18. Point to the **Architecture** panel in the sidebar:
    - **Gemini 2.5 Flash** — NPC dialogue + world event generation + narrative recap
    - **LlamaIndex** — per-NPC vector memory with semantic retrieval
    - **Temporal** — durable workflow orchestration for world simulation
19. Say: *"If the server crashes mid-simulation, Temporal picks up exactly where it left off. The memories persist across sessions. And every world is fully isolated."*

### Act 6: Genre Flexibility (15 sec)

20. Click **Worlds** in the top bar. Pick **Byte & Brew** (the startup scenario).
21. *"Same engine, completely different genre. A startup founder and a burned-out engineer. The world simulates investor meetings, product crashes, co-founder arguments."*
22. Show it loads different NPCs, different starters, different world state.

## Key Points to Emphasize

- **"Not a chatbot"** — NPCs have episodic memory that persists and is semantically retrieved
- **"Not scripted"** — every response is generated from personality + memory + world state
- **"The world doesn't need you"** — simulation runs independently via Temporal durable workflows
- **"NPCs have social lives"** — gossip propagates information between NPCs without player involvement
- **"Any genre"** — 5 completely different worlds prove the engine is genre-agnostic
- **"Crash-proof"** — Temporal guarantees simulation completes even if the server restarts

## Questions Judges Might Ask

**Q: How is this different from ChatGPT with memory?**
> ChatGPT remembers your chat history linearly. Lorekeeper does semantic retrieval — it finds the *relevant* memory, not the recent one. Ask about dragons after 50 other conversations and it still finds it. Plus the world simulates independently and NPCs talk to each other.

**Q: Does the memory scale?**
> Each NPC has a separate LlamaIndex vector store. Retrieval is O(log n) via similarity search, not O(n) scanning. You could have hundreds of NPCs with thousands of memories.

**Q: What happens if Pass Time fails halfway?**
> Temporal's durable execution model means the workflow resumes from the last completed activity. If event generation succeeds but NPC memory update fails, it retries just the memory update. No data loss.

**Q: Why not just use a database for memory?**
> Databases do exact matching. Our memories are semantic. "Do you remember the dragon?" matches a memory about "heading north to hunt the beast" even though the word "dragon" wasn't used. That's the vector similarity search.

**Q: How are the worlds isolated?**
> Each scenario gets its own SQLite database file and its own LlamaIndex index directory. Switching worlds just changes which files the backend reads from. No data bleeds between worlds.
