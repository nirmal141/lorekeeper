import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Button } from "pixel-retroui";
import "./DialogueBox.css";

interface DialogueEntry {
  speaker: "player" | "narrator" | string;
  text: string;
  memories?: string[];
}

interface Props {
  entries: DialogueEntry[];
  loading: boolean;
  onSend: (msg: string) => void;
  npcName: string;
}

export default function DialogueBox({ entries, loading, onSend, npcName }: Props) {
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [entries, loading]);

  const handleSend = () => {
    if (!input.trim() || loading) return;
    onSend(input.trim());
    setInput("");
  };

  return (
    <div className="dialogue-box">
      <div className="db-scroll" ref={scrollRef}>
        <AnimatePresence>
          {entries.map((entry, i) => (
            <motion.div
              key={i}
              className={`db-entry ${entry.speaker === "player" ? "player" : entry.speaker === "narrator" ? "narrator" : "npc"}`}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              {entry.speaker !== "player" && entry.speaker !== "narrator" && (
                <span className="db-speaker">{entry.speaker}</span>
              )}
              {entry.speaker === "narrator" && (
                <span className="db-speaker narrator-label">Narrator</span>
              )}
              {entry.speaker === "player" && (
                <span className="db-speaker player-label">You</span>
              )}

              <p className="db-text">{entry.text}</p>

              {entry.memories && entry.memories.length > 0 && (
                <motion.div
                  className="db-memories"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  <span className="db-mem-label">⟡ memories recalled</span>
                  {entry.memories.map((m, j) => (
                    <p key={j} className="db-mem-text">{m}</p>
                  ))}
                </motion.div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            className="db-entry npc"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <span className="db-speaker">{npcName}</span>
            <div className="db-thinking">
              <span className="db-dot" />
              <span className="db-dot" />
              <span className="db-dot" />
            </div>
          </motion.div>
        )}
      </div>

      <div className="db-input-row">
        <input
          className="db-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder={`Say something to ${npcName}...`}
          disabled={loading}
        />
        <Button
          onClick={handleSend}
          bg="#533483"
          textColor="#f1c40f"
          shadow="#1a1a2e"
          className="db-send-btn"
          disabled={loading || !input.trim()}
        >
          Speak
        </Button>
      </div>
    </div>
  );
}
