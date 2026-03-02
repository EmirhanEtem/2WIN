import asyncio
from typing import Callable, Dict, List, Any, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class Event:
    """Base class for all system events."""
    def __init__(self, event_type: str, payload: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.type = event_type
        self.payload = payload
        self.timestamp = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Event {self.type} @ {self.timestamp}>"

class EventBus:
    """
    Central asynchronous event bus for the DTCE architecture.
    Implements the Observer pattern for loose coupling.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], Any]]] = {}
        self._loop = asyncio.get_event_loop()
        self._queue = asyncio.Queue()
        self._running = False
        self._worker_task: Optional[asyncio.Task] = None

    def subscribe(self, event_type: str, callback: Callable[[Event], Any]) -> None:
        """Subscribe a callback to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed {callback.__name__} to {event_type}")

    def publish_sync(self, event: Event) -> None:
        """Convenience method for background threads to safely put events onto the async bus."""
        if self._running:
            self._loop.call_soon_threadsafe(self._queue.put_nowait, event)
            logger.debug(f"Published sync event: {event.type}")

    async def publish(self, event: Event) -> None:
        """Publish an event to the bus asynchronously."""
        await self._queue.put(event)
        logger.debug(f"Published async event: {event.type}")

    async def _process_events(self) -> None:
        """Background worker that routes events to subscribers."""
        while self._running:
            try:
                event = await self._queue.get()
                subscribers = self._subscribers.get(event.type, [])
                
                # Create a task for each subscriber to handle the event concurrently
                for sub in subscribers:
                    if asyncio.iscoroutinefunction(sub):
                        asyncio.create_task(sub(event))
                    else:
                        # For synchronous callbacks, run in executor to avoid blocking the event loop
                        self._loop.run_in_executor(None, sub, event)
                
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing event {event}: {e}")

    async def start(self) -> None:
        """Start the event bus background worker."""
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._process_events())
            logger.info("Event Bus started")

    async def stop(self) -> None:
        """Stop the event bus and wait for remaining events to be processed."""
        if self._running:
            self._running = False
            if self._worker_task:
                self._worker_task.cancel()
                try:
                    await self._worker_task
                except asyncio.CancelledError:
                    pass
            logger.info("Event Bus stopped")
