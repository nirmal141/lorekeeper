import { useEffect, useRef, useState } from "react";
import MemoryCards from "./MemoryCards";
import "./ChatTerminal.css";

export interface Message {
  sender: "player" | "npc" | "system";
  text: string;
  memories?: string[];
}

interface Props {
  messages: Message[];
  loading: boolean;
  onSend: (msg: string) => void;
  disabled: boolean;
}

export default function ChatTerminal({ messages, loading, onSend, disabled }: Props) {
  const [input, setInput] = useState("");
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = () => {
    if (!input.trim() || disabled || loading) return;
    onSend(input.trim());
    setInput("");
  };

  return (
    <div className="chat-terminal">
      <div className="ct-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`ct-msg ${msg.sender}`}>
            <span className="ct-msg-text">{msg.text}</span>
            {msg.memories && msg.memories.length > 0 && (
              <MemoryCards memories={msg.memories} />
            )}
          </div>
        ))}
        {loading && (
          <div className="ct-msg system">
            <span className="ct-thinking">
              <span className="dot" />
              <span className="dot" />
              <span className="dot" />
            </span>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <div className="ct-input-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Speak to the NPC..."
          disabled={disabled || loading}
        />
        <button onClick={handleSend} disabled={disabled || loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}
