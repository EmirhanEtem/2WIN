import time
import logging
from typing import Optional, Dict, Any
from core.event_bus import EventBus, Event
from .base import BaseCollector

try:
    import win32gui
    import win32process
    import psutil
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    logging.warning("win32gui or psutil not installed. WindowTracker will not function correctly on non-windows or missing dependencies.")

logger = logging.getLogger(__name__)

class WindowTrackerCollector(BaseCollector):
    """
    Monitors the currently active window and publishes WindowChangedEvents
    when the focus shifts to a new application or window title.
    """
    def __init__(self, event_bus: EventBus, interval_seconds: float = 0.5):
        super().__init__(event_bus, interval_seconds)
        self.last_window_title: Optional[str] = None
        self.last_app_name: Optional[str] = None

    def get_active_window_info(self) -> Dict[str, Any]:
        if not WIN32_AVAILABLE:
            return {"app_name": "unknown", "window_title": "unknown", "pid": None}

        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return {"app_name": "unknown", "window_title": "idle", "pid": None}

            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            app_name = "unknown"
            if pid > 0:
                try:
                    process = psutil.Process(pid)
                    app_name = process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return {"app_name": app_name, "window_title": window_title, "pid": pid}
        except Exception as e:
            logger.debug(f"Failed to get active window info: {e}")
            return {"app_name": "error", "window_title": "error", "pid": None}

    def collect(self) -> None:
        info = self.get_active_window_info()
        title = info["window_title"]
        app = info["app_name"]

        # Only publish an event if the active window actually changed
        if title != self.last_window_title or app != self.last_app_name:
            self.last_window_title = title
            self.last_app_name = app

            event = Event(
                event_type="WindowChangedEvent",
                payload={
                    "app_name": app,
                    "window_title": title,
                    "pid": info["pid"]
                }
            )
            self.event_bus.publish_sync(event)
