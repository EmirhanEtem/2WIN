import time
import logging
from core.event_bus import EventBus, Event
from .base import BaseCollector

try:
    from pynput import mouse, keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    logging.warning("pynput not installed. InputTimingCollector will fallback to mock timing or stay idle.")

logger = logging.getLogger(__name__)

class InputTimingCollector(BaseCollector):
    """
    Monitors keyboard and mouse activity for temporal patterns (no keylogging).
    Detects activity bursts, idle time, and typing cadence signatures.
    """
    def __init__(self, event_bus: EventBus, interval_seconds: float = 5.0):
        super().__init__(event_bus, interval_seconds)
        self.key_strokes_since_last = 0
        self.mouse_moves_since_last = 0
        self.mouse_clicks_since_last = 0
        
        self.mouse_listener = None
        self.keyboard_listener = None

    def on_start(self) -> None:
        if not PYNPUT_AVAILABLE:
            return

        def on_press(key):
            self.key_strokes_since_last += 1

        def on_move(x, y):
            self.mouse_moves_since_last += 1

        def on_click(x, y, button, pressed):
            if pressed:
                self.mouse_clicks_since_last += 1

        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
        
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def on_stop(self) -> None:
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

    def collect(self) -> None:
        # Publish an event summarizing the activity over the last interval
        if self.key_strokes_since_last > 0 or self.mouse_moves_since_last > 0:
            event = Event(
                event_type="InputActivityEvent",
                payload={
                    "keystrokes": self.key_strokes_since_last,
                    "mouse_moves": self.mouse_moves_since_last,
                    "mouse_clicks": self.mouse_clicks_since_last,
                    "interval": self.interval_seconds
                }
            )
            self.event_bus.publish_sync(event)

        # Reset counters
        self.key_strokes_since_last = 0
        self.mouse_moves_since_last = 0
        self.mouse_clicks_since_last = 0
