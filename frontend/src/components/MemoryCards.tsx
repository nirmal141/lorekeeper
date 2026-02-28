import "./MemoryCards.css";

interface Props {
  memories: string[];
}

export default function MemoryCards({ memories }: Props) {
  if (memories.length === 0) return null;

  return (
    <div className="memory-cards">
      <span className="memory-label">memories recalled</span>
      {memories.map((m, i) => (
        <div key={i} className="memory-card" style={{ animationDelay: `${i * 150}ms` }}>
          {m}
        </div>
      ))}
    </div>
  );
}
