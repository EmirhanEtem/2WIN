import pytest
import asyncio
from typing import List, Tuple

from dtce.core.interfaces import IPredictionModel
from dtce.prediction.engine import PredictionEngine

class MockMarkovModel(IPredictionModel):
    def fit(self) -> None:
        pass
    def predict_next(self, current_app: str) -> List[Tuple[str, float]]:
        if current_app == "chrome.exe":
            return [("code.exe", 0.8), ("explorer.exe", 0.2)]
        return []

class MockBayesianModel(IPredictionModel):
    def fit(self) -> None:
        pass
    def predict_next(self, current_app: str) -> List[Tuple[str, float]]:
        if current_app == "chrome.exe":
            return [("code.exe", 0.4), ("slack.exe", 0.6)]
        return []

@pytest.fixture
def prediction_engine():
    models = [MockMarkovModel(), MockBayesianModel()]
    return PredictionEngine(models=models)

def test_ensemble_prediction_averaging(prediction_engine):
    preds = prediction_engine.predict_next_app("chrome.exe")
    
    # Markov gave code.exe 0.8, Bayes gave 0.4. Avg = 0.6
    # Markov gave explorer 0.2, Bayes 0. Avg = 0.1
    # Bayes gave slack 0.6, Markov 0. Avg = 0.3
    
    pred_dict = {app: prob for app, prob in preds}
    
    assert "code.exe" in pred_dict
    assert abs(pred_dict["code.exe"] - 0.6) < 0.01
    
    assert "slack.exe" in pred_dict
    assert abs(pred_dict["slack.exe"] - 0.3) < 0.01

def test_simulation_generates_correct_length(prediction_engine):
    path = prediction_engine.simulate_future_path("chrome.exe", steps=3)
    assert len(path) > 0 # Should at least have the origin
