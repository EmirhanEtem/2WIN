import logging
from typing import List, Tuple
from core.interfaces import IPredictionModel
import random

logger = logging.getLogger(__name__)

class PredictionEngine:
    """
    Main orchestrator that uses multiple underlying models (Markov, Bayesian)
    to predict future user states.
    """
    def __init__(self, models: List[IPredictionModel]):
        self.models = models

    def predict_next_app(self, current_app: str) -> List[Tuple[str, float]]:
        """
        Queries all models and acts as an ensemble voting system.
        For now, simply averages probabilities from all active models.
        """
        aggregated_probs = {}
        total_models = len(self.models)
        
        if total_models == 0:
            return []

        for model in self.models:
            predictions = model.predict_next(current_app)
            for app, prob in predictions:
                aggregated_probs[app] = aggregated_probs.get(app, 0.0) + (prob / total_models)

        # Sort by highest probability
        sorted_preds = sorted(aggregated_probs.items(), key=lambda x: x[1], reverse=True)
        return sorted_preds[:5]

    def simulate_future_path(self, current_app: str, steps: int = 5) -> List[str]:
        """
        Generates a simulated probabilistic timeline starting from the current app.
        """
        path = [current_app]
        curr = current_app
        
        for _ in range(steps):
            predictions = self.predict_next_app(curr)
            if not predictions:
                break
                
            # Probabilistic random choice based on weights
            apps, weights = zip(*predictions)
            next_app = random.choices(apps, weights=weights, k=1)[0]
            path.append(next_app)
            curr = next_app
            
        return path
