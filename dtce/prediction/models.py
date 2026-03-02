import logging
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import random

from core.interfaces import IPredictionModel
from cognitive_map.graph import CognitiveGraph
from pattern.discovery import PatternDiscoveryEngine

logger = logging.getLogger(__name__)

class MarkovPredictionModel(IPredictionModel):
    """
    Forecasts future user behavior using a probabilistic Markov chain model based on the Cognitive Graph.
    """
    def __init__(self, cognitive_graph: CognitiveGraph, pattern_engine: PatternDiscoveryEngine):
        self.graph = cognitive_graph
        self.pattern_engine = pattern_engine

    def fit(self) -> None:
        """In a pure Markov system based on NetworkX edges, the graph IS the trained model."""
        pass

    def predict_next(self, current_app: str) -> List[Tuple[str, float]]:
        """
        Predicts the next application the user will switch to, given the current application.
        Returns a list of tuples (app_name, confidence).
        """
        if not self.graph.graph.has_node(current_app):
            # Fallback to general probability if we don't have this node in graph yet
            return []
            
        probable_nodes = self.graph.get_probable_next_nodes(current_app)
        
        # Normalize weights to probabilities between 0 and 1
        total_weight = sum([w for _, w in probable_nodes])
        if total_weight == 0:
            return []
            
        normalized_probabilities = [(node, weight / total_weight) for node, weight in probable_nodes]
        return normalized_probabilities


class BayesianPredictionModel(IPredictionModel):
    """
    A pseudo-Bayesian model exploring probability given prior temporal constraints.
    P(App B | App A AND Time is Morning)
    """
    def __init__(self, pattern_engine: PatternDiscoveryEngine):
        self.pattern_engine = pattern_engine
        self._prior_global_counts = defaultdict(int)
        self._total_events = 0

    def fit(self) -> None:
        # Complex Bayesian training logic would go here
        # E.g. awaiting self.pattern_engine.discover_app_transitions() to calculate global priors
        pass
        
    def predict_next(self, current_app: str) -> List[Tuple[str, float]]:
        # Simplified mock up for v2 extensibility showing Bayesian logic structure
        return [("chrome.exe", 0.6), ("explorer.exe", 0.4)]
