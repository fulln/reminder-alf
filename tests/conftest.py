"""
Pytest configuration and fixtures for reminder-alf tests.
"""
import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_ai_responses(fixtures_dir: Path) -> dict:
    """Load sample AI responses from fixtures."""
    with open(fixtures_dir / "ai_responses.json") as f:
        return json.load(f)


@pytest.fixture
def sample_inputs(fixtures_dir: Path) -> list[str]:
    """Load sample input texts from fixtures."""
    with open(fixtures_dir / "test_inputs.txt") as f:
        return [line.strip() for line in f if line.strip()]


@pytest.fixture
def mock_current_time() -> datetime:
    """Return fixed datetime for testing."""
    return datetime(2026, 1, 26, 10, 0, 0)


@pytest.fixture
def temp_tracking_file(tmp_path: Path) -> Path:
    """Create temporary tracking file for tests."""
    tracking_file = tmp_path / "tracking.json"
    tracking_file.write_text('{"items": []}')
    return tracking_file
