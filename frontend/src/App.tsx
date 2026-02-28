import { useState } from "react";
import { AnimatePresence } from "motion/react";
import IntroScreen from "./components/IntroScreen";
import GameWorld from "./components/GameWorld";

function App() {
  const [started, setStarted] = useState(false);

  return (
    <AnimatePresence mode="wait">
      {!started ? (
        <IntroScreen key="intro" onEnter={() => setStarted(true)} />
      ) : (
        <GameWorld key="world" />
      )}
    </AnimatePresence>
  );
}

export default App;
