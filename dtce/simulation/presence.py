import logging
from typing import Dict, Any, List, Optional

from prediction.engine import PredictionEngine
from cognitive_map.graph import CognitiveGraph
from core.dt_state import DTState

logger = logging.getLogger(__name__)

class DigitalPresenceSimulator:
    """
    Simulates the digital presence of the user based on historical models.
    Supports multi-branched \"what-if\" path generations.
    """
    def __init__(self, dt_state: DTState, prediction_engine: PredictionEngine, cognitive_graph: CognitiveGraph):
        self.dt_state = dt_state
        self.prediction_engine = prediction_engine
        self.graph = cognitive_graph

    def generate_expected_timeline(self, steps: int = 5) -> Dict[str, Any]:
        return self.generate_what_if_timeline(start_state=None, steps=steps, num_branches=1)[0]

    def generate_what_if_timeline(self, start_state: Optional[str] = None, steps: int = 5, num_branches: int = 3) -> List[Dict[str, Any]]:
        """
        Generates multiple probable branches of future activity.
        """
        current_app = start_state
        if not current_app:
            current_app = self.dt_state.current_window.app_name if self.dt_state.current_window else "unknown"
            
        branches = []
        for i in range(num_branches):
            # Seed the generation differently based on probability weightings
            simulated_path = self.prediction_engine.simulate_future_path(current_app, steps=steps)
            
            path_confidence = 1.0
            for j in range(len(simulated_path) - 1):
                source = simulated_path[j]
                target = simulated_path[j+1]
                
                predictions = self.prediction_engine.predict_next_app(source)
                target_prob = next((prob for app, prob in predictions if app == target), 0.1)
                path_confidence *= target_prob
                
            branches.append({
                "branch_id": i + 1,
                "origin_state": current_app,
                "simulated_sequence": simulated_path,
                "path_confidence": round(path_confidence, 4)
            })
            
        # Sort branches by most probable timeline
        branches = sorted(branches, key=lambda x: x["path_confidence"], reverse=True)
        return branches

