---

description: "Implementation tasks for AI-Powered Calendar and Reminder workflow"

---

# Tasks: AI-Powered Calendar and Reminder Management

**Input**: Design documents from `/specs/001-ai-calendar-reminder/`
**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅)

**Tests**: Tests are OPTIONAL - included here for TDD approach (write tests first, fail, then implement)

**Organization**: Tasks grouped by user story to enable independent implementation, testing, and deployment of each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3) showing which story this task belongs to
- **File paths**: Exact locations where code should be written

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Python environment setup

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python 3.11 project with pyproject.toml and dependencies in `pyproject.toml`
- [ ] T003 [P] Set up linting with ruff configuration in `.ruff.toml`
- [ ] T004 [P] Set up code formatting with black configuration in `pyproject.toml`
- [ ] T005 [P] Create pytest configuration in `pyproject.toml` and `tests/conftest.py`
- [ ] T006 Create main Alfred workflow entry point script in `src/main.py` (stub)
- [ ] T007 Create `src/__init__.py` package initialization
- [ ] T008 Create `.gitignore` with Python, Alfred, and macOS-specific ignores

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story can begin

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Configuration & Secrets Management

- [ ] T009 [P] Implement AIConfiguration data class with provider/model/timeout in `src/models/ai_config.py`
- [ ] T010 [P] Implement ConfigManager service for keyring + env var integration in `src/services/config_manager.py`
- [ ] T011 [P] Implement keyring setup and credential retrieval logic in `src/services/config_manager.py`
- [ ] T012 Create configuration initialization workflow in `src/workflow/config_init.py` (prompts user for API key)

### Data Models & Validation

- [ ] T013 [P] Create CalendarEvent dataclass with validation in `src/models/calendar_event.py`
- [ ] T014 [P] Create Reminder dataclass with validation in `src/models/reminder.py`
- [ ] T015 [P] Create ParseResult dataclass (AI parsing output) in `src/models/parse_result.py`
- [ ] T016 [P] Create CreatedItemTracker classes in `src/models/tracker.py` (tracks created items for deletion)
- [ ] T017 [P] Implement validators module for data validation in `src/utils/validators.py`
- [ ] T018 Create logger configuration in `src/utils/logger.py`

### EventKit System Integration

- [ ] T019 [P] Implement EventKitBridge wrapper class for Calendar operations in `src/services/eventkit_bridge.py`
- [ ] T020 [P] Implement EventKit Reminders operations in `src/services/eventkit_bridge.py`
- [ ] T021 Implement permission request and handling in `src/services/eventkit_bridge.py`
- [ ] T022 Add error handling for permission denied scenarios in `src/services/eventkit_bridge.py`

### AI Service Integration

- [ ] T023 [P] Implement AIClient abstraction class in `src/services/ai_client.py` (interface)
- [ ] T024 [P] Implement OpenAI client provider in `src/services/ai_client.py` (with httpx fallback)
- [ ] T025 [P] Implement Anthropic client provider in `src/services/ai_client.py`
- [ ] T026 Add prompt template construction in `src/services/ai_client.py` (use contracts/ai-prompt.md)
- [ ] T027 Add response parsing and validation in `src/services/ai_client.py` (validate against contracts/ai-response.json)
- [ ] T028 Add error handling for API failures, timeouts, rate limits in `src/services/ai_client.py`

### Tracking & Persistence

- [ ] T029 Implement TrackerService for JSON persistence in `src/services/tracker_service.py`
- [ ] T030 Add atomic write operations (temp file + rename) in `src/services/tracker_service.py`
- [ ] T031 Create tracking data directory setup in `src/services/tracker_service.py`

### Alfred Workflow Integration

- [ ] T032 [P] Implement InputHandler to parse Alfred input (clipboard, text) in `src/workflow/input_handler.py`
- [ ] T033 [P] Implement FeedbackBuilder for Alfred JSON output in `src/workflow/feedback_builder.py` (use contracts/alfred-feedback.json)
- [ ] T034 Implement CommandRouter for workflow command routing in `src/workflow/command_router.py`
- [ ] T035 Add error display formatting in `src/workflow/feedback_builder.py`
- [ ] T036 Add loading/progress indicators in `src/workflow/feedback_builder.py`

