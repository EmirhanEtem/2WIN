import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from .models import Base, DBEvent
from typing import List
from core.event_bus import Event
from core.interfaces import IEventRepository

logger = logging.getLogger(__name__)

class AsyncEventRepository(IEventRepository):
    """
    Fully asynchronous SQLAlchemy repository using aiosqlite.
    Prevents background storage I/O from blocking the main event loop.
    """
    def __init__(self, db_path: str = "sqlite+aiosqlite:///dtce_history_v2.db"):
        self.engine = create_async_engine(db_path, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def initialize_db(self) -> None:
        """Create database tables asynchronously."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.debug("Database initialized.")

    async def save_event(self, event: Event) -> None:
        """Asynchronously save a real-time event into the database."""
        db_event = DBEvent(
            id=event.id,
            event_type=event.type,
            timestamp=event.timestamp,
            payload=event.payload
        )
        async with self.async_session() as session:
            try:
                session.add(db_event)
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to async save event {event.id}: {e}")

    async def get_recent_events(self, limit: int = 100) -> List[DBEvent]:
        async with self.async_session() as session:
            result = await session.execute(
                select(DBEvent).order_by(DBEvent.timestamp.desc()).limit(limit)
            )
            return list(result.scalars().all())
            
    async def get_events_by_type(self, event_type: str, limit: int = 1000) -> List[DBEvent]:
        async with self.async_session() as session:
            result = await session.execute(
                select(DBEvent)
                .filter(DBEvent.event_type == event_type)
                .order_by(DBEvent.timestamp.asc())
                .limit(limit)
            )
            return list(result.scalars().all())

