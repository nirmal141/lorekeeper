import { useState } from "react";
import { AnimatePresence } from "motion/react";
import IntroScreen from "./components/IntroScreen";
import ScenarioSelect from "./components/ScenarioSelect";
import GameWorld from "./components/GameWorld";

type Phase = "intro" | "select" | "game";

function getInitialPhase(): Phase {
  const saved = localStorage.getItem("lk_phase");
  if (saved === "game" && localStorage.getItem("lk_scenario")) return "game";
  if (saved === "select") return "select";
  return "intro";
}

function App() {
  const [phase, setPhase] = useState<Phase>(getInitialPhase);

  const goTo = (p: Phase) => {
    localStorage.setItem("lk_phase", p);
    setPhase(p);
  };

  return (
    <AnimatePresence mode="wait">
      {phase === "intro" && (
        <IntroScreen key="intro" onEnter={() => goTo("select")} />
      )}
      {phase === "select" && (
        <ScenarioSelect key="select" onSelect={() => goTo("game")} onHome={() => goTo("intro")} />
      )}
      {phase === "game" && (
        <GameWorld key="world" onBack={() => goTo("select")} onHome={() => goTo("intro")} />
      )}
    </AnimatePresence>
  );
}

export default App;
