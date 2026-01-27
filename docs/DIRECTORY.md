# 项目目录整理

## 根目录结构

```
reminder-alf/
├── 📖 核心文档（保留在根目录）
│   ├── README.md                   # 项目主文档 ⭐⭐⭐
│   ├── LICENSE                     # MIT 开源许可证
│   ├── CHANGELOG.md                # 版本变更日志
│   └── CONTRIBUTING.md             # 贡献指南
│
├── 📚 docs/ - 详细文档目录
│   ├── QUICKSTART.md               # 5分钟快速开始
│   ├── INSTALL_ALFRED.md           # 详细安装指南
│   ├── DEEPSEEK.md                 # DeepSeek 配置指南
│   ├── DEVELOPMENT.md              # 开发者文档
│   ├── AUTOMATION.md               # 自动化工作流说明
│   ├── RELEASE.md                  # 发布指南
│   ├── STRUCTURE.md                # 项目结构说明
│   ├── PROJECT_SUMMARY_CN.md       # 项目中文总结
│   └── CLAUDE.md                   # Claude AI 相关说明
│
├── 🛠️ scripts/ - 脚本工具
│   ├── build_workflow.py           # 构建 Alfred 工作流包
│   ├── release.sh                  # 一键自动发布脚本
│   ├── quick-install.sh            # 一键安装脚本
│   └── setup.sh                    # 开发环境设置
│
├── ⚙️ 配置文件
│   ├── pyproject.toml              # Python 项目配置（含版本号）
│   ├── .env.example                # 环境变量示例
│   ├── .gitignore                  # Git 忽略配置
│   └── .ruff.toml                  # 代码检查配置
│
├── 🔧 源代码
│   └── src/                        # Python 源代码
│       ├── models/                 # 数据模型
│       ├── services/               # 业务逻辑服务
│       ├── workflow/               # Alfred 工作流
│       └── utils/                  # 工具函数
│
├── 🧪 tests/                       # 测试代码
│   ├── fixtures/                   # 测试数据
│   └── test_*.py                   # 测试文件
│
├── 📋 specs/                       # 产品规范文档
│   └── 001-ai-calendar-reminder/   # 项目规范
│
├── 🔧 workflow/                    # Alfred 工作流配置
│   ├── info.plist                  # 工作流配置文件
│   └── run_script.py               # 工作流入口脚本
│
├── ⚙️ .github/                     # GitHub 配置
│   └── workflows/
│       └── build-workflow.yml      # CI/CD 配置
│
└── 📦 产物
    └── Reminder-Alf.alfredworkflow # 最终 Alfred 工作流包

```

## 阅读指南

### 👤 用户

1. 开始：[README.md](../README.md) - 项目介绍
2. 安装：[docs/QUICKSTART.md](QUICKSTART.md) - 5分钟快速开始
3. 详细：[docs/INSTALL_ALFRED.md](INSTALL_ALFRED.md) - 完整安装指南
4. DeepSeek：[docs/DEEPSEEK.md](DEEPSEEK.md) - 中文 AI 配置

### 👨‍💻 开发者

1. 贡献：[CONTRIBUTING.md](../CONTRIBUTING.md) - 贡献流程
2. 开发：[docs/DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南
3. 架构：[docs/STRUCTURE.md](STRUCTURE.md) - 项目结构

### 🔧 维护者

1. 发布：[docs/AUTOMATION.md](AUTOMATION.md) - 自动化工作流
2. 脚本：[scripts/release.sh](../scripts/release.sh) - 版本发布
3. 构建：[scripts/build_workflow.py](../scripts/build_workflow.py) - 工作流构建

## 常用命令

### 开发

```bash
# 安装
bash scripts/quick-install.sh

# 测试
python3 -m pytest tests/

# 构建
python3 scripts/build_workflow.py

# 代码检查
ruff check src/
black src/ --check
```

### 发布

```bash
# 预览发布
./scripts/release.sh patch --dry-run

# 发布补丁版本 (1.0.0 -> 1.0.1)
./scripts/release.sh patch

# 发布次版本 (1.0.0 -> 1.1.0)
./scripts/release.sh minor

# 发布主版本 (1.0.0 -> 2.0.0)
./scripts/release.sh major
```

## 文件移动说明

从原始结构迁移的文件：

- ✅ 文档文件移至 `docs/`：QUICKSTART.md, INSTALL_ALFRED.md, DEEPSEEK.md, DEVELOPMENT.md, AUTOMATION.md, RELEASE.md, STRUCTURE.md, PROJECT_SUMMARY_CN.md, CLAUDE.md
- ✅ 脚本文件移至 `scripts/`：build_workflow.py, release.sh, quick-install.sh, setup.sh
- ✅ 核心文件保留根目录：README.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md

## 优势

- 🎯 **清晰易用** - 用户只需看根目录的 4 个文件
- 📚 **分类明确** - 文档、脚本、代码各自分开
- 🚀 **便于维护** - 结构清晰，扩展性好
- 📖 **易于导航** - 文档之间链接清晰

---

更新日期：2026-01-26
