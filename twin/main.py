import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
import time
from tabulate import tabulate

from core.event_bus import EventBus, Event
from core.dt_state import DTState
from storage.repository import AsyncEventRepository
from cognitive_map.graph import CognitiveGraph
from pattern.discovery import PatternDiscoveryEngine
from prediction.engine import PredictionEngine
from prediction.models import MarkovPredictionModel, BayesianPredictionModel
from identity.fingerprint import IdentityRecognitionEngine
from simulation.presence import DigitalPresenceSimulator

from collectors.window_tracker import WindowTrackerCollector
from collectors.input_timing import InputTimingCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DTCE_Main")

class DigitalTwinConsciousnessEngine:
    """
    Main orchestrator for the DTCE v2 architecture.
    Initializes and links all subsystems using dependency injection.
    """
    def __init__(self):
        # 1. State & Bus
        self.dt_state = DTState()
        self.event_bus = EventBus()
        
        # 2. Async Storage & Graph
        self.repository = AsyncEventRepository()
        self.cognitive_graph = CognitiveGraph()
        
        # 3. Engines
        self.pattern_engine = PatternDiscoveryEngine(self.repository)
        
        # Multi-model prediction system
        markov_model = MarkovPredictionModel(self.cognitive_graph, self.pattern_engine)
        bayesian_model = BayesianPredictionModel(self.pattern_engine)
        self.prediction_engine = PredictionEngine(models=[markov_model, bayesian_model])
        
        self.identity_engine = IdentityRecognitionEngine(self.repository)
        self.simulation_engine = DigitalPresenceSimulator(self.dt_state, self.prediction_engine, self.cognitive_graph)
        
        # 4. Collectors
        self.collectors = [
            WindowTrackerCollector(self.event_bus, interval_seconds=1.0),
            InputTimingCollector(self.event_bus, interval_seconds=5.0)
        ]

    def _setup_event_handlers(self):
        async def on_window_changed(event: Event):
            app_name = event.payload.get("app_name")
            title = event.payload.get("window_title")
            
            last_app = self.dt_state.current_window.app_name if self.dt_state.current_window else None
            self.dt_state.update_window(app_name, title, event.payload.get("pid"))
            
            # Non-blocking async DB write
            await self.repository.save_event(event)
            
            # Multi-layer Cognitive Graph update
            self.cognitive_graph.add_node(app_name, layer="app", metadata={"last_title": title})
            
            if last_app and last_app != app_name:
                self.cognitive_graph.add_edge(last_app, app_name, base_weight=1.0, relation_type="window_transition")
                
            logger.info(f"[Real-time State Change] Focus: {app_name} | {title}")

        async def on_input_activity(event: Event):
            self.dt_state.mark_active()
            await self.repository.save_event(event)

        self.event_bus.subscribe("WindowChangedEvent", on_window_changed)
        self.event_bus.subscribe("InputActivityEvent", on_input_activity)

    async def start(self):
        logger.info("Initializing Digital Twin Consciousness Engine v2...")
        
        await self.repository.initialize_db()
        self._setup_event_handlers()
        await self.event_bus.start()
        
        for collector in self.collectors:
            collector.start()
            
        logger.info("DTCE v2 System fully operational.")
        
    async def stop(self):
        logger.info("Initiating shutdown sequence...")
        for collector in self.collectors:
            collector.stop()
            
        await self.event_bus.stop()
        logger.info("DTCE Offline.")


async def demo_loop():
    engine = DigitalTwinConsciousnessEngine()
    
    print("==========================================================")
    print(" DIGITAL TWIN CONSCIOUSNESS ENGINE (DTCE v2) INIT ")
    print("==========================================================")
    
    await engine.start()
    
    # Inject baseline to demonstrate the ensemble logic and layered graph
    print("[ SYSTEM ] Injecting baseline cognitive seeding...")
    engine.cognitive_graph.add_node("chrome.exe", "app")
    engine.cognitive_graph.add_node("code.exe", "app")
    engine.cognitive_graph.add_edge("chrome.exe", "code.exe", base_weight=2.0)
    engine.cognitive_graph.add_edge("code.exe", "chrome.exe", base_weight=1.5)

    try:
        iterations = 0
        while True:
            await asyncio.sleep(5)
            iterations += 1
            
            print("\\n----------------------------------------------------------")
            print(f"[ ENGINE STATUS REPORT - Iteration {iterations} ]")
            
            fp = await engine.identity_engine.generate_fingerprint()
            print(f"\\n>>  Identity Hash (Behavioral): {fp.get('hash')} (Confidence: {fp.get('confidence'):.2f})")
            
            current_app = "unknown"
            if engine.dt_state.current_window:
                current_app = engine.dt_state.current_window.app_name
                print(f">>  Current Active Window: {current_app}")
            
            preds = engine.prediction_engine.predict_next_app(current_app)
            if preds:
                headers = ["Ensemble Predicted Next App", "Probability"]
                data = [[app, f"{prob*100:.1f}%"] for app, prob in preds]
                print("\\n>>  Ensemble Cognitive Predictive Model:")
                print(tabulate(data, headers=headers, tablefmt="grid"))
            
            branches = engine.simulation_engine.generate_what_if_timeline(steps=4, num_branches=2)
            print("\\n>>  Digital Presence What-If Simulations:")
            for b in branches:
                print(f"   [Branch {b['branch_id']} - {b['path_confidence']*100:.1f}%] {' -> '.join(b['simulated_sequence'])}")
            
            print("----------------------------------------------------------")
            print("[ SYSTEM ] Engine operational. Press Ctrl+C to stop.")
                
    except asyncio.CancelledError:
        pass
    finally:
        await engine.stop()


if __name__ == "__main__":
    try:
        asyncio.run(demo_loop())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Fatal error running entry point: {e}")

