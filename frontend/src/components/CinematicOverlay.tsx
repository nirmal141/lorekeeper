import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Button } from "pixel-retroui";
import { Typewriter } from "react-simple-typewriter";
import type { SimulationResult, NarrativeRecap } from "../api";
import "./CinematicOverlay.css";

interface Props {
  visible: boolean;
  result: SimulationResult | null;
  recap: NarrativeRecap | null;
  npcNames: Record<string, string>;
  onDone: () => void;
}

type Phase = "recap" | "event" | "gossip" | "done";

export default function CinematicOverlay({ visible, result, recap, npcNames, onDone }: Props) {
  const [phase, setPhase] = useState<Phase>("recap");
  const [showContent, setShowContent] = useState(false);
  const [showContinue, setShowContinue] = useState(false);

  useEffect(() => {
    if (!visible) return;
    setShowContent(false);
    setShowContinue(false);

    const hasRecap = recap && recap.summary && recap.key_moments.length > 0;
    setPhase(hasRecap ? "recap" : "event");

    const t = setTimeout(() => setShowContent(true), 500);
    return () => clearTimeout(t);
  }, [visible, recap]);

  useEffect(() => {
    if (!showContent || !visible) return;

    let delay = 3000;
    if (phase === "recap" && recap) {
      delay = recap.summary.length * 35 + 2000;
    } else if (phase === "event" && result) {
      delay = result.event.description.length * 35 + 2000;
    } else if (phase === "gossip") {
      delay = 2000;
    }

    const t = setTimeout(() => setShowContinue(true), delay);
    return () => clearTimeout(t);
  }, [showContent, phase, visible, recap, result]);

  if (!visible || !result) return null;

  const handleNext = () => {
    setShowContent(false);
    setShowContinue(false);

    if (phase === "recap") {
      setPhase("event");
      setTimeout(() => setShowContent(true), 300);
    } else if (phase === "event") {
      if (result.gossip && result.gossip.length > 0) {
        setPhase("gossip");
        setTimeout(() => setShowContent(true), 300);
      } else {
        onDone();
      }
    } else {
      onDone();
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        className="co-overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="co-content">
          {/* RECAP PHASE */}
          {phase === "recap" && recap && (
            <motion.div key="recap" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <span className="co-label">Previously on Lorekeeper...</span>
              {showContent && (
                <div className="co-recap">
                  <div className="co-event">
                    <Typewriter words={[recap.summary]} typeSpeed={30} cursor cursorStyle="_" />
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {/* EVENT PHASE */}
          {phase === "event" && (
            <motion.div key="event" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <span className="co-label">While you were away...</span>
              {showContent && (
                <>
                  <div className="co-event">
                    <Typewriter words={[result.event.description]} typeSpeed={30} cursor cursorStyle="_" />
                  </div>
                  <motion.div
                    className="co-reactions"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: result.event.description.length * 0.03 + 1 }}
                  >
                    {Object.entries(result.npc_reactions).map(([npcId, reaction], i) => (
                      <motion.div
                        key={npcId}
                        className="co-reaction"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.3 }}
                      >
                        <span className="co-reaction-name">{npcNames[npcId] || npcId}</span>
                        <p className="co-reaction-text">{reaction}</p>
                      </motion.div>
                    ))}
                  </motion.div>
                </>
              )}
            </motion.div>
          )}

          {/* GOSSIP PHASE */}
          {phase === "gossip" && (
            <motion.div key="gossip" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <span className="co-label">Meanwhile, whispers spread...</span>
              {showContent && (
                <div className="co-gossip">
                  {result.gossip.map((g, i) => (
                    <motion.div
                      key={i}
                      className="co-gossip-item"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.4 }}
                    >
                      <span className="co-gossip-arrow">
                        {npcNames[g.from_npc] || g.from_npc} → {npcNames[g.to_npc] || g.to_npc}
                      </span>
                      <p className="co-gossip-text">"{g.content}"</p>
                    </motion.div>
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {showContinue && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
              <Button
                onClick={handleNext}
                bg="#533483"
                textColor="#f1c40f"
                shadow="#1a1a2e"
                className="co-continue-btn"
              >
                {phase === "gossip" || (phase === "event" && (!result.gossip || result.gossip.length === 0))
                  ? "Return to World →"
                  : "Continue →"}
              </Button>
            </motion.div>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