### Test Fixtures

- [ ] T037 Create test fixtures for AI responses in `tests/fixtures/ai_responses.json`
- [ ] T038 Create test fixtures for sample inputs in `tests/fixtures/test_inputs.txt`
- [ ] T039 Create pytest conftest with fixtures in `tests/conftest.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - AI Text Recognition and System Integration (Priority: P1) 🎯 MVP

**Goal**: Parse natural language text via AI and automatically create calendar events and reminders in macOS

**Independent Test**: Paste "明天下午3点开会" → workflow parses → calendar event created in Calendar app with correct date/time

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL)

- [ ] T040 [P] [US1] Unit test for CalendarEvent model validation in `tests/unit/test_calendar_event.py`
- [ ] T041 [P] [US1] Unit test for Reminder model validation in `tests/unit/test_reminder.py`
- [ ] T042 [P] [US1] Unit test for ParseResult model in `tests/unit/test_parse_result.py`
- [ ] T043 [P] [US1] Unit test for date_parser utility (relative dates) in `tests/unit/test_date_parser.py`
- [ ] T044 [P] [US1] Unit test for validators (title, datetime) in `tests/unit/test_validators.py`
- [ ] T045 [P] [US1] Contract test for AI response parsing in `tests/contract/test_ai_parsing.py`
- [ ] T046 [P] [US1] Integration test for EventKit event creation in `tests/integration/test_eventkit_create_event.py`
- [ ] T047 [P] [US1] Integration test for EventKit reminder creation in `tests/integration/test_eventkit_create_reminder.py`
- [ ] T048 [US1] Integration test for full workflow (input → AI → EventKit) in `tests/integration/test_workflow_e2e.py`

### Implementation for User Story 1

- [ ] T049 [P] [US1] Create date_parser utility for relative dates in `src/utils/date_parser.py`
- [ ] T050 [P] [US1] Implement ParseResult to CalendarEvent/Reminder conversion in `src/models/parse_result.py`
- [ ] T051 [US1] Implement AIClient.parse_text() method for AI parsing in `src/services/ai_client.py`
- [ ] T052 [P] [US1] Implement EventKitBridge.create_calendar_event() in `src/services/eventkit_bridge.py`
- [ ] T053 [P] [US1] Implement EventKitBridge.create_reminder() in `src/services/eventkit_bridge.py`
- [ ] T054 [US1] Create EventCreationService orchestrating AI → validation → EventKit in `src/services/event_creation_service.py`
- [ ] T055 [US1] Implement TrackerService.track_created_item() in `src/services/tracker_service.py`
- [ ] T056 [US1] Create workflow command handler for "create" in `src/workflow/command_router.py`
- [ ] T057 [US1] Add ParseResult validation before creation in `src/services/event_creation_service.py`
- [ ] T058 [US1] Implement ambiguity detection and user confirmation flow in `src/workflow/feedback_builder.py`
- [ ] T059 [US1] Implement error handling and clear error messages for: missing AI config, permission denied, parse failure, API error in `src/workflow/feedback_builder.py`
- [ ] T060 [US1] Implement Alfred JSON feedback for created items (success, errors, ambiguities) in `src/workflow/feedback_builder.py`
- [ ] T061 [US1] Create main.py entry point routing input → parser → EventKit in `src/main.py`
- [ ] T062 [US1] Test with sample inputs (Chinese, English, mixed) in Alfred workflow

**Checkpoint**: User Story 1 is fully functional and independently testable

---

## Phase 4: User Story 2 - AI Configuration Management (Priority: P2)

**Goal**: Allow users to configure AI service (OpenAI/Anthropic/custom) and securely store credentials

**Independent Test**: Configure API key → keyring stores securely → test API call succeeds with configured endpoint

### Tests for User Story 2 (TDD)

- [ ] T063 [P] [US2] Unit test for ConfigManager keyring integration in `tests/unit/test_config_manager.py`
- [ ] T064 [P] [US2] Unit test for AIConfiguration validation in `tests/unit/test_ai_config.py`
- [ ] T065 [P] [US2] Contract test for API endpoint connectivity in `tests/contract/test_api_connectivity.py`
- [ ] T066 [US2] Integration test for end-to-end config workflow in `tests/integration/test_config_workflow.py`

### Implementation for User Story 2

- [ ] T067 [P] [US2] Implement ConfigManager.set_api_key() in keyring in `src/services/config_manager.py`
- [ ] T068 [P] [US2] Implement ConfigManager.get_api_key() from keyring in `src/services/config_manager.py`
- [ ] T069 [P] [US2] Implement ConfigManager.set_endpoint_url() in Alfred env vars in `src/services/config_manager.py`
- [ ] T070 [P] [US2] Implement ConfigManager.validate_credentials() (test API call) in `src/services/config_manager.py`
- [ ] T071 [US2] Create config command handler in `src/workflow/command_router.py`
- [ ] T072 [US2] Implement first-run prompt for API key in `src/workflow/config_init.py`
- [ ] T073 [US2] Create configuration UI workflow (set key, set endpoint, test connection) in `src/workflow/config_init.py`
- [ ] T074 [US2] Add provider selection (OpenAI, Anthropic, custom) in `src/workflow/config_init.py`
- [ ] T075 [US2] Implement endpoint validation and custom endpoint support in `src/services/config_manager.py`
- [ ] T076 [US2] Add clear error messages for invalid credentials, connectivity issues in `src/workflow/feedback_builder.py`
- [ ] T077 [US2] Test configuration UI with multiple providers and custom endpoints

**Checkpoint**: User Stories 1 AND 2 both work independently

---

## Phase 5: User Story 3 - Batch Deletion of Created Items (Priority: P3)

**Goal**: Delete all workflow-created calendar items and reminders with one command, preserving user data

**Independent Test**: Create 5 events/reminders → delete all → verify only workflow items removed, user's existing items intact

### Tests for User Story 3 (TDD)

- [ ] T078 [P] [US3] Unit test for CreatedItemTracker.remove_item() in `tests/unit/test_tracker.py`
- [ ] T079 [P] [US3] Unit test for CreatedItemTracker.clear_all() in `tests/unit/test_tracker.py`
- [ ] T080 [US3] Integration test for EventKit deletion of tracked items in `tests/integration/test_eventkit_delete.py`
- [ ] T081 [US3] Integration test for selective deletion workflow in `tests/integration/test_selective_delete.py`

### Implementation for User Story 3

- [ ] T082 [P] [US3] Implement EventKitBridge.delete_calendar_event(event_id) in `src/services/eventkit_bridge.py`
- [ ] T083 [P] [US3] Implement EventKitBridge.delete_reminder(reminder_id) in `src/services/eventkit_bridge.py`
- [ ] T084 [US3] Implement TrackerService.get_all_tracked_items() in `src/services/tracker_service.py`
- [ ] T085 [US3] Create DeletionService orchestrating tracker lookup → EventKit deletion in `src/services/deletion_service.py`
- [ ] T086 [US3] Implement delete command handler in `src/workflow/command_router.py`
- [ ] T087 [US3] Create deletion confirmation UI (list items, confirm delete all) in `src/workflow/feedback_builder.py`
- [ ] T088 [US3] Implement selective deletion (show list, user picks items to delete) in `src/workflow/deletion_workflow.py`
- [ ] T089 [US3] Add deletion summary feedback (X items deleted, Y preserved) in `src/workflow/feedback_builder.py`
- [ ] T090 [US3] Implement error handling for deletion failures in `src/services/deletion_service.py`
- [ ] T091 [US3] Add rollback capability if partial deletion fails in `src/services/deletion_service.py`
- [ ] T092 [US3] Test deletion with large tracker (1000+ items)

**Checkpoint**: All user stories independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and hardening across all user stories

- [ ] T093 [P] Add comprehensive logging throughout application in `src/utils/logger.py`
- [ ] T094 [P] Create README.md with installation, usage, and troubleshooting in `README.md`
- [ ] T095 [P] Create pyproject.toml with complete dependencies and metadata in `pyproject.toml`
- [ ] T096 [P] Add type hints to all modules (src/**/*.py)
- [ ] T097 [P] Format code with black across `src/` and `tests/`
- [ ] T098 [P] Lint code with ruff across `src/` and `tests/`
- [ ] T099 Create Alfred workflow info.plist with metadata in `info.plist`
- [ ] T100 [P] Additional unit tests for edge cases in `tests/unit/`
- [ ] T101 [P] Performance profiling of full workflow (should complete in <10 seconds)
- [ ] T102 Security audit: API keys never logged, error messages don't leak sensitive data
- [ ] T103 Test with very long input (500 words) for performance
- [ ] T104 Test timezone handling and date parsing across timezones
- [ ] T105 Run quickstart.md validation (fresh install works)
- [ ] T106 Create workflow icon and assets in `assets/`
- [ ] T107 Create changelog (CHANGELOG.md)
- [ ] T108 Add git commit hooks for linting/testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - **BLOCKS all user stories**
- **Phase 3-5 (User Stories)**: All depend on Phase 2 completion
  - Can proceed in parallel (P1 → P2 → P3) or all together
  - Each story independently testable
- **Phase 6 (Polish)**: Depends on desired user stories being complete

### Within-Story Task Dependencies

**User Story 1**:
- Tests (T040-T048) must be written first, verified to FAIL
- Models (T049-T050) before parsing (T051)
- Parsing before EventKit creation (T052-T053)
- Creation before tracking (T055)
- All before main.py integration (T061)

**User Story 2**:
- Tests (T063-T066) written first, verified to FAIL
- ConfigManager implementation (T067-T070) before integration (T071-T077)

**User Story 3**:
- Tests (T078-T081) written first, verified to FAIL
- Deletion implementation (T082-T085) before UI workflows (T086-T091)

### Parallel Opportunities

**Phase 1**:
- T003, T004, T005 can run in parallel (linting/formatting/testing setup)

**Phase 2**:
- T009-T011 can run in parallel (configuration models)
- T013-T016 can run in parallel (data models)
- T019-T020 can run in parallel (EventKit Calendar and Reminders)
- T023-T025 can run in parallel (AI client providers)
- T032-T033 can run in parallel (input/output handling)
- T037-T038 can run in parallel (test fixtures)

**Phase 3 (User Story 1)**:
- T040-T045 can run in parallel (unit and contract tests)
- T046-T047 can run in parallel (EventKit integration tests)
- T049-T050 can run in parallel (utility and parsing models)
- T052-T053 can run in parallel (EventKit creation methods)

**Phase 4 (User Story 2)**:
- T063-T064 can run in parallel (config unit tests)
- T067-T070 can run in parallel (ConfigManager methods)

**Phase 5 (User Story 3)**:
- T078-T079 can run in parallel (tracker deletion tests)
- T082-T083 can run in parallel (EventKit deletion methods)

**Phase 6**:
- T093-T098 can run in parallel (logging, docs, types, formatting, linting)

---

## Parallel Execution Example

### Phase 1 Setup (Sequential)

```bash
T001        # Create structure
  ↓
