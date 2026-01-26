# Feature Specification: AI-Powered Calendar and Reminder Management

**Feature Branch**: `001-ai-calendar-reminder`
**Created**: 2026-01-26
**Status**: Draft
**Input**: User description: "我要的主要是3个功能点比较关键 1. 输入文字直接让ai识别对应格式， 并调用系统的calander 和reminder 写入 2. 设置ai api 和ai 的url ， 默认openai的chat格式，3 提供一键删除当前列上去的calander 和reminder的能力"

## Clarifications

### Session 2026-01-26

- Q: Which calendar should the workflow create events in when the user has multiple calendars configured? → A: Use the user's default calendar (as set in Calendar app preferences)
- Q: How should the workflow distinguish between calendar events (time-specific activities) and reminders (to-do items) when AI parsing is ambiguous? → A: Explicit time references → Calendar events; action phrases → Reminders
- Q: What should happen when the AI cannot identify any calendar events or reminders from the user's input text? → A: Show error message with unparsed text, suggest user rephrase
- Q: How long should the workflow retain tracking data for created calendar events and reminders? → A: Retain indefinitely until user manually deletes items
- Q: Which reminder list should the workflow use when creating reminders? → A: Use the user's default reminder list (as set in Reminders app)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI Text Recognition and System Integration (Priority: P1)

A user copies or types natural language text containing dates, times, and tasks (e.g., "明天下午3点开会讨论项目进展" or "Next Tuesday at 2pm, dentist appointment"). They invoke the Alfred workflow, which uses AI to parse the text, identify calendar events and reminders, and automatically creates them in the macOS Calendar and Reminders apps. The items sync to their iOS devices via iCloud.

**Why this priority**: This is the core value proposition - automating the tedious task of manually creating calendar events and reminders. Without this, there's no product.

**Independent Test**: Can be fully tested by pasting text like "明天3pm会议", triggering the workflow, and verifying a calendar event appears in the system Calendar app. Delivers immediate value by saving manual data entry.

**Acceptance Scenarios**:

1. **Given** user has text "明天下午2点开会" in clipboard, **When** user triggers Alfred workflow with this text, **Then** a calendar event "开会" is created for tomorrow at 2:00 PM in the user's default calendar
2. **Given** user types "提醒我下周买牛奶", **When** user submits to workflow, **Then** a reminder "买牛奶" is created with due date next week in the user's default reminder list
3. **Given** text contains both event and reminder ("周五3点会议，提醒我准备材料"), **When** processed, **Then** both calendar event and reminder are created appropriately
4. **Given** AI successfully parses text, **When** creating items, **Then** user sees confirmation with details of what was created
5. **Given** text is ambiguous about date/time, **When** AI extracts multiple possibilities, **Then** user is prompted to choose or confirm the interpretation

---

### User Story 2 - AI Configuration Management (Priority: P2)

A user needs to configure their preferred AI service (OpenAI, Anthropic, or custom endpoint). They access the Alfred workflow settings and enter their API key and endpoint URL. The default is OpenAI's chat completion format, but users can customize the endpoint for other compatible services. Settings are stored securely.

**Why this priority**: Required infrastructure for the core feature, but can have sensible defaults. Users won't use the tool if they can't configure their AI service, but this is a one-time setup task.

**Independent Test**: Can be tested by configuring a custom API endpoint, verifying credentials are stored securely, and confirming text parsing works with the configured service. Delivers value by enabling user choice and privacy.

**Acceptance Scenarios**:

1. **Given** user opens workflow settings, **When** they enter OpenAI API key, **Then** key is stored securely in system keychain
2. **Given** user wants to use custom AI endpoint, **When** they provide URL and API key, **Then** workflow validates connectivity and saves configuration
3. **Given** user has configured AI service, **When** they test with sample text, **Then** parsing works correctly with their chosen service
4. **Given** API key is invalid or expired, **When** workflow attempts to use it, **Then** user receives clear error message with instructions to update settings
5. **Given** default configuration (OpenAI), **When** user first launches workflow without configuration, **Then** user is prompted to enter API key with clear instructions

---

### User Story 3 - Batch Deletion of Created Items (Priority: P3)

A user realizes they made a mistake or want to clear out test entries. They access a "delete all" function in the Alfred workflow that removes all calendar events and reminders created by this tool. The workflow tracks which items it created to avoid deleting user's other calendar events.

**Why this priority**: Nice-to-have convenience feature. Users can manually delete items from Calendar/Reminders apps if needed. This is about improving UX but isn't critical for MVP.

**Independent Test**: Can be tested by creating several events/reminders via the workflow, triggering the delete function, and verifying only those items are removed while preserving existing calendar data. Delivers value by providing quick cleanup.

**Acceptance Scenarios**:

1. **Given** workflow has created 5 events and 3 reminders today, **When** user selects "delete all created items", **Then** all 8 items are removed from Calendar/Reminders
2. **Given** user has pre-existing calendar events, **When** delete function runs, **Then** only workflow-created items are deleted, others remain intact
3. **Given** user wants to delete selectively, **When** they view created items list, **Then** they can choose which items to keep or delete
4. **Given** items were synced to iCloud, **When** deleted via workflow, **Then** deletions sync across all devices
5. **Given** user confirms deletion, **When** operation completes, **Then** user sees summary of what was deleted

