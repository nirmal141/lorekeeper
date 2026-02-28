import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Card, Button } from "pixel-retroui";
import {
  type NPC,
  type WorldState,
  type WorldEvent,
  type SimulationResult,
  getWorld,
  getNPCs,
  getEvents,
  chatWithNPC,
  simulateWorld,
} from "../api";
import DialogueBox from "./DialogueBox";
import CinematicOverlay from "./CinematicOverlay";
import "./GameWorld.css";

interface DialogueEntry {
  speaker: "player" | "narrator" | string;
  text: string;
  memories?: string[];
}

export default function GameWorld() {
  const [world, setWorld] = useState<WorldState | null>(null);
  const [npcs, setNpcs] = useState<NPC[]>([]);
  const [events, setEvents] = useState<WorldEvent[]>([]);
  const [selectedNpc, setSelectedNpc] = useState<NPC | null>(null);
  const [dialogue, setDialogue] = useState<DialogueEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [simulating, setSimulating] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);
  const [latestResult, setLatestResult] = useState<SimulationResult | null>(null);

  const npcNames: Record<string, string> = {};
  npcs.forEach((n) => { npcNames[n.id] = n.personality.name; });

  useEffect(() => {
    Promise.all([getWorld(), getNPCs(), getEvents()]).then(([w, n, e]) => {
      setWorld(w);
      setNpcs(n);
      setEvents(e);
      setDialogue([{
        speaker: "narrator",
        text: `You arrive at the trading post. ${w.description}`,
      }]);
    });
  }, []);

  const handleTalkToNPC = (npc: NPC) => {
    setSelectedNpc(npc);
    setDialogue([{
      speaker: "narrator",
      text: `You approach ${npc.personality.name}, the ${npc.personality.role}.`,
    }]);
  };

  const handleSend = async (msg: string) => {
    if (!selectedNpc || loading) return;
    setDialogue((prev) => [...prev, { speaker: "player", text: msg }]);
    setLoading(true);

    try {
      const res = await chatWithNPC(selectedNpc.id, msg);
      setDialogue((prev) => [
        ...prev,
        {
          speaker: selectedNpc.personality.name,
          text: res.npc_dialogue,
          memories: res.memories_retrieved,
        },
      ]);
    } catch {
      setDialogue((prev) => [...prev, { speaker: "narrator", text: "The NPC doesn't respond..." }]);
    }
    setLoading(false);
  };

  const handlePassTime = async () => {
    if (simulating) return;
    setSimulating(true);

    try {
      const result = await simulateWorld();
      setLatestResult(result);
      setShowOverlay(true);
    } catch {
      setDialogue((prev) => [
        ...prev,
        { speaker: "narrator", text: "The world remains still... (Is the Temporal worker running?)" },
      ]);
      setSimulating(false);
    }
  };

  const handleOverlayDone = async () => {
    setShowOverlay(false);
    if (latestResult) {
      setDialogue((prev) => [
        ...prev,
        { speaker: "narrator", text: latestResult.event.description },
      ]);
    }
    const [w, n, e] = await Promise.all([getWorld(), getNPCs(), getEvents()]);
    setWorld(w);
    setNpcs(n);
    setEvents(e);
    setSimulating(false);
  };

  const handleBack = () => {
    setSelectedNpc(null);
    setDialogue([{
      speaker: "narrator",
      text: "You step back and survey the trading post.",
    }]);
  };

  return (
    <motion.div
      className="game-world"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Top bar */}
      <div className="gw-topbar">
        <span className="gw-title">Lorekeeper</span>
        <span className="gw-hours">Day {Math.floor((world?.hours_passed ?? 0) / 24) + 1} · Hour {(world?.hours_passed ?? 0) % 24}</span>
      </div>

      {/* Main area */}
      <div className="gw-main">
        {/* Left: World info */}
        <div className="gw-sidebar">
          <Card bg="#16213e" textColor="#e0e0e0" borderColor="#533483" shadowColor="#0a0a14" className="gw-card">
            <h3 className="gw-card-title">The Trading Post</h3>
            <p className="gw-card-text">{world?.description}</p>
          </Card>

          {events.length > 0 && (
            <Card bg="#16213e" textColor="#e0e0e0" borderColor="#533483" shadowColor="#0a0a14" className="gw-card">
              <h3 className="gw-card-title">Recent Events</h3>
              {events.slice(0, 4).map((e) => (
                <p key={e.id} className="gw-event-text">· {e.description}</p>
              ))}
            </Card>
          )}

          <Card bg="#16213e" textColor="#e0e0e0" borderColor="#533483" shadowColor="#0a0a14" className="gw-card gw-arch">
            <h3 className="gw-card-title">Architecture</h3>
            <p className="gw-arch-row"><span className="gw-tag purple">Gemini 2.5</span> NPC Dialogue + World Sim</p>
            <p className="gw-arch-row"><span className="gw-tag gold">LlamaIndex</span> NPC Episodic Memory</p>
            <p className="gw-arch-row"><span className="gw-tag red">Temporal</span> Durable World Workflows</p>
          </Card>
        </div>

        {/* Center: NPC area or dialogue */}
        <div className="gw-center">
          <AnimatePresence mode="wait">
            {!selectedNpc ? (
              <motion.div
                key="npc-select"
                className="gw-npc-grid"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <p className="gw-prompt">Who would you like to speak with?</p>
                <div className="gw-npcs">
                  {npcs.map((npc) => (
                    <motion.div
                      key={npc.id}
                      whileHover={{ scale: 1.03 }}
                      whileTap={{ scale: 0.97 }}
                    >
                      <div onClick={() => handleTalkToNPC(npc)}>
                      <Card
                        bg="#0f3460"
                        textColor="#e0e0e0"
                        borderColor="#533483"
                        shadowColor="#0a0a14"
                        className="gw-npc-card"
                      >
                        <div className="gw-npc-name">{npc.personality.name}</div>
                        <div className="gw-npc-role">{npc.personality.role}</div>
                        <div className="gw-npc-mood">
                          <span className="gw-mood-dot" style={{ background: npc.current_mood === "neutral" ? "#6a6a8a" : "#f1c40f" }} />
                          {npc.current_mood}
                        </div>
                        <div className="gw-npc-goal">{npc.personality.goals[0]}</div>
                      </Card>
                      </div>
                    </motion.div>
                  ))}
                </div>

                <Button
                  onClick={handlePassTime}
                  bg="#533483"
                  textColor="#f1c40f"
                  shadow="#1a1a2e"
                  className="gw-pass-btn"
                  disabled={simulating}
                >
                  {simulating ? "Simulating..." : "⏳ Pass Time"}
                </Button>
              </motion.div>
            ) : (
              <motion.div
                key="dialogue"
                className="gw-dialogue-area"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <div className="gw-dialogue-header">
                  <Button
                    onClick={handleBack}
                    bg="#16213e"
                    textColor="#e0e0e0"
                    shadow="#0a0a14"
                    borderColor="#533483"
                    className="gw-back-btn"
                  >
                    ← Back
                  </Button>
                  <span className="gw-talking-to">Speaking with {selectedNpc.personality.name}</span>
                </div>

                <DialogueBox
                  entries={dialogue}
                  loading={loading}
                  onSend={handleSend}
                  npcName={selectedNpc.personality.name}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <CinematicOverlay
        visible={showOverlay}
        result={latestResult}
        npcNames={npcNames}
        onDone={handleOverlayDone}
      />
    </motion.div>
  );
}
