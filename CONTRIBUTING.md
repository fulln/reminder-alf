# 贡献指南 | Contributing Guide

感谢你考虑为 Reminder-Alf 做出贡献！我们欢迎所有形式的贡献。

Thank you for considering contributing to Reminder-Alf! We welcome all forms of contributions.

## 🌍 语言 | Language

本项目支持中英文双语。你可以用任何一种语言提交 Issue 和 Pull Request。

This project supports both Chinese and English. You can submit Issues and Pull Requests in either language.

## 📋 如何贡献 | How to Contribute

### 报告 Bug | Report Bugs

如果你发现了 Bug，请[创建 Issue](../../issues/new) 并包含：

If you find a bug, please [create an Issue](../../issues/new) with:

- 清晰的标题和描述 | Clear title and description
- 复现步骤 | Steps to reproduce
- 期望行为 | Expected behavior
- 实际行为 | Actual behavior
- 系统环境（macOS 版本、Python 版本等）| System environment (macOS version, Python version, etc.)
- 相关日志或截图 | Relevant logs or screenshots

### 建议新功能 | Suggest Features

我们欢迎新功能建议！请[创建 Issue](../../issues/new) 并说明：

We welcome feature suggestions! Please [create an Issue](../../issues/new) with:

- 功能描述 | Feature description
- 使用场景 | Use cases
- 为什么这个功能有用 | Why this feature would be useful
- 可能的实现方式（可选）| Possible implementation (optional)

### 提交代码 | Submit Code

#### 1. Fork 并克隆仓库 | Fork and Clone

```bash
# Fork 仓库到你的 GitHub 账号
# Fork the repository to your GitHub account

# 克隆你的 fork
# Clone your fork
git clone https://github.com/YOUR_USERNAME/reminder-alf.git
cd reminder-alf

# 添加上游仓库
# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/reminder-alf.git
```

#### 2. 创建分支 | Create Branch

```bash
# 从 main 创建新分支
# Create a new branch from main
git checkout -b feature/your-feature-name

# 或者用于 bug 修复
# Or for bug fixes
git checkout -b fix/bug-description
```

分支命名规范 | Branch naming convention:
- `feature/xxx` - 新功能 | New features
- `fix/xxx` - Bug 修复 | Bug fixes
- `docs/xxx` - 文档更新 | Documentation updates
- `refactor/xxx` - 代码重构 | Code refactoring
- `test/xxx` - 测试相关 | Testing

#### 3. 开发并测试 | Develop and Test

```bash
# 安装依赖
# Install dependencies
python3 -m pip install -e .

# 运行测试
# Run tests
python3 -m pytest tests/ -v

# 代码格式化
# Format code
black src/ tests/

# 代码检查
# Lint code
ruff check src/ tests/
```

#### 4. 提交更改 | Commit Changes

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

