"""
TrackerService for persistent tracking of created items.
"""
from pathlib import Path
from typing import Optional
from ..models.tracker import CreatedItemTracker, CreatedItem
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TrackerService:
    """Service for managing created item tracking."""

    DEFAULT_STORAGE_PATH = (
        Path.home()
        / "Library/Application Support/Alfred/Workflow Data/com.reminder-alf/tracking.json"
    )

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize TrackerService.

        Args:
            storage_path: Path to tracking file (defaults to Alfred data dir)
        """
        if storage_path is None:
            storage_path = self.DEFAULT_STORAGE_PATH

        self.tracker = CreatedItemTracker(storage_path)
        logger.info(f"TrackerService initialized with storage: {storage_path}")

    def track_created_item(self, item: CreatedItem) -> bool:
        """
        Track a newly created item.

        Args:
            item: CreatedItem to track

        Returns:
            True if successfully tracked
        """
        try:
            self.tracker.add(item)
            logger.info(f"Tracked {item.item_type}: {item.title} (ID: {item.item_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to track item: {e}")
            return False

    def get_all_tracked_items(self):
        """Get all tracked items."""
        return self.tracker.get_all()

    def get_recent_items(self, limit: int = 10):
        """Get recent tracked items."""
        return self.tracker.get_recent(limit)

    def remove_tracked_item(self, item_id: str) -> bool:
        """
        Remove item from tracking.

        Args:
            item_id: EventKit identifier

        Returns:
            True if found and removed
        """
        return self.tracker.remove(item_id)

    def clear_all_tracked(self) -> int:
        """
        Clear all tracked items.

        Returns:
            Number of items removed
        """
        count = self.tracker.clear_all()
        logger.info(f"Cleared {count} tracked items")
        return count

    def cleanup_old_items(self, days: int = 7) -> int:
        """
        Remove items older than specified days.

        Args:
            days: Age threshold in days

        Returns:
            Number of items removed
        """
        count = self.tracker.clear_old(days)
        if count > 0:
            logger.info(f"Cleaned up {count} items older than {days} days")
        return count
