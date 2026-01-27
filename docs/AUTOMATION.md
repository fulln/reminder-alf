# 🚀 自动发布工作流

Reminder-Alf 提供了完整的自动化发布工作流，包括：

1. **GitHub Actions** - 自动构建和发布
2. **版本管理脚本** - 一键升级版本号
3. **Changelog 自动生成** - 从 Git commits 自动生成

## 快速开始

### 1. 提交代码（遵循 Conventional Commits）

```bash
# 新功能
git commit -m "feat: add DeepSeek API support"

# Bug 修复
git commit -m "fix: resolve import error in run_script.py"

# 文档更新
git commit -m "docs: update installation guide"

# 代码重构
git commit -m "refactor: simplify config manager"
```

### 2. 一键发布新版本

```bash
# 升级补丁版本 (1.0.0 -> 1.0.1)
./release.sh patch

# 升级次版本 (1.0.0 -> 1.1.0)
./release.sh minor

# 升级主版本 (1.0.0 -> 2.0.0)
./release.sh major
```

### 3. 自动完成

脚本会自动：
- ✅ 从 Git commits 生成 changelog
- ✅ 更新版本号（pyproject.toml）
- ✅ 运行测试
- ✅ 构建 Alfred workflow
- ✅ 提交更改
- ✅ 创建 Git tag
- ✅ 推送到 GitHub

### 4. GitHub Actions 接管

推送后，GitHub Actions 会自动：
- ✅ 运行完整测试
- ✅ 构建 .alfredworkflow 文件
- ✅ 创建 GitHub Release
- ✅ 上传 workflow 文件到 Release

## Git Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 前缀 | 说明 | Changelog 分类 |
|------|------|---------------|
| `feat:` | 新功能 | Added |
| `fix:` | Bug 修复 | Fixed |
| `docs:` | 文档 | Changed |
| `refactor:` | 重构 | Changed |
| `perf:` | 性能优化 | Changed |
| `remove:` | 删除功能 | Removed |
| `deprecate:` | 废弃功能 | Deprecated |
| `security:` | 安全修复 | Security |
| `chore:` | 构建/工具 | 不显示 |
| `ci:` | CI 配置 | 不显示 |

### 示例

```bash
# ✅ 好的提交信息
feat: add support for custom API endpoints
fix: resolve calendar permission issue on macOS 14
docs: update QUICKSTART guide with new keyword
refactor: simplify AI client error handling
perf: optimize parsing performance with caching

# ❌ 不好的提交信息
update code
fix bug
wip
```

## 发布脚本选项

### 基本用法

```bash
./release.sh [major|minor|patch] [options]
```

### 选项

#### --dry-run (-d)
模拟运行，查看将要生成的 changelog，不实际修改文件

```bash
./release.sh patch --dry-run
```

输出示例：
```
🚀 Reminder-Alf 自动发布
================================

1️⃣  检查 Git 工作区...
✅ 工作区干净

2️⃣  升级版本号...
   当前版本: 1.0.0
   新版本:   1.0.1

[模拟模式]

📝 将要生成的 Changelog:
---
### Added
- support for DeepSeek API

### Fixed
- import error in run_script.py
---
```

#### --no-push (-n)
只创建 tag，不推送到远程

```bash
./release.sh minor --no-push
```

使用场景：
- 本地测试发布流程
- 需要手动检查后再推送

### 完整示例

```bash
# 1. 查看将要生成的内容
./release.sh patch --dry-run

# 2. 如果满意，执行发布
./release.sh patch

# 3. 或者先不推送，检查后再手动推送
./release.sh patch --no-push
git push origin main
git push origin v1.0.1
```

## 工作流程详解

### 自动化流程图

```
提交代码
   ↓
feat: add feature X
fix: resolve bug Y
   ↓
./release.sh patch
   ↓
┌─────────────────────────┐
│ 1. 检查工作区           │
│ 2. 收集 Git commits     │
│ 3. 生成 changelog       │
│ 4. 更新版本号           │
│ 5. 运行测试             │
│ 6. 构建 workflow        │
│ 7. Git commit & tag     │
│ 8. 推送到 GitHub        │
└─────────────────────────┘
   ↓
GitHub Actions 触发
   ↓
┌─────────────────────────┐
│ 1. Checkout 代码        │
│ 2. 安装依赖             │
│ 3. 运行测试             │
│ 4. 构建 workflow        │
│ 5. 创建 Release         │
│ 6. 上传文件             │
└─────────────────────────┘
   ↓
发布完成！
```

### 文件更新

发布时会自动更新这些文件：

