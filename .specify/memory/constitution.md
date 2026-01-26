<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Rationale: Initial constitution creation for reminder-alf project
- Added sections:
  * Core Principles (5 principles)
  * API Integration Standards
  * Development Workflow
  * Governance
- Templates status:
  ✅ plan-template.md - Constitution Check section compatible
  ✅ spec-template.md - Requirements structure compatible
  ✅ tasks-template.md - Task organization compatible
  ✅ All command files - No agent-specific references found
- Follow-up TODOs: None
-->

# Reminder-Alf Constitution

## Core Principles

### I. Alfred Workflow Integration

The plugin MUST integrate seamlessly with Alfred's workflow system:
- Accept input via Alfred's standard input mechanisms (clipboard, selection, direct input)
- Return structured output to Alfred for display and action
- Follow Alfred's JSON feedback format for rich UI responses
- Support Alfred's configuration and preferences system
- Provide clear user feedback for all operations (success, errors, progress)

**Rationale**: Alfred users expect consistent behavior across workflows. Native integration patterns ensure reliability and maintainability.

### II. AI Processing Pipeline

AI content parsing MUST be reliable and accurate:
- Use structured prompts to extract calendar events and reminders from natural language
- Validate AI-extracted data before system integration
- Handle ambiguous dates/times with explicit user confirmation
- Support multiple languages if the AI model permits
- Gracefully degrade when AI service is unavailable (offline mode or fallback)

**Rationale**: The core value proposition is AI-powered parsing. Accuracy and reliability are non-negotiable for user trust.

### III. macOS/iOS System Integration

System API integration MUST be robust and secure:
- Use official macOS APIs (EventKit) for Calendar and Reminders access
- Request and manage user permissions explicitly
- Handle API failures gracefully with clear error messages
- Respect system-level privacy and security settings
- Support iCloud sync (events/reminders sync across devices automatically via system APIs)

**Rationale**: Direct system integration requires careful handling of permissions and failure modes to maintain user trust and data integrity.

### IV. Error Handling & User Experience

All failure modes MUST be handled explicitly:
- Clear error messages explaining what went wrong and how to fix it
- No silent failures - always notify the user of the outcome
- Validation at each step: input → AI parsing → data validation → system API calls
- Rollback capability if partial operations fail
- Logging for debugging without exposing sensitive user data

**Rationale**: Integrations with AI services and system APIs have multiple failure points. Explicit error handling prevents data loss and user frustration.

### V. Simplicity & Maintainability

Keep the implementation simple and focused:
- Single-purpose modules: input handling, AI processing, system integration
- Direct API calls over abstraction layers (no unnecessary ORMs, repositories, or frameworks)
- Configuration via simple JSON or environment variables
- Minimal dependencies - prefer standard library when possible
- No premature optimization - straightforward code over clever tricks

**Rationale**: Small tools benefit from simplicity. Each additional dependency is a maintenance burden and potential failure point.

## API Integration Standards

### AI Service Integration

- Support pluggable AI providers (OpenAI, Anthropic, local models)
- API keys stored securely in system keychain or environment variables (never in code)
- Implement rate limiting and retry logic with exponential backoff
- Cache AI responses when appropriate to reduce API costs
- Provide fallback to manual parsing if AI service fails

### System API Usage

- Use EventKit framework for Calendar and Reminders on macOS
- Request permissions on first use with clear explanation
- Handle permission denied scenarios gracefully
- Test against multiple macOS versions (support N and N-1 major versions at minimum)
- Document required system permissions in README and setup instructions

## Development Workflow

### Testing Requirements

Testing is OPTIONAL unless explicitly requested, but when implemented:
- Unit tests for AI prompt construction and response parsing
- Integration tests for EventKit API interactions (requires test Calendar/Reminders)
- Manual testing workflow documented in quickstart.md
- Test with various input formats (different date/time formats, languages, edge cases)

### Code Quality

- Use Python type hints for all public functions
- Format with black and sort imports with isort
- Lint with ruff or pylint
- Keep functions small and single-purpose
- Document non-obvious logic with inline comments (avoid restating the obvious)

### Dependency Management

- Use pyproject.toml for dependency specification
- Pin major versions, allow minor/patch updates
- Review dependencies quarterly for security updates
- Prefer pure Python libraries over those requiring compiled extensions

## Governance

### Amendment Process

Constitution changes require:
1. Clear justification for the change
2. Impact assessment on existing code and templates
3. Version bump following semantic versioning
4. Update to dependent templates and documentation

### Compliance

- All PRs MUST verify compliance with core principles
- Complexity additions MUST be justified (see plan-template.md Complexity Tracking)
- Any principle violation MUST be explicitly documented and approved

### Versioning Policy

- **MAJOR**: Principle removal, redefinition, or major governance change
- **MINOR**: New principle added or section materially expanded
- **PATCH**: Clarifications, typo fixes, non-semantic improvements

**Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26