---

### Edge Cases

- When AI cannot parse any recognizable date/time from the input text, workflow displays an error message showing the unparsed text and suggests the user rephrase their input
- How does the system handle timezone differences when user travels?
- What if the Calendar or Reminders app denies permission?
- How to handle very long text input (e.g., entire email or document pasted)?
- What if AI service is temporarily unavailable or rate-limited?
- How to handle text with multiple events on the same day at different times?
- What if user's system date/time settings are incorrect?
- How to handle recurring events (e.g., "every Monday at 9am")?
- What if created items are manually edited by user after creation - can they still be deleted via workflow?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept text input from Alfred's standard input mechanisms (clipboard, typed text, selected text)
- **FR-002**: System MUST send text to configured AI service and receive structured parsing results identifying calendar events and reminders
- **FR-003**: System MUST distinguish between calendar events and reminders using this logic: text with explicit time/date references creates calendar events; text with imperative action phrases ("remind me to...", "don't forget to...") creates reminders
- **FR-004**: System MUST validate AI-parsed data for required fields (title, date/time for events; title for reminders)
- **FR-005**: System MUST create calendar events in the user's default calendar (as configured in macOS Calendar app preferences)
- **FR-006**: System MUST create reminders in the user's default reminder list (as configured in macOS Reminders app preferences)
- **FR-007**: System MUST request and handle Calendar and Reminders permissions from macOS
- **FR-008**: System MUST provide configuration interface for AI API key and endpoint URL
- **FR-009**: System MUST store API credentials securely (system keychain or equivalent)
- **FR-010**: System MUST default to OpenAI chat completion API format
- **FR-011**: System MUST support custom AI endpoint URLs compatible with OpenAI format
- **FR-012**: System MUST track which calendar events and reminders it creates (for deletion capability)
- **FR-013**: System MUST provide function to delete all tracked items
- **FR-014**: System MUST display confirmation of created items to user via Alfred's feedback mechanism
- **FR-015**: System MUST handle errors gracefully (AI service failure, permission denied, invalid input) with clear user messages
- **FR-016**: When AI parsing fails completely (no items identified), system MUST display error message showing the unparsed text and suggest user rephrase
- **FR-017**: System MUST support both English and Chinese text input for AI parsing
- **FR-018**: System MUST prompt user for confirmation when AI parsing is ambiguous
- **FR-019**: System MUST preserve user's existing calendar events and reminders when deleting workflow-created items
- **FR-020**: System MUST provide user feedback during processing (loading indicators, progress status)

### Key Entities

- **Calendar Event**: Represents an event with title, start date/time, optional end date/time, optional location, optional notes. Created in user's default calendar and tracked by workflow for deletion.

- **Reminder**: Represents a task with title, optional due date, optional priority, optional notes. Created in user's default reminder list and tracked by workflow for deletion.

- **AI Configuration**: Stores user's AI service settings including API endpoint URL (default: OpenAI), API key (stored in keychain), and optional model preferences.

- **Created Item Tracker**: Maintains list of calendar event IDs and reminder IDs created by this workflow, enabling selective deletion. Includes creation timestamp and source text metadata. Tracking data is retained indefinitely until user manually deletes items.

- **Parse Result**: Structured data from AI containing identified events (title, datetime, duration, location) and reminders (title, due date, priority) extracted from user's text input.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create calendar events and reminders from natural language text in under 10 seconds (from Alfred trigger to system confirmation)
- **SC-002**: AI parsing correctly identifies dates, times, and event/reminder intent with 90%+ accuracy for common input patterns
- **SC-003**: 95% of users successfully configure AI settings on first attempt without external help
- **SC-004**: Workflow processes text inputs up to 500 words without performance degradation
- **SC-005**: Created items appear in Calendar/Reminders apps and sync to iOS devices within 5 seconds
- **SC-006**: Batch deletion removes all workflow-created items while preserving 100% of user's pre-existing calendar data
- **SC-007**: Users can successfully use the workflow with both English and Chinese text input
- **SC-008**: Error messages enable users to resolve common issues (missing permissions, invalid API key) without developer intervention
- **SC-009**: Workflow handles AI service unavailability with fallback behavior or clear error messaging within 3 seconds

### Assumptions

- Users have macOS with Calendar and Reminders apps installed (standard system apps)
- Users have Alfred with Powerpack license (required for workflows with external scripts)
- Users have or can obtain an API key for OpenAI or compatible AI service
- Users' macOS systems have Python 3.9+ installed or workflow bundles Python runtime
- Users grant Calendar and Reminders permissions when prompted by macOS
- iCloud sync is configured by user separately (not managed by this workflow)
- AI service returns responses in expected JSON format compatible with OpenAI's chat completion structure
- Users understand they are sending text to third-party AI service (privacy consideration)
- Users have configured default calendar and default reminder list in their system preferences
