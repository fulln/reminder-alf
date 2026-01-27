# Changelog

All notable changes to Reminder-Alf will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [Unreleased]

## [1.1.0] - 2026-01-27

### Added
- add automated release workflow via GitHub Actions
- add Python package distribution to releases
- initial release with AI-powered calendar and reminder management (#1)

### Changed
- consolidate version to pyproject.toml only
- reorganize project structure and add badges
- Initial commit from Specify template

### Fixed
- resolve GitHub Actions CI build failures
- correct pyproject.toml structure
- update pyproject.toml with correct metadata
- standardize on main as primary branch
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-26

### Added

#### Core Features
- 🤖 AI-powered natural language parsing for calendar events and reminders
- 📅 Direct integration with macOS Calendar and Reminders via EventKit
- 🔄 Automatic iCloud sync to iOS devices
- 🌐 Multi-language support (English and Chinese)
- 🔒 Secure API key storage in macOS Keychain

#### AI Provider Support
- OpenAI (GPT-4, GPT-3.5-turbo)
- Anthropic Claude (Claude 3 Opus, Sonnet, Haiku)
- Custom OpenAI-compatible endpoints

#### Command Interface
- `rem <text>` - Parse natural language to create events/reminders
- `rem config` - Manage AI configuration
  - `config status` - View current configuration
  - `config set <provider> <api-key> [model]` - Set up AI provider
  - `config delete [provider]` - Remove configuration
- `rem list [limit]` - View recently created items
- `rem delete` - Delete tracked items
  - `delete <id>` - Delete specific item
  - `delete all` - Delete all tracked items
  - `delete old [days]` - Delete items older than N days
- `rem help` - Show command help

#### Architecture
- **Data Models**: AIConfiguration, CalendarEvent, Reminder, ParseResult, CreatedItem
- **Services**: AIClient, ConfigManager, EventKitBridge, ParseService, TrackerService
- **Workflow Components**: InputHandler, FeedbackBuilder, CommandRouter
- **Command Handlers**: Parse, Config, Delete, List, Help

#### Development
- Comprehensive test suite (104 tests, 55% coverage)
- TDD approach with pytest
- Type hints throughout (Python 3.11+)
- Code quality tools (ruff, black, mypy)
- Integration tests for end-to-end workflows

#### Documentation
- Complete README with installation and usage instructions
- Setup script for easy installation
- Environment variable configuration template
- Alfred workflow configuration (info.plist)
- Inline code documentation and docstrings

### Technical Details

#### Project Structure
```
reminder-alf/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── workflow/        # Alfred integration
│   │   └── handlers/    # Command handlers
│   └── utils/           # Utilities
├── tests/               # Test suite
├── workflow/            # Alfred workflow config
└── specs/               # Specifications
```

#### Testing
- Unit tests for all components
- Integration tests for workflows
- Mock-based testing for external dependencies
- 55% code coverage overall
- 80-100% coverage for core workflow components

#### Dependencies
- pyobjc-framework-EventKit - macOS Calendar/Reminders integration
- alfred-workflow - Alfred workflow helpers
- keyring - Secure credential storage
- openai - OpenAI API client
- anthropic - Anthropic API client
- httpx - HTTP client
- python-dateutil - Date parsing

### Design Decisions

1. **Security First**: API keys stored in macOS Keychain, never in plaintext
2. **Atomic Operations**: Tracking data uses atomic file writes (temp + rename)
3. **Error Handling**: Comprehensive error handling with user-friendly messages
4. **Type Safety**: Full type hints for better IDE support and fewer bugs
5. **Testability**: Dependency injection and mocking for isolated testing
6. **Extensibility**: Plugin-like handler architecture for easy feature additions

### Known Limitations

1. EventKit permissions must be granted manually in System Settings
2. AI parsing quality depends on provider and model selection
3. Ambiguous dates/times may require clarification
4. Recurrence rules not yet fully supported
5. Batch operations for multiple items not optimized

### Future Enhancements

- [ ] Voice input support via macOS speech recognition
- [ ] Smart suggestions based on history
- [ ] Calendar conflict detection
- [ ] Advanced recurrence rule support
- [ ] Custom calendar/list selection UI
- [ ] Export/import of tracking data
- [ ] Analytics dashboard for usage patterns
- [ ] Multi-account support
- [ ] Siri Shortcuts integration

---

## Development Notes

### Phase 1: Setup (Complete)
- Project structure
- Dependencies
- Configuration files
- Test infrastructure

### Phase 2: Foundational (Complete)
- Core data models
- Service layer
- EventKit integration
- AI client abstraction
- Workflow components

### Phase 3: User Story 1 - AI Parsing MVP (Complete)
- Natural language parsing
- Event/reminder creation
- Item tracking
- Full workflow integration

### Phase 4: User Story 2 - Configuration (Complete)
- Configuration management
- API key handling
- Provider validation
- Setup utilities

### Phase 5: User Story 3 - Deletion (Complete)
- Individual item deletion
- Bulk deletion
- Age-based cleanup
- List view for selection

### Phase 6: Polish (In Progress)
- Documentation
- Setup automation
- Error messages refinement
- Performance optimization

---

**Contributors**: Built with ❤️ for Alfred users

**License**: MIT License
