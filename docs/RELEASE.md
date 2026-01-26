# Reminder-Alf 发布指南

## 自动发布流程

我们使用 GitHub Actions 自动化构建和发布 Alfred 工作流包。

### 发布新版本

#### 1. 基于 Tag 的自动发布（推荐）

```bash
# 1. 创建新 tag（遵循语义化版本）
git tag -a v1.0.0 -m "Release version 1.0.0"

# 2. 推送 tag 到 GitHub
git push origin v1.0.0

# 3. GitHub Actions 会自动：
#    - 运行测试
#    - 生成 .alfredworkflow 文件
#    - 创建 GitHub Release
#    - 上传工作流文件到 Release
```

#### 2. 手动触发构建

如果你想在不创建 Release 的情况下测试构建过程：

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Build Alfred Workflow"
4. 点击 "Run workflow" 按钮
5. 选择分支并运行

工作流包会作为 artifact 提供下载，保存 30 天。

#### 3. 自动 PR 构建

对所有 PR 自动运行：
- ✅ 依赖安装
- ✅ 单元测试
- ✅ 工作流构建
- ✅ 上传 artifact

## 版本命名规范

遵循 [Semantic Versioning](https://semver.org/):

```
v MAJOR.MINOR.PATCH
├─ MAJOR: 重大功能或不兼容变更
├─ MINOR: 新功能（向后兼容）
└─ PATCH: 错误修复
```

示例：
- `v1.0.0` - 初始发布
- `v1.1.0` - 添加 DeepSeek 支持
- `v1.1.1` - 修复 bug

## 发布检查清单

在创建 Release 之前，确保：

- [ ] 所有测试通过：`python -m pytest tests/`
- [ ] 代码已提交：`git status` (clean)
- [ ] 更新版本号（如果适用）
- [ ] 更新 CHANGELOG
- [ ] 文档已更新

## 完整发布流程示例

```bash
# 1. 确保在 main 分支上
git checkout main
git pull origin main

# 2. 更新版本号和文档
# 编辑 CHANGELOG.md, setup.py 等

# 3. 提交更改
git add .
git commit -m "Bump version to 1.1.0"
git push origin main

# 4. 创建 tag
git tag -a v1.1.0 -m "Release v1.1.0: Add DeepSeek support"

# 5. 推送 tag（触发 GitHub Action）
git push origin v1.1.0

# 6. 等待 GitHub Actions 完成（1-2 分钟）
# 7. 在 GitHub Releases 页面查看发布内容
```

## 工作流详情

### 触发条件

✅ 推送到 `main` 或 `master` 分支
✅ 创建 `v*.*.*` 格式的 tag
✅ Pull Request 到 `main` 或 `master`
✅ 手动触发（workflow_dispatch）

### 工作流步骤

1. **Checkout** - 克隆仓库代码
2. **Setup Python** - 安装 Python 3.11
3. **Install dependencies** - 安装项目依赖
4. **Run tests** - 运行单元测试
5. **Build workflow** - 生成 `.alfredworkflow` 文件
6. **Upload artifact** - 上传构建产物（保存 30 天）
7. **Create Release** - 如果是 tag，创建 GitHub Release 并上传文件

### Artifact 保存

- **保存时长**: 30 天
- **访问方式**: GitHub Actions > Workflow > Artifacts
- **文件名**: `Reminder-Alf-{git_hash}.zip` 或 `Reminder-Alf-{tag}.zip`

### Release 发布

自动创建的 Release 包含：

- ✅ `.alfredworkflow` 可执行文件
- ✅ 版本号和发布时间
- ✅ 安装说明
- ✅ 支持的功能列表
- ✅ 文档链接

## 故障排除

### 构建失败

1. 检查 GitHub Actions 日志：
   - 进入 Actions 标签
   - 找到失败的工作流
   - 查看日志找出问题

2. 常见问题：
   - **测试失败**: 本地运行 `python -m pytest tests/` 修复
   - **依赖缺失**: 更新 `setup.py` 和 `requirements.txt`
   - **构建脚本错误**: 本地运行 `python build_workflow.py` 测试

### Release 未创建

- 确保 tag 格式正确：`v1.0.0` (不是 `v1.0` 或 `release-1.0`)
- GitHub Actions 日志可能有更详细的信息
- 检查仓库权限

## 本地测试

在推送之前，在本地测试完整流程：

```bash
# 1. 清理旧的 artifact
rm -f Reminder-Alf.alfredworkflow

# 2. 运行测试
python -m pytest tests/ -v

# 3. 构建工作流
python build_workflow.py

# 4. 验证文件
ls -lh Reminder-Alf.alfredworkflow
unzip -l Reminder-Alf.alfredworkflow
```

## 高级用法

### 环境变量

在 GitHub Actions 中设置仓库级变量：

1. Settings > Secrets and variables > Actions
2. 添加新 variable 或 secret
3. 在工作流中使用：`${{ vars.VARIABLE_NAME }}`

### 自定义构建

修改 `.github/workflows/build-workflow.yml` 以：
- 更改 Python 版本
- 添加额外的构建步骤
- 修改 artifact 保存时长
- 添加通知（邮件、Slack 等）

## 相关资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
- [Alfred Workflow 格式](https://www.alfredapp.com/help/workflows/)
