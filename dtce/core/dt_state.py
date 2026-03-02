from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class WindowState:
    app_name: str
    window_title: str
    start_time: datetime
    process_id: Optional[int] = None

@dataclass
class ActivityState:
    is_active: bool
    last_keyboard_activity: Optional[datetime] = None
    last_mouse_activity: Optional[datetime] = None
    idle_time_seconds: float = 0.0

@dataclass
class DTState:
    """
    Represents the real-time aggregated state of the user's digital presence.
    """
    current_window: Optional[WindowState] = None
    activity: ActivityState = field(default_factory=lambda: ActivityState(is_active=True))
    context_tags: Dict[str, Any] = field(default_factory=dict)
    
    def update_window(self, app_name: str, window_title: str, pid: Optional[int] = None) -> None:
        self.current_window = WindowState(
            app_name=app_name,
            window_title=window_title,
            start_time=datetime.utcnow(),
            process_id=pid
        )

    def mark_active(self) -> None:
        self.activity.is_active = True
        self.activity.idle_time_seconds = 0.0
