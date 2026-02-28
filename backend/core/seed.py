import json

from backend.core.config import Settings
from backend.core.database import get_db, init_db
from backend.core.scenarios import SCENARIOS


def seed_scenario(settings: Settings, scenario_id: str) -> None:
    scenario = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return

    scoped = settings.for_scenario(scenario_id)
    conn = get_db(scoped)
    init_db(conn)

    if conn.execute("SELECT COUNT(*) FROM npcs").fetchone()[0] > 0:
        conn.close()
        return

    conn.execute(
        "INSERT INTO world_state (id, description, hours_passed) VALUES (1, ?, 0)",
        (scenario["description"],),
    )

    npcs = [
        (
            npc["id"],
            npc["name"],
            npc["role"],
            npc["backstory"],
            json.dumps(npc["goals"]),
        )
        for npc in scenario["npcs"]
    ]

    conn.executemany(
        "INSERT INTO npcs (id, name, role, backstory, goals, current_mood) VALUES (?, ?, ?, ?, ?, 'neutral')",
        npcs,
    )
    conn.commit()
    conn.close()


def seed_all(settings: Settings) -> None:
    for scenario in SCENARIOS:
        seed_scenario(settings, scenario["id"])
