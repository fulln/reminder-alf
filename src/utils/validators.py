"""
Validation utilities for reminder-alf.
"""
from datetime import datetime
from typing import Optional


def validate_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate title string.

    Returns:
        (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title cannot be empty"
    if len(title) > 500:
        return False, "Title too long (max 500 characters)"
    return True, None


def validate_datetime(dt: datetime, allow_past: bool = False) -> tuple[bool, Optional[str]]:
    """
    Validate datetime.

    Args:
        dt: Datetime to validate
        allow_past: Whether to allow past dates

    Returns:
        (is_valid, error_message)
    """
    if not allow_past and dt < datetime.now():
        return False, "Date/time cannot be in the past"
    # Check reasonable future date (within 10 years)
    far_future = datetime.now().replace(year=datetime.now().year + 10)
    if dt > far_future:
        return False, "Date/time too far in future (max 10 years)"
    return True, None


def validate_datetime_range(
    start: datetime, end: datetime
) -> tuple[bool, Optional[str]]:
    """
    Validate datetime range.

    Returns:
        (is_valid, error_message)
    """
    if end <= start:
        return False, "End time must be after start time"
    # Check duration is reasonable (max 7 days for single event)
    duration = (end - start).total_seconds()
    if duration > 7 * 24 * 3600:
        return False, "Event duration exceeds 7 days"
    return True, None


def validate_priority(priority: int) -> tuple[bool, Optional[str]]:
    """
    Validate priority level.

    Returns:
        (is_valid, error_message)
    """
    if priority not in [0, 1, 2, 3]:
        return False, "Priority must be 0 (None), 1 (Low), 2 (Medium), or 3 (High)"
    return True, None


def validate_url(url: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate URL if provided.

    Returns:
        (is_valid, error_message)
    """
    if url is None or not url.strip():
        return True, None

    # Basic URL validation
    if not (url.startswith("http://") or url.startswith("https://")):
        return False, "URL must start with http:// or https://"

    if len(url) > 2000:
        return False, "URL too long (max 2000 characters)"

    return True, None
