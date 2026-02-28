import { useState } from "react";
import "./HowItWorks.css";

export default function HowItWorks() {
  const [open, setOpen] = useState(false);

  return (
    <div className="hiw">
      <button className="hiw-toggle" onClick={() => setOpen(!open)}>
        <span>How It Works</span>
        <span className={`hiw-chevron ${open ? "open" : ""}`}>&#9662;</span>
      </button>

      {open && (
        <div className="hiw-content">
          <div className="hiw-flow">
            <span className="hiw-label">Chat</span>
            <div className="hiw-row">
              <span className="hiw-box">Player Message</span>
              <span className="hiw-arrow">&rarr;</span>
              <span className="hiw-box accent">LlamaIndex<br/>Memory RAG</span>
              <span className="hiw-arrow">&rarr;</span>
              <span className="hiw-box accent">Gemini 2.5<br/>Flash</span>
              <span className="hiw-arrow">&rarr;</span>
              <span className="hiw-box">NPC Response</span>
            </div>
          </div>

          <div className="hiw-flow">
            <span className="hiw-label">Pass Time</span>
            <div className="hiw-row">
              <span className="hiw-box gold">Temporal<br/>Workflow</span>
              <span className="hiw-arrow">&rarr;</span>
              <span className="hiw-box accent">Gemini<br/>World Sim</span>
              <span className="hiw-arrow">&rarr;</span>
              <span className="hiw-box gold">LlamaIndex<br/>NPC Update</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
