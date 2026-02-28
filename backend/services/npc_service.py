from pathlib import Path
from typing import Optional

from google import genai
from llama_index.core import Document, Settings as LlamaSettings, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding

from backend.core.config import Settings
from backend.core.models import ChatRequest, ChatResponse, Memory, NPC, WorldEvent, WorldState


class NPCService:
    def __init__(self, settings: Settings, embed_model: Optional[BaseEmbedding] = None):
        self._client = genai.Client(api_key=settings.gemini_api_key)
        if embed_model is None:
            embed_model = GeminiEmbedding(
                api_key=settings.gemini_api_key,
                model_name="models/gemini-embedding-001",
            )
        LlamaSettings.embed_model = embed_model
        self._index_dir = Path(settings.index_dir)
        self._index_dir.mkdir(parents=True, exist_ok=True)
        self._indexes: dict[str, VectorStoreIndex] = {}

    def _get_index(self, npc_id: str) -> VectorStoreIndex:
        if npc_id in self._indexes:
            return self._indexes[npc_id]

        persist_dir = str(self._index_dir / npc_id)
        if Path(persist_dir).exists():
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = load_index_from_storage(storage_context)
        else:
            index = VectorStoreIndex([])
            index.storage_context.persist(persist_dir=persist_dir)

        self._indexes[npc_id] = index
        return index

    def _retrieve_memories(self, npc_id: str, query: str, top_k: int = 5) -> list[str]:
        index = self._get_index(npc_id)
        if not index.docstore.docs:
            return []
        retriever = index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)
        return [node.text for node in nodes]

    def _store_memory(self, npc_id: str, memory: Memory) -> None:
        index = self._get_index(npc_id)
        doc = Document(
            text=f"[{memory.memory_type}] {memory.content}",
            metadata={"timestamp": memory.timestamp.isoformat(), "type": memory.memory_type},
        )
        index.insert(doc)
        persist_dir = str(self._index_dir / npc_id)
        index.storage_context.persist(persist_dir=persist_dir)

    async def chat(self, npc: NPC, world_state: WorldState, request: ChatRequest) -> ChatResponse:
        memories = self._retrieve_memories(npc.id, request.player_message)

        memories_block = "\n".join(f"- {m}" for m in memories) if memories else "No prior memories of this player."

        prompt = f"""You are {npc.personality.name}, a {npc.personality.role}.

BACKSTORY: {npc.personality.backstory}

YOUR GOALS: {', '.join(npc.personality.goals)}

CURRENT MOOD: {npc.current_mood}

WORLD STATE: {world_state.description}
RECENT EVENTS: {', '.join(world_state.recent_events) if world_state.recent_events else 'Nothing notable recently.'}

YOUR MEMORIES OF THIS PLAYER:
{memories_block}

The player says: "{request.player_message}"

Respond in character as {npc.personality.name}. Be concise (2-4 sentences). Reference your memories of this player if relevant. React to recent world events if they affect you. Stay in character."""

        response = self._client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        npc_dialogue = response.text

        self._store_memory(
            npc.id,
            Memory(
                content=f"Player said: '{request.player_message}'. I responded: '{npc_dialogue}'",
                memory_type="player_interaction",
            ),
        )

        return ChatResponse(
            npc_id=npc.id,
            npc_dialogue=npc_dialogue,
            memories_retrieved=memories,
        )

    def add_world_event_to_npc(self, npc_id: str, event: WorldEvent) -> None:
        self._store_memory(
            npc_id,
            Memory(
                content=f"World event: {event.description}",
                memory_type="world_event",
            ),
        )