1. **pyproject.toml** - Python 项目配置（版本号）
   ```toml
   [project]
   name = "reminder-alf"
   version = "1.0.1"
   ```

2. **CHANGELOG.md** - 变更日志
   ```markdown
   ## [Unreleased]

   ## [1.0.1] - 2026-01-26

   ### Added
   - Support for DeepSeek API

   ### Fixed
   - Import error in run_script.py
   ```

## GitHub Actions 配置

工作流文件位置：`.github/workflows/build-workflow.yml`

### 触发条件

- ✅ 推送到 `main` 分支
- ✅ 创建 `v*.*.*` 格式的 tag（自动发布）
- ✅ Pull Request 到 `main` 分支
- ✅ 手动触发

### 手动触发构建

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **Build Alfred Workflow**
4. 点击 **Run workflow**
5. 选择分支并运行

构建结果会作为 Artifact 保存 30 天。

### 查看构建状态

```bash
# 构建状态
https://github.com/YOUR_USERNAME/reminder-alf/actions

# Release 页面
https://github.com/YOUR_USERNAME/reminder-alf/releases
```

## 最佳实践

### 1. 频繁提交，清晰描述

```bash
# ✅ 每个功能单独提交
git commit -m "feat: add keyboard shortcut support"
git commit -m "feat: add dark mode theme"

# ❌ 多个功能一起提交
git commit -m "add features"
```

### 2. 定期发布

```bash
# 补丁版本 - 每周或每次 bug 修复
./release.sh patch

# 次版本 - 每月或新功能完成
./release.sh minor

# 主版本 - 重大变更或不兼容更新
./release.sh major
```

### 3. 发布前检查

```bash
# 1. 运行测试
python3 -m pytest tests/

# 2. 本地构建
python3 build_workflow.py

# 3. 预览 changelog
./release.sh patch --dry-run

# 4. 发布
./release.sh patch
```

### 4. 版本号语义

遵循 [Semantic Versioning](https://semver.org/):

- **MAJOR** (主版本) - 不兼容的 API 变更
- **MINOR** (次版本) - 向后兼容的新功能
- **PATCH** (补丁) - 向后兼容的 bug 修复

示例：
```
1.0.0 → 1.0.1  (fix: bug fixes)
1.0.1 → 1.1.0  (feat: new features)
1.1.0 → 2.0.0  (remove: breaking changes)
```

## 故障排除

### 问题：工作区有未提交的修改

```bash
❌ 工作区有未提交的修改
请先提交或暂存修改
```

**解决**：
```bash
# 查看修改
git status

# 提交修改
git add .
git commit -m "feat: your message"

# 或暂存修改
git stash

# 发布
./release.sh patch

# 恢复修改
git stash pop
```

### 问题：测试失败

```bash
❌ 测试失败，请修复后再发布
```

**解决**：
```bash
# 运行测试查看具体错误
python3 -m pytest tests/ -v

# 修复错误后重新提交
git add .
git commit -m "fix: resolve test failures"

# 重新发布
./release.sh patch
```

### 问题：推送失败

```bash
❌ 推送 commits 失败
```

**解决**：
```bash
# 检查远程分支
git remote -v

# 拉取最新代码
git pull origin main --rebase

# 重新推送
git push origin main
git push origin v1.0.1
```

### 问题：GitHub Actions 构建失败

1. 查看 Actions 页面的日志
2. 检查依赖是否完整
3. 本地运行相同的命令测试
4. 修复后重新推送 tag

```bash
# 删除本地 tag
git tag -d v1.0.1

# 删除远程 tag
git push origin :refs/tags/v1.0.1

# 修复后重新发布
./release.sh patch
```

## 高级用法

### 自定义 Changelog

如果需要手动编辑 changelog：

```bash
# 1. 生成初始 changelog
./release.sh patch --no-push

# 2. 手动编辑 CHANGELOG.md
vim CHANGELOG.md

# 3. 修改 commit
git add CHANGELOG.md
git commit --amend --no-edit

# 4. 推送
git push origin main --force-with-lease
git push origin v1.0.1
```

### 回滚发布

```bash
# 删除 tag
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# 回滚 commit
git reset --hard HEAD~1
git push origin main --force-with-lease

# 在 GitHub 删除 Release（如果已创建）
```

## 相关文档

- [RELEASE.md](RELEASE.md) - 详细发布指南
- [CHANGELOG.md](CHANGELOG.md) - 完整变更历史
- [.github/workflows/build-workflow.yml](.github/workflows/build-workflow.yml) - CI/CD 配置

---

**Happy Releasing! 🎉**
