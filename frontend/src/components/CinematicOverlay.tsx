import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Button } from "pixel-retroui";
import { Typewriter } from "react-simple-typewriter";
import type { SimulationResult } from "../api";
import "./CinematicOverlay.css";

interface Props {
  visible: boolean;
  result: SimulationResult | null;
  npcNames: Record<string, string>;
  onDone: () => void;
}

export default function CinematicOverlay({ visible, result, npcNames, onDone }: Props) {
  const [showReactions, setShowReactions] = useState(false);
  const [showContinue, setShowContinue] = useState(false);

  useEffect(() => {
    if (!visible || !result) return;
    setShowReactions(false);
    setShowContinue(false);

    const len = result.event.description.length;
    const typeDuration = len * 35 + 500;
    const t1 = setTimeout(() => setShowReactions(true), typeDuration);
    const t2 = setTimeout(() => setShowContinue(true), typeDuration + 1500);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [visible, result]);

  if (!visible || !result) return null;

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
          <motion.span
            className="co-label"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            While you were away...
          </motion.span>

          <div className="co-event">
            <Typewriter
              words={[result.event.description]}
              typeSpeed={30}
              cursor
              cursorStyle="_"
            />
          </div>

          {showReactions && (
            <motion.div
              className="co-reactions"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
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
          )}

          {showContinue && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              <Button
                onClick={onDone}
                bg="#533483"
                textColor="#f1c40f"
                shadow="#1a1a2e"
                className="co-continue-btn"
              >
                Continue →
              </Button>
            </motion.div>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
