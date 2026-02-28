import type { WorldState, WorldEvent } from "../api";
import "./WorldTimeline.css";

interface Props {
  world: WorldState | null;
  events: WorldEvent[];
}

export default function WorldTimeline({ world, events }: Props) {
  if (!world) return null;

  return (
    <div className="world-timeline">
      <h3>World</h3>
      <p className="wt-desc">{world.description}</p>
      <p className="wt-hours">Hours passed: {world.hours_passed}</p>

      {events.length > 0 && (
        <div className="wt-events">
          <h4>Timeline</h4>
          <div className="tl-line">
            {events.slice(0, 8).map((e) => (
              <div key={e.id} className="tl-node">
                <span className="tl-dot" />
                <span className="tl-text">{e.description}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
