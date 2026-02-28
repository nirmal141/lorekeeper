import type { NPC } from "../api";
import "./NPCCard.css";

interface Props {
  npc: NPC;
  selected: boolean;
  onClick: () => void;
}

const MOOD_COLORS: Record<string, string> = {
  neutral: "#5a5a7a",
  affected: "#e8a84c",
  worried: "#d4764a",
  angry: "#c45a5a",
  hopeful: "#5a9a6a",
};

export default function NPCCard({ npc, selected, onClick }: Props) {
  const moodColor = MOOD_COLORS[npc.current_mood] || MOOD_COLORS.neutral;

  return (
    <button className={`npc-card ${selected ? "selected" : ""}`} onClick={onClick}>
      <div className="npc-card-header">
        <strong className="npc-card-name">{npc.personality.name}</strong>
        <div className="npc-card-mood">
          <span className="mood-dot" style={{ background: moodColor }} />
          <span className="mood-text">{npc.current_mood}</span>
        </div>
      </div>
      <span className="npc-card-role">{npc.personality.role}</span>
    </button>
  );
}
