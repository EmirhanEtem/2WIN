from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from core.event_bus import Event

class IEventRepository(ABC):
    """
    Interface for the historical event repository.
    Allows decoupling from SQLAlchemy and enables easy mocking for tests.
    """
    
    @abstractmethod
    async def save_event(self, event: Event) -> None:
        pass
        
    @abstractmethod
    async def get_recent_events(self, limit: int = 100) -> List[Any]:
        pass

    @abstractmethod
    async def get_events_by_type(self, event_type: str, limit: int = 1000) -> List[Any]:
        pass


class IPredictionModel(ABC):
    """
    Interface for any prediction model (Markov, Bayesian, Neural Net).
    """
    
    @abstractmethod
    def fit(self) -> None:
        """Train or update the model based on the graph or history."""
        pass

    @abstractmethod
    def predict_next(self, current_state: str) -> List[Tuple[str, float]]:
        """
        Predict the probabilities of the next states.
        Returns a list of tuples (state_id, probability).
        """
        pass
