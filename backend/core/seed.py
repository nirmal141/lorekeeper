import json

from backend.core.config import Settings
from backend.core.database import get_db, init_db


def seed(settings: Settings) -> None:
    conn = get_db(settings)
    init_db(conn)

    if conn.execute("SELECT COUNT(*) FROM npcs").fetchone()[0] > 0:
        conn.close()
        return

    conn.execute(
        "INSERT INTO world_state (id, description, hours_passed) VALUES (1, ?, 0)",
        (
            "A quiet trading post at the edge of the Ashwood. "
            "Tensions have been rising since the northern roads closed. "
            "Merchants whisper about bandits, and the blacksmith has been forging more weapons than tools.",
        ),
    )

    npcs = [
        (
            "aldric",
            "Aldric",
            "merchant",
            "An aging merchant who lost his son to the northern wars. "
            "He runs the only supply shop at the trading post. "
            "Protective of his remaining stock and deeply suspicious of armed travelers, "
            "but shows kindness to those who earn his trust.",
            json.dumps(["protect his shop", "find news of his son", "keep the trading post safe"]),
        ),
        (
            "mira",
            "Blacksmith Mira",
            "blacksmith",
            "A skilled blacksmith who arrived at the trading post two years ago from the east. "
            "She speaks little about her past. She distrusts outsiders but is fiercely loyal "
            "to those she considers friends. Her blades are the finest in the region.",
            json.dumps(["forge a legendary weapon", "protect the trading post", "uncover the source of the bandit raids"]),
        ),
    ]

    conn.executemany(
        "INSERT INTO npcs (id, name, role, backstory, goals, current_mood) VALUES (?, ?, ?, ?, ?, 'neutral')",
        npcs,
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed(Settings())
