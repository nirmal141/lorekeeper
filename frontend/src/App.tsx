import { useState } from "react";
import { AnimatePresence } from "motion/react";
import IntroScreen from "./components/IntroScreen";
import ScenarioSelect from "./components/ScenarioSelect";
import GameWorld from "./components/GameWorld";

type Phase = "intro" | "select" | "game";

function App() {
  const [phase, setPhase] = useState<Phase>("intro");

  return (
    <AnimatePresence mode="wait">
      {phase === "intro" && (
        <IntroScreen key="intro" onEnter={() => setPhase("select")} />
      )}
      {phase === "select" && (
        <ScenarioSelect key="select" onSelect={() => setPhase("game")} />
      )}
      {phase === "game" && (
        <GameWorld key="world" onBack={() => setPhase("select")} />
      )}
    </AnimatePresence>
  );
}

export default App;
