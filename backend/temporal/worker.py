import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from backend.core.config import Settings
from backend.temporal.workflows import (
    WorldSimulationWorkflow,
    generate_world_event_activity,
    update_npc_memory_activity,
)

TASK_QUEUE = "lorekeeper"


async def run_worker():
    settings = Settings()
    client = await Client.connect(settings.temporal_host)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[WorldSimulationWorkflow],
        activities=[generate_world_event_activity, update_npc_memory_activity],
    )

    print(f"Temporal worker started on queue: {TASK_QUEUE}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_worker())
