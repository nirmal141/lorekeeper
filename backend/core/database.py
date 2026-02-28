import json
import sqlite3
from pathlib import Path

from backend.core.config import Settings
from backend.core.models import NPC, NPCPersonality, WorldEvent, WorldState


def get_db(settings: Settings) -> sqlite3.Connection:
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS world_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            description TEXT NOT NULL,
            hours_passed INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS world_events (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            affected_npc_ids TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS npcs (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            backstory TEXT NOT NULL,
            goals TEXT NOT NULL,
            current_mood TEXT NOT NULL DEFAULT 'neutral'
        );
    """)
    conn.commit()


def get_world_state(conn: sqlite3.Connection) -> WorldState:
    row = conn.execute("SELECT * FROM world_state WHERE id = 1").fetchone()
    if not row:
        return WorldState(description="Unknown world", hours_passed=0)
    events = conn.execute(
        "SELECT description FROM world_events ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()
    return WorldState(
        description=row["description"],
        hours_passed=row["hours_passed"],
        recent_events=[e["description"] for e in events],
    )


def save_world_event(conn: sqlite3.Connection, event: WorldEvent) -> None:
    conn.execute(
        "INSERT INTO world_events (id, description, timestamp, affected_npc_ids) VALUES (?, ?, ?, ?)",
        (event.id, event.description, event.timestamp.isoformat(), json.dumps(event.affected_npc_ids)),
    )
    conn.execute(
        "UPDATE world_state SET hours_passed = hours_passed + 6 WHERE id = 1"
    )
    conn.commit()


def get_npcs(conn: sqlite3.Connection) -> list[NPC]:
    rows = conn.execute("SELECT * FROM npcs").fetchall()
    return [
        NPC(
            id=row["id"],
            personality=NPCPersonality(
                name=row["name"],
                role=row["role"],
                backstory=row["backstory"],
                goals=json.loads(row["goals"]),
            ),
            current_mood=row["current_mood"],
        )
        for row in rows
    ]


def get_npc(conn: sqlite3.Connection, npc_id: str) -> NPC | None:
    row = conn.execute("SELECT * FROM npcs WHERE id = ?", (npc_id,)).fetchone()
    if not row:
        return None
    return NPC(
        id=row["id"],
        personality=NPCPersonality(
            name=row["name"],
            role=row["role"],
            backstory=row["backstory"],
            goals=json.loads(row["goals"]),
        ),
        current_mood=row["current_mood"],
    )


def update_npc_mood(conn: sqlite3.Connection, npc_id: str, mood: str) -> None:
    conn.execute("UPDATE npcs SET current_mood = ? WHERE id = ?", (mood, npc_id))
    conn.commit()
