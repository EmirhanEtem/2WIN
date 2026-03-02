import logging
import hashlib
from datetime import datetime
from typing import Dict, Any

from storage.repository import AsyncEventRepository

logger = logging.getLogger(__name__)

class IdentityRecognitionEngine:
    """
    Analyzes user behavior to create a unique behavioral biometric fingerprint.
    Can be used to verify the operator is the true owner of the digital twin.
    """
    def __init__(self, repository: AsyncEventRepository):
        self.repository = repository
        self._current_fingerprint = "Unknown"
        self._confidence = 0.0

    async def generate_fingerprint(self) -> Dict[str, Any]:
        """
        Aggregates recent typing cadence, idle behavior, and application sequences
        to form a hash fingerprint.
        """
        input_events = await self.repository.get_events_by_type("InputActivityEvent", limit=5000)
        
        total_keystrokes = 0
        total_moves = 0
        total_intervals = 0
        
        for evt in input_events:
            total_keystrokes += evt.payload.get("keystrokes", 0)
            total_moves += evt.payload.get("mouse_moves", 0)
            total_intervals += 1
            
        if total_intervals == 0:
            return {"hash": "InsufficientData", "confidence": 0.0, "typing_speed": 0, "mouse_usage": 0}
            
        avg_typing_speed = total_keystrokes / total_intervals
        avg_mouse_usage = total_moves / total_intervals
        
        # Incorporate app habit clustering for a more unique footprint
        window_events = await self.repository.get_events_by_type("WindowChangedEvent", limit=100)
        recent_apps = list(set([evt.payload.get("app_name", "unknown") for evt in window_events]))
        recent_apps.sort()
        
        fingerprint_data = {
            "avg_typing_speed": round(avg_typing_speed, 2),
            "avg_mouse_usage": round(avg_mouse_usage, 2),
            "top_apps": recent_apps,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Hash the feature set to create an identity signature
        signature_string = f"{avg_typing_speed:.1f}_{avg_mouse_usage:.1f}_{'_'.join(recent_apps)}"
        identity_hash = hashlib.sha256(signature_string.encode()).hexdigest()[:16]
        
        fingerprint_data["hash"] = identity_hash
        # Assume confidence grows as we collect more intervals up to a cap
        fingerprint_data["confidence"] = min(total_intervals / 1000.0, 0.99)
        
        self._current_fingerprint = identity_hash
        self._confidence = fingerprint_data["confidence"]
        
        logger.info(f"Generated new identity fingerprint: {identity_hash} (Confidence: {self._confidence})")
        return fingerprint_data

