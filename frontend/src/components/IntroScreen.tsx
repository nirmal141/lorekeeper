import { motion } from "motion/react";
import { Typewriter } from "react-simple-typewriter";
import { Button } from "pixel-retroui";
import "./IntroScreen.css";

interface Props {
  onEnter: () => void;
}

export default function IntroScreen({ onEnter }: Props) {
  return (
    <motion.div
      className="intro-screen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="intro-content">
        <motion.h1
          className="intro-title"
          initial={{ y: -30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3, type: "spring" }}
        >
          Lorekeeper
        </motion.h1>

        <motion.p
          className="intro-subtitle"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          Every NPC remembers. Every world event persists.
        </motion.p>

        <motion.div
          className="intro-narrative"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
        >
          <Typewriter
            words={[
              "In most games, the world freezes when you leave. NPCs forget you. Nothing changes. Lorekeeper is different. Here, NPCs remember everything. The world simulates itself while you are away. When you return, the story has moved on without you...",
            ]}
            typeSpeed={30}
            cursor
            cursorStyle="_"
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 5 }}
        >
          <Button
            onClick={onEnter}
            bg="#533483"
            textColor="#f1c40f"
            shadow="#1a1a2e"
            className="intro-btn"
          >
            Choose Your World
          </Button>
        </motion.div>

        <motion.div
          className="intro-tech"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.4 }}
          transition={{ delay: 5.5 }}
        >
          Powered by Gemini · LlamaIndex · Temporal
        </motion.div>
      </div>
    </motion.div>
  );
}
