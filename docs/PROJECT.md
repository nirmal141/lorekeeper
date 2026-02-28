# Lorekeeper — Project Overview

## What Is It?

Lorekeeper is a browser-based RPG engine where **NPCs genuinely remember you** and **the world keeps moving when you leave**.

Pick a world — a fantasy trading post, a failing space station, a frontier town with a dead sheriff, a noir murder mystery, or a startup on the brink of collapse. Talk to the NPCs. Build relationships. Then walk away. When you come back, the world has changed. NPCs have talked to each other about you. Events have unfolded. And every NPC remembers exactly what you said.

## Why Is It Interesting?

Every game ever made has the same problem: **the world is a frozen diorama that only animates when you're looking at it.** NPCs have no memory. Nothing happens between sessions. Talk to a shopkeeper 100 times and they greet you like a stranger every time.

Lorekeeper solves three things no current game does well together:

### 1. Genuine Episodic Memory
Tell the blacksmith you're hunting a dragon. Come back 5 conversations later — she remembers. Not because we scripted it, but because every conversation is stored as a vector embedding and semantically retrieved when relevant. Ask "do you remember the dragon?" and the system finds that memory even if 50 other conversations happened since.

### 2. Persistent World Simulation
Hit "Pass Time" and the world simulates itself through a durable workflow. Bandits raid. Storms hit. NPCs make decisions. The simulation runs as an orchestrated pipeline — if the server crashes mid-simulation, it picks up exactly where it left off.

### 3. NPC Social Networks
NPCs talk to each other. When you tell Aldric about the dragon, he tells Mira during the next simulation. When you talk to Mira later, she already knows — even though you never told her. NPCs have social lives that exist independently of the player.

## The 5 Worlds

| World | Genre | Setting |
|-------|-------|---------|
| **The Ashwood Post** | Fantasy | A trading post under bandit threat. An aging merchant and a secretive blacksmith. |
| **Starfall Station** | Sci-Fi | A space station with a failing reactor. A stern commander and a suspicious scientist. |
| **Dusty Gulch** | Western | A frontier town where the sheriff just died. A saloon owner and a scared deputy. |
| **The Holloway Case** | Noir | A rain-soaked city. Your client is dead and the answers aren't. A detective and an informant. |
| **Byte & Brew** | Modern | Demo day is tomorrow. The product crashed. The co-founders aren't speaking. |

Each world has its own database, memory indexes, event timeline, and NPC moods. They're fully isolated — progress in one world doesn't affect another.

## How To Play

### Step 1: Choose a World
Pick one of the 5 scenarios. Each has a unique setting, tone, and pair of NPCs with rich backstories and personal goals.

### Step 2: Talk to an NPC
Click an NPC to enter dialogue mode. You'll see 3 starter suggestions to get the conversation going. Or type anything you want — NPCs respond in character based on their personality, mood, goals, and what they remember about you.

### Step 3: Build a Relationship
Keep talking. Tell them your plans. Ask about their life. Make promises. Be rude. Every word gets stored in their memory and shapes how they treat you in the future.

### Step 4: Pass Time
Go back to the world view and hit "Pass Time." The world simulates itself:
- A **"Previously on..."** narrative recap appears, summarizing the story so far
- A **world event** unfolds — bandits, storms, discoveries, betrayals
- **NPC reactions** show how each character was affected
- **Gossip spreads** — NPCs share information with each other about you and about events

### Step 5: Return and See the Difference
Talk to the same NPC again. They now reference:
- Everything you told them before (your personal history)
- The world event that just happened (their experience)
- What other NPCs told them about you (gossip)

All woven naturally into one coherent, in-character response. That's the magic.

### Step 6: Repeat
Hit Pass Time again. The world builds on itself — causal chains, escalating tensions, evolving relationships. Every session is different because the world has genuine history.

## What Makes This Different From a Chatbot?

A chatbot responds to your last message. Lorekeeper responds to your **entire relationship history**, the **world's event timeline**, and **information from other NPCs** — all at once.

The NPCs aren't prompts. They're characters with memories, moods, goals, and social connections that persist across sessions and evolve through events they witness independently of you.