Use [Conventional Commits](https://www.conventionalcommits.org/) convention:

```bash
# 新功能
# New feature
git commit -m "feat: add support for recurring events"

# Bug 修复
# Bug fix
git commit -m "fix: resolve calendar permission issue"

# 文档
# Documentation
git commit -m "docs: update installation guide"

# 重构
# Refactoring
git commit -m "refactor: simplify config manager"

# 测试
# Tests
git commit -m "test: add integration tests for delete handler"
```

**Commit 前缀 | Commit Prefixes:**
- `feat:` - 新功能 | New feature
- `fix:` - Bug 修复 | Bug fix
- `docs:` - 文档 | Documentation
- `style:` - 代码格式 | Code style
- `refactor:` - 重构 | Refactoring
- `perf:` - 性能优化 | Performance
- `test:` - 测试 | Tests
- `chore:` - 构建/工具 | Build/Tools
- `ci:` - CI/CD | CI/CD

#### 5. 推送并创建 PR | Push and Create PR

```bash
# 推送到你的 fork
# Push to your fork
git push origin feature/your-feature-name

# 然后在 GitHub 上创建 Pull Request
# Then create a Pull Request on GitHub
```

**PR 标题示例 | PR Title Examples:**
- `feat: Add DeepSeek API support`
- `fix: Resolve import error in run_script.py`
- `docs: Update QUICKSTART guide`

**PR 描述应包含 | PR Description Should Include:**
- 解决的问题或添加的功能 | Problem solved or feature added
- 实现方式 | Implementation approach
- 相关 Issue（如果有）| Related issues (if any)
- 测试情况 | Testing status
- 截图或演示（如适用）| Screenshots or demos (if applicable)

## 🧪 测试要求 | Testing Requirements

所有代码更改都应该包含测试：

All code changes should include tests:

- 新功能必须有单元测试 | New features must have unit tests
- Bug 修复必须有回归测试 | Bug fixes must have regression tests
- 测试覆盖率不应降低 | Test coverage should not decrease
- 所有测试必须通过 | All tests must pass

```bash
# 运行所有测试
# Run all tests
python3 -m pytest tests/ -v

# 检查覆盖率
# Check coverage
python3 -m pytest tests/ --cov=src --cov-report=html

# 查看覆盖率报告
# View coverage report
open htmlcov/index.html
```

## 📝 代码风格 | Code Style

我们使用以下工具保持代码一致性：

We use the following tools to maintain code consistency:

- **Black** - 代码格式化 | Code formatting
- **Ruff** - 代码检查 | Linting
- **Type hints** - 类型提示 | Type annotations

```bash
# 格式化代码
# Format code
black src/ tests/

# 检查代码
# Lint code
ruff check src/ tests/

# 类型检查
# Type check
mypy src/
```

### Python 代码规范 | Python Style Guide

- 使用 Type hints | Use type hints
- 函数和类添加 docstrings | Add docstrings to functions and classes
- 遵循 PEP 8 | Follow PEP 8
- 每行不超过 100 字符 | Max 100 characters per line
- 使用有意义的变量名 | Use meaningful variable names

**示例 | Example:**

```python
def parse_text(text: str, config: AIConfiguration) -> ParseResult:
    """
    Parse natural language text to extract calendar events and reminders.

    Args:
        text: User input text in natural language
        config: AI configuration for the parser

    Returns:
        ParseResult containing extracted events and reminders

    Raises:
        ValueError: If text is empty or invalid
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Implementation...
```

## 🔍 代码审查 | Code Review

所有 PR 都会经过代码审查：

All PRs will go through code review:

- 保持代码简洁清晰 | Keep code clean and clear
- 添加必要的注释 | Add necessary comments
- 遵循项目架构 | Follow project architecture
- 确保向后兼容（除非是 breaking change）| Ensure backward compatibility (unless breaking change)

维护者可能会：

Maintainers may:

- 请求更改 | Request changes
- 提出建议 | Provide suggestions
- 批准并合并 | Approve and merge

## 📦 发布流程 | Release Process

维护者负责发布新版本：

Maintainers are responsible for releasing new versions:

1. 合并所有待发布的 PR | Merge all PRs for the release
2. 运行 `./release.sh [major|minor|patch]` | Run `./release.sh [major|minor|patch]`
3. GitHub Actions 自动构建和发布 | GitHub Actions automatically builds and releases

## 🎯 优先级 | Priorities

我们优先处理以下类型的贡献：

We prioritize the following types of contributions:

1. 🐛 Bug 修复 | Bug fixes
2. 📚 文档改进 | Documentation improvements
3. ✨ 社区需求高的功能 | Highly requested features
4. 🧪 测试覆盖率提升 | Test coverage improvements
5. ♿ 可访问性改进 | Accessibility improvements

## 💬 交流讨论 | Communication

- **GitHub Issues** - Bug 报告和功能建议 | Bug reports and feature requests
- **GitHub Discussions** - 一般讨论和问题 | General discussions and questions
- **Pull Requests** - 代码贡献 | Code contributions

## 🏆 贡献者 | Contributors

感谢所有贡献者！你的名字会自动出现在：

Thank you to all contributors! Your name will automatically appear in:

- GitHub Contributors 页面 | GitHub Contributors page
- Release notes（如果你的 PR 包含在发布中）| Release notes (if your PR is included)

## 📄 许可证 | License

贡献代码即表示你同意将代码以 MIT 许可证开源。

By contributing, you agree that your contributions will be licensed under the MIT License.

查看 [LICENSE](LICENSE) 了解详情。

See [LICENSE](LICENSE) for details.

## ❓ 问题？| Questions?

如有任何问题，欢迎：

If you have any questions, feel free to:

- 创建 Issue | Create an issue
- 发起 Discussion | Start a discussion
- 联系维护者 | Contact maintainers

---

再次感谢你的贡献！🎉

Thank you again for your contribution! 🎉
