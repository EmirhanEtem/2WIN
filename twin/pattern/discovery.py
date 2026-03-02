import logging
from typing import List, Dict, Any
from storage.repository import AsyncEventRepository
from storage.models import DBEvent
from collections import defaultdict

logger = logging.getLogger(__name__)

class PatternDiscoveryEngine:
    """
    Analyzes historical event data to discover recurring behavioral patterns.
    Examples: App transition sequences, time-of-day access habits.
    """
    def __init__(self, repository: AsyncEventRepository):
        self.repository = repository

    async def discover_app_transitions(self, limit: int = 1000) -> Dict[str, Dict[str, int]]:
        """
        Calculates the transition frequencies between applications.
        Returns a dict of source_app -> {target_app: frequency}.
        """
        events = await self.repository.get_events_by_type("WindowChangedEvent", limit=limit)
        
        transitions = defaultdict(lambda: defaultdict(int))
        
        last_app = None
        for evt in events:
            current_app = evt.payload.get("app_name")
            if current_app and last_app and current_app != last_app:
                transitions[last_app][current_app] += 1
            last_app = current_app
            
        return {k: dict(v) for k, v in transitions.items()}

    async def discover_time_habits(self, limit: int = 1000) -> Dict[str, List[int]]:
        """
        Groups most used applications by the hour of the day to identify recurring temporal habits.
        Returns a dict of app_name -> list of hours it is frequently used.
        """
        events = await self.repository.get_events_by_type("WindowChangedEvent", limit=limit)
        
        app_hours = defaultdict(list)
        for evt in events:
            app_name = evt.payload.get("app_name")
            if app_name:
                hour = evt.timestamp.hour
                app_hours[app_name].append(hour)
                
        # Simplify by just returning the most common hour clusters
        habit_summary = {}
        for app, hours in app_hours.items():
            if len(hours) > 0:
                # Mode or top N hours
                from collections import Counter
                top_hours = [str(h) for h, count in Counter(hours).most_common(3)]
                habit_summary[app] = top_hours
                
        return habit_summary

