# Implementation Plan: AI-Powered Calendar and Reminder Management

**Branch**: `001-ai-calendar-reminder` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-calendar-reminder/spec.md`

## Summary

Build an Alfred workflow that uses AI to parse natural language text (English/Chinese) and automatically create calendar events and reminders in macOS system apps. Users configure their AI service (OpenAI/Anthropic/custom), input text via Alfred, and the workflow handles parsing, validation, and system integration. Includes tracking and batch deletion of created items.

**Technical Approach**: Python 3.11-based Alfred workflow using PyObjC for EventKit access, alfred-workflow for UI, keyring for credentials, and official AI client libraries (openai/anthropic) with httpx for flexible endpoint support.

## Technical Context

**Language/Version**: Python 3.11 (Universal2 binary for Apple Silicon + Intel compatibility)
**Primary Dependencies**:
- `pyobjc-framework-EventKit` (macOS Calendar/Reminders access)
- `alfred-workflow` (Alfred JSON feedback and workflow helpers)
- `keyring` (secure credential storage in macOS Keychain)
- `openai` (primary AI client, OpenAI-compatible format)
- `anthropic` (optional, for Anthropic Claude)
- `httpx` (custom endpoint support)

**Storage**: JSON file for Created Item Tracker (`~/.alfred-reminder-alf/tracking.json`)
**Testing**: pytest for unit tests, manual workflow testing via Alfred
**Target Platform**: macOS 11+ (Big Sur and later)
**Project Type**: Single Python project (Alfred workflow)
**Performance Goals**:
- Text parsing + item creation in <10 seconds end-to-end
- AI API calls with 30-second timeout
- Handle text inputs up to 500 words

**Constraints**:
- Must work within Alfred's Script Filter environment
- Requires macOS Calendar/Reminders permissions
- AI service dependency (online-only for parsing)
- No background processing (Alfred workflow limitations)

**Scale/Scope**:
- Single user per installation
- ~2000 LOC total
- 5-10 Python modules
- Support unlimited created items tracking

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Alfred Workflow Integration ✅ PASS

- Using `alfred-workflow` library for JSON feedback format
- Script Filter will accept input from Alfred's standard mechanisms
- Configuration via Alfred's workflow environment variables
- Clear feedback for all operations (success/error/progress)

**Compliance**: Full adherence to Alfred's patterns and JSON format.

### II. AI Processing Pipeline ✅ PASS

- Structured prompts for extracting CalendarEvent and Reminder entities
- Data validation layer before EventKit API calls
- Ambiguous parsing prompts user for confirmation via Alfred feedback
- Multi-language support (EN/CN) via AI model capabilities
- Error handling for AI service unavailability

**Compliance**: Robust parsing with validation and user confirmation workflow.

### III. macOS/iOS System Integration ✅ PASS

- Using official EventKit framework via PyObjC
- Permission request handled by PyObjC + macOS system dialogs
- Graceful error messages for permission denied scenarios
- Default calendar/reminder list detection via EventKit APIs
- iCloud sync handled automatically by system

**Compliance**: Direct system API usage, proper permission handling.

### IV. Error Handling & User Experience ✅ PASS

- Comprehensive error messages for all failure modes:
  - Missing/invalid API credentials
  - Calendar/Reminders permission denied
  - AI parsing failures (no items found)
  - Network/API service errors
  - EventKit API errors
- No silent failures - all outcomes shown via Alfred feedback
- Input validation → AI parsing → data validation → API calls pipeline
- Partial failure handling (e.g., 3 of 5 items created successfully)

**Compliance**: Explicit error handling at every integration boundary.

### V. Simplicity & Maintainability ✅ PASS

- Minimal dependencies (6 total, all well-maintained)
- Direct API calls to EventKit and AI services (no ORMs or heavy frameworks)
- Simple JSON file for tracking data
- Configuration via keyring + Alfred environment variables
- Modular structure: input → AI → validation → EventKit → feedback
- Standard library used for JSON, datetime, pathlib operations

**Compliance**: Straightforward architecture with focused modules.

### Summary

All 5 core principles are satisfied. No constitution violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-calendar-reminder/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions and rationale
├── data-model.md        # Phase 1: Data structures and schemas
├── quickstart.md        # Phase 1: User installation and usage guide
├── contracts/           # Phase 1: API contract definitions
│   ├── alfred-feedback.json    # Alfred JSON feedback format examples
│   ├── ai-prompt.md            # AI prompt templates
│   └── ai-response.json        # Expected AI response format
└── tasks.md             # Phase 2: Implementation tasks (created by /speckit.tasks)
```

### Source Code (repository root)

```text
reminder-alf/                    # Alfred workflow root
├── info.plist                   # Alfred workflow metadata
├── icon.png                     # Workflow icon
├── src/
│   ├── __init__.py
│   ├── main.py                  # Alfred script entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── calendar_event.py   # CalendarEvent data class
│   │   ├── reminder.py          # Reminder data class
│   │   ├── ai_config.py         # AIConfiguration data class
│   │   ├── parse_result.py      # ParseResult from AI
│   │   └── tracker.py           # CreatedItemTracker
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_client.py         # AI service abstraction (OpenAI/Anthropic/custom)
│   │   ├── eventkit_bridge.py   # PyObjC EventKit wrapper
│   │   ├── config_manager.py    # Keyring + env var config
│   │   └── tracker_service.py   # Tracking data persistence
│   ├── workflow/
│   │   ├── __init__.py
│   │   ├── input_handler.py     # Parse Alfred input
│   │   ├── feedback_builder.py  # Generate Alfred JSON feedback
│   │   └── command_router.py    # Route commands (create/delete/config)
│   └── utils/
│       ├── __init__.py
│       ├── date_parser.py       # Date/time normalization helpers
│       ├── validators.py        # Data validation
│       └── logger.py            # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_ai_client.py
│   │   ├── test_validators.py
│   │   └── test_date_parser.py
│   ├── integration/
│   │   ├── test_eventkit_bridge.py  # Requires test calendar
│   │   └── test_tracker_service.py
│   └── fixtures/
│       ├── ai_responses.json
│       └── test_inputs.txt
├── pyproject.toml               # Dependencies and project metadata
├── requirements.txt             # Generated from pyproject.toml
├── README.md                    # Project overview
└── .gitignore
```

**Structure Decision**: Single Python project structure is optimal for an Alfred workflow. The workflow is self-contained, has no frontend/backend split, and follows Alfred's standard workflow directory layout. The `src/` directory contains all workflow logic, organized into models (data structures), services (external integrations), workflow (Alfred-specific), and utils (helpers). Tests are separated by type (unit/integration) and fixtures support reproducible testing.

## Complexity Tracking

No violations - this section is empty as all constitution principles are satisfied.
