import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Card } from "pixel-retroui";
import { type ScenarioSummary, getScenarios, activateScenario } from "../api";
import "./ScenarioSelect.css";

interface Props {
  onSelect: (scenarioId: string) => void;
}

const GENRE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Fantasy: { bg: "#2d1b4e", text: "#c084fc", border: "#7c3aed" },
  "Sci-Fi": { bg: "#0c2d48", text: "#38bdf8", border: "#0284c7" },
  Western: { bg: "#3b2008", text: "#fbbf24", border: "#b45309" },
  Noir: { bg: "#1a1a1a", text: "#a1a1aa", border: "#52525b" },
  Modern: { bg: "#0a2e1a", text: "#4ade80", border: "#16a34a" },
};

const SCENARIO_IMAGES: Record<string, string> = {
  ashwood: "/ashwood_station.png",
  starfall: "/starfall_station.png",
  "dusty-gulch": "/dusty_gulch.png",
  holloway: "/holloway_case.png",
  "byte-brew": "/byte_and_brew.png",
};

export default function ScenarioSelect({ onSelect }: Props) {
  const [scenarios, setScenarios] = useState<ScenarioSummary[]>([]);
  const [activating, setActivating] = useState<string | null>(null);

  useEffect(() => {
    getScenarios().then(setScenarios);
  }, []);

  const handleSelect = async (id: string) => {
    setActivating(id);
    await activateScenario(id);
    onSelect(id);
  };

  return (
    <motion.div
      className="ss-screen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <motion.h2
        className="ss-title"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2, type: "spring" }}
      >
        Choose Your World
      </motion.h2>
      <motion.p
        className="ss-subtitle"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        Each world has its own NPCs, memories, and timeline
      </motion.p>

      <div className="ss-grid">
        {scenarios.map((s, i) => {
          const colors = GENRE_COLORS[s.genre] || GENRE_COLORS.Fantasy;
          return (
            <motion.div
              key={s.id}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + i * 0.1, type: "spring" }}
              whileHover={{ scale: 1.04, y: -4 }}
              whileTap={{ scale: 0.97 }}
              className="ss-card-wrapper"
            >
              <Card
                bg="#16213e"
                textColor="#e0e0e0"
                borderColor={colors.border}
                shadowColor="#0a0a14"
                className="ss-card"
              >
                <div className="ss-card-inner" onClick={() => !activating && handleSelect(s.id)}>
                  <div className="ss-img-wrapper">
                    <img src={SCENARIO_IMAGES[s.id]} alt={s.name} className="ss-img" />
                    <div className="ss-img-overlay" />
                  </div>
                  <div className="ss-card-text">
                    <span className="ss-genre" style={{ background: colors.bg, color: colors.text, borderColor: colors.border }}>
                      {s.genre}
                    </span>
                    <h3 className="ss-name">{s.name}</h3>
                    <p className="ss-tagline">{s.tagline}</p>
                    {activating === s.id && <span className="ss-loading">Loading world...</span>}
                  </div>
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      <motion.div
        className="ss-tech"
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.3 }}
        transition={{ delay: 1.2 }}
      >
        Powered by Gemini 2.5 · LlamaIndex · Temporal
      </motion.div>
    </motion.div>
  );
}
