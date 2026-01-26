# 📁 项目结构说明

## 根目录文件说明

### 📚 文档（按阅读顺序）

1. **README.md** - 项目主文档，从这里开始 ⭐
2. **QUICKSTART.md** - 快速开始指南（用户必读）
3. **INSTALL_ALFRED.md** - 详细安装说明
4. **DEEPSEEK.md** - DeepSeek AI 配置指南
5. **CONTRIBUTING.md** - 贡献指南（开发者必读）
6. **DEVELOPMENT.md** - 开发者文档
7. **AUTOMATION.md** - 自动化工作流说明
8. **RELEASE.md** - 发布指南
9. **CHANGELOG.md** - 版本变更日志
10. **LICENSE** - MIT 开源许可证
11. **PROJECT_SUMMARY_CN.md** - 项目中文总结
12. **CLAUDE.md** - Claude AI 相关说明

### 🛠️ 脚本文件

1. **build_workflow.py** - 构建 Alfred 工作流包
   ```bash
   python3 build_workflow.py
   ```

2. **release.sh** - 自动版本发布脚本 ⭐
   ```bash
   ./release.sh patch  # 1.0.0 -> 1.0.1
   ./release.sh minor  # 1.0.0 -> 1.1.0
   ./release.sh major  # 1.0.0 -> 2.0.0
   ```

3. **quick-install.sh** - 一键安装脚本
   ```bash
   bash quick-install.sh
   ```

4. **setup.sh** - 开发环境设置
   ```bash
   bash setup.sh
   ```

### ⚙️ 配置文件

1. **pyproject.toml** - Python 项目配置
2. **VERSION** - 当前版本号
3. **.env.example** - 环境变量示例
4. **.gitignore** - Git 忽略文件
5. **.ruff.toml** - 代码检查配置

### 📦 构建产物

- **Reminder-Alf.alfredworkflow** - Alfred 工作流包（可直接导入）

## 目录结构

```
reminder-alf/
├── 📚 文档
│   ├── README.md                    # 主文档 ⭐
│   ├── QUICKSTART.md               # 快速开始
│   ├── INSTALL_ALFRED.md           # 安装指南
│   ├── DEEPSEEK.md                 # DeepSeek 配置
│   ├── CONTRIBUTING.md             # 贡献指南
│   ├── DEVELOPMENT.md              # 开发文档
│   ├── AUTOMATION.md               # 自动化说明
│   ├── RELEASE.md                  # 发布指南
│   ├── CHANGELOG.md                # 变更日志
│   └── LICENSE                     # MIT 许可证
│
├── 🛠️ 脚本
│   ├── build_workflow.py           # 构建工作流
│   ├── release.sh                  # 自动发布 ⭐
│   ├── quick-install.sh            # 一键安装
│   └── setup.sh                    # 环境设置
│
├── ⚙️ 配置
│   ├── pyproject.toml              # Python 配置
│   ├── VERSION                     # 版本号
│   ├── .env.example                # 环境变量示例
│   ├── .gitignore                  # Git 忽略
│   └── .ruff.toml                  # 代码检查
│
├── 🔧 源代码
│   ├── src/                        # Python 源代码
│   │   ├── models/                 # 数据模型
│   │   ├── services/               # 业务逻辑
│   │   ├── workflow/               # Alfred 工作流
│   │   └── utils/                  # 工具函数
│   │
│   └── workflow/                   # Alfred 工作流配置
│       ├── info.plist              # 工作流配置
│       └── run_script.py           # 入口脚本
│
├── 🧪 测试
│   └── tests/                      # 单元测试和集成测试
│       ├── fixtures/               # 测试数据
│       └── test_*.py               # 测试文件
│
├── 📋 规范文档
│   └── specs/                      # 功能规范
│       └── 001-ai-calendar-reminder/
│           ├── spec.md             # 功能规范
│           ├── plan.md             # 实现计划
│           ├── tasks.md            # 任务列表
│           └── data-model.md       # 数据模型
│
├── ⚙️ GitHub
│   └── .github/
│       └── workflows/
│           └── build-workflow.yml  # CI/CD 配置
│
└── 📦 产物
    └── Reminder-Alf.alfredworkflow # Alfred 工作流包

```

## 快速导航

### 👤 用户

1. 安装：[QUICKSTART.md](QUICKSTART.md)
2. 使用：[README.md](README.md)
3. DeepSeek：[DEEPSEEK.md](DEEPSEEK.md)

### 👨‍💻 开发者

1. 贡献：[CONTRIBUTING.md](CONTRIBUTING.md)
2. 开发：[DEVELOPMENT.md](DEVELOPMENT.md)
3. 发布：[AUTOMATION.md](AUTOMATION.md)

### 🔧 维护者

1. 发布：[RELEASE.md](RELEASE.md)
2. 自动化：[AUTOMATION.md](AUTOMATION.md)
3. 构建：`./release.sh patch`

## 文件大小

```
总计：~2 MB（包含工作流包）
- 源代码：~150 KB
- 文档：~200 KB
- 测试：~100 KB
- 工作流包：~35 KB
```

## 常用命令

```bash
# 开发
python3 -m pytest tests/              # 运行测试
python3 build_workflow.py            # 构建工作流
bash quick-install.sh                # 快速安装

# 发布
./release.sh patch --dry-run         # 预览发布
./release.sh patch                   # 发布补丁版本
./release.sh minor                   # 发布次版本
./release.sh major                   # 发布主版本

# Git
git status                           # 查看状态
git add .                            # 添加所有文件
git commit -m "feat: xxx"            # 提交（遵循规范）
git push origin main                 # 推送
```

## 文档更新日志

- 2026-01-26: 初始版本，完整项目结构
