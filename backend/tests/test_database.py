import sqlite3

import pytest

from backend.core.database import (
    get_npc,
    get_npcs,
    get_world_state,
    init_db,
    save_world_event,
    update_npc_mood,
)
from backend.core.models import WorldEvent


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    init_db(c)
    yield c
    c.close()


@pytest.fixture
def seeded_conn(conn):
    conn.execute(
        "INSERT INTO world_state (id, description, hours_passed) VALUES (1, 'A quiet village', 0)"
    )
    conn.execute(
        "INSERT INTO npcs (id, name, role, backstory, goals, current_mood) VALUES (?, ?, ?, ?, ?, ?)",
        ("aldric", "Aldric", "merchant", "Old trader", '["survive"]', "neutral"),
    )
    conn.commit()
    return conn


class TestInitDb:
    def test_creates_tables(self, conn):
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        names = {t["name"] for t in tables}
        assert "world_state" in names
        assert "world_events" in names
        assert "npcs" in names


class TestWorldState:
    def test_get_empty(self, conn):
        ws = get_world_state(conn)
        assert ws.description == "Unknown world"

    def test_get_seeded(self, seeded_conn):
        ws = get_world_state(seeded_conn)
        assert ws.description == "A quiet village"
        assert ws.hours_passed == 0

    def test_save_event_increments_hours(self, seeded_conn):
        event = WorldEvent(description="Bandits attacked", affected_npc_ids=["aldric"])
        save_world_event(seeded_conn, event)
        ws = get_world_state(seeded_conn)
        assert ws.hours_passed == 6
        assert "Bandits attacked" in ws.recent_events


class TestNPCs:
    def test_get_npcs(self, seeded_conn):
        npcs = get_npcs(seeded_conn)
        assert len(npcs) == 1
        assert npcs[0].id == "aldric"
        assert npcs[0].personality.name == "Aldric"

    def test_get_npc_found(self, seeded_conn):
        npc = get_npc(seeded_conn, "aldric")
        assert npc is not None
        assert npc.personality.role == "merchant"

    def test_get_npc_not_found(self, seeded_conn):
        assert get_npc(seeded_conn, "nobody") is None

    def test_update_mood(self, seeded_conn):
        update_npc_mood(seeded_conn, "aldric", "worried")
        npc = get_npc(seeded_conn, "aldric")
        assert npc.current_mood == "worried"