T002        # Initialize project
  ↓
T003, T004, T005  # Linting/formatting/testing (parallel)
  ↓
T006-T008   # Entry point and gitignore
```

### Phase 2 Foundation (Mostly Parallel)

```bash
Setup complete
  ↓
T009-T011, T013-T016, T019-T020, T023-T025  # Models/services (all parallel)
  ↓
T012, T021-T022, T026-T031  # Service integration (depends on models)
  ↓
T032-T036, T037-T039  # Workflow and fixtures (parallel)
```

### Phase 3 User Story 1 (Tests First, Then Implementation Parallel)

```bash
Foundation complete
  ↓
T040-T048         # All tests (run first, should FAIL)
  ↓
T049-T050, T052-T053  # Models and EventKit (parallel)
  ↓
T051, T054-T061   # Parsing and orchestration (depends on models)
  ↓
T062              # Manual testing in Alfred
```

### Phases 4-5 Can Start in Parallel

```bash
Phase 3 foundational work complete
  ↓
User Story 2 (T063-T077) AND User Story 3 (T078-T092) in parallel
```

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**Goal**: Deliver User Story 1 (core value) as quickly as possible

**Steps**:
1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T039)
3. Complete Phase 3: User Story 1 (T040-T062)
4. **STOP and VALIDATE**: Test end-to-end workflow independently
5. Deploy MVP

**Timeline**: ~30-40 hours for MVP

### Incremental Delivery

**Phase 1**: Setup (4 hours)
**Phase 2**: Foundation (16 hours, team parallel possible)
**Phase 3**: US1 MVP (10 hours)
→ **Deploy V1.0** (core feature working)

**Phase 4**: US2 Configuration (6 hours)
→ **Deploy V1.1** (configurable AI service)

**Phase 5**: US3 Deletion (6 hours)
→ **Deploy V1.2** (batch deletion support)

**Phase 6**: Polish (8 hours)
→ **Deploy V2.0** (production-ready)

### Parallel Team Strategy

**If 3 developers available**:
1. **All**: Complete Phase 1 & Phase 2 together (10 hours)
2. **Dev A**: User Story 1 (10 hours) → Deploy MVP
3. **Dev B**: User Story 2 (6 hours) while A finishes
4. **Dev C**: User Story 3 (6 hours) while A finishes
5. **All**: Phase 6 Polish (2-3 hours each)

**Total**: ~20 hours of total effort instead of 50+ sequential

---

## Success Criteria Validation

After completing each phase, validate against success criteria from spec.md:

**Phase 1-2 Complete**: Foundation working
- Config system initialized
- Logger configured
- Data models created

**Phase 3 Complete (US1)**:
- ✅ SC-001: Text → creation in <10 seconds
- ✅ SC-002: AI parsing accuracy 90%+ on test cases
- ✅ SC-005: Items appear in Calendar/Reminders within 5 seconds

**Phase 4 Complete (US2)**:
- ✅ SC-003: 95% configure on first attempt

**Phase 5 Complete (US3)**:
- ✅ SC-006: Deletion preserves 100% of user data

**Phase 6 Complete (Polish)**:
- ✅ SC-004: 500-word input processes without degradation
- ✅ SC-007: Chinese + English input works
- ✅ SC-008: Error messages resolve issues without dev help
- ✅ SC-009: <3 second error response when AI unavailable

---

## Notes

- **[P] marker**: Tasks marked [P] can run in parallel (different files, no dependencies between them)
- **[US#] label**: Indicates which user story task belongs to (US1, US2, US3)
- **File paths**: All paths relative to repository root
- **TDD approach**: Tests FIRST (T040+), ensure they FAIL before implementing corresponding code
- **Checkpoints**: Verify independent functionality at each phase completion
- **Commit often**: After each task or logical group completion
- **Stop at checkpoints**: Validate story independently before moving next priority
- **Avoid**: Vague tasks, same-file conflicts, cross-story dependencies that break independence

---

## Quick Reference: Task Categories

| Category | Task Range | Purpose |
|----------|-----------|---------|
| Setup | T001-T008 | Project structure and tooling |
| Configuration | T009-T012 | AI config, keyring, env vars |
| Data Models | T013-T018 | Dataclasses, validation, logging |
| EventKit Integration | T019-T022 | Calendar/Reminders system access |
| AI Client | T023-T028 | OpenAI, Anthropic providers, prompts |
| Persistence | T029-T031 | Tracking, JSON storage |
| Workflow UI | T032-T036 | Alfred input/output, routing |
| Fixtures | T037-T039 | Test data |
| **US1 Tests** | **T040-T048** | **TDD: Parse → Create → Track** |
| **US1 Code** | **T049-T062** | **Main feature implementation** |
| **US2 Tests** | **T063-T066** | **TDD: Configuration** |
| **US2 Code** | **T067-T077** | **Config UI, validation** |
| **US3 Tests** | **T078-T081** | **TDD: Deletion** |
| **US3 Code** | **T082-T092** | **Delete, list, selective removal** |
| Polish | T093-T108 | Docs, linting, types, testing |
