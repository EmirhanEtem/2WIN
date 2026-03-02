import threading
import time
import logging
from abc import ABC, abstractmethod
from core.event_bus import EventBus

logger = logging.getLogger(__name__)

class BaseCollector(ABC):
    """
    Abstract base class for all background collectors.
    Collectors run in their own thread and push events to the central EventBus.
    """
    def __init__(self, event_bus: EventBus, interval_seconds: float = 1.0):
        self.event_bus = event_bus
        self.interval_seconds = interval_seconds
        self._running = False
        self._thread = None

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_loop, daemon=True, name=self.__class__.__name__)
            self._thread.start()
            logger.info(f"Started collector: {self.__class__.__name__}")

    def stop(self) -> None:
        if self._running:
            self._running = False
            if self._thread:
                self._thread.join(timeout=2.0)
            logger.info(f"Stopped collector: {self.__class__.__name__}")

    def _run_loop(self) -> None:
        self.on_start()
        while self._running:
            try:
                self.collect()
            except Exception as e:
                logger.error(f"Error in {self.__class__.__name__} loop: {e}")
            time.sleep(self.interval_seconds)
        self.on_stop()

    def on_start(self) -> None:
        """Optional hook to setup resources before collection loop starts."""
        pass

    def on_stop(self) -> None:
        """Optional hook to cleanup resources after collection loop stops."""
        pass

    @abstractmethod
    def collect(self) -> None:
        """
        Implemented by subclasses.
        Should gather data and call self.event_bus.publish_sync(event).
        """
        pass
