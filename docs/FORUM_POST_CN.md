# 【开源分享】Reminder-Alf：用 AI 让 macOS 日历和提醒事项更智能 🚀

> 用自然语言创建日程，告别繁琐操作

---

## 📌 项目简介

大家好！今天给大家分享一个我开发的 macOS 效率工具：**Reminder-Alf**。

作为一个经常需要管理日程的人，我一直觉得在 macOS 上创建日历事件和提醒事项太繁琐了——打开应用、选择日期、填写标题、设置时间……能不能像跟人说话一样，直接说"明天下午3点开会"就搞定呢？

于是，**Reminder-Alf** 诞生了！它利用 AI 自然语言解析，让你用一句话就能创建日历事件或提醒事项，而且**完美支持中英文**。

现在支持 **Raycast 扩展**，可以直接在 Raycast 中使用！

## ✨ 核心特性

### 🤖 AI 自然语言解析
- **双语支持**：中英文都能准确识别
- **智能判断**：自动区分是日历事件还是提醒事项
- **多模型支持**：OpenAI GPT、DeepSeek（国内访问友好）、自定义端点

### 📅 深度系统集成
- 直接调用 macOS EventKit，创建的事件和提醒可在系统应用中看到
- 通过 iCloud 自动同步到 iPhone/iPad
- 无需安装额外 App

### � Raycast 集成
- 原生 Raycast 扩展
- 快捷键直接呼出
- 美观的 UI 界面

### �🔒 安全可靠
- API 密钥存储在 macOS 钥匙串，不明文保存
- 支持原子性文件写入，防止数据损坏
- 零数据追踪，隐私优先

### 🗑️ 完整的撤销支持
- 追踪所有创建的项目
- 支持单个删除、批量删除、按时间清理

---

## 🎯 使用演示

### 在 Raycast 中使用
1. 打开 Raycast（⌘ + 空格）
2. 搜索 "Create Event or Reminder"
3. 输入自然语言，如 "明天下午3点开会"
4. 按回车创建

### CLI 使用
```bash
# 创建日历事件
python -m src.cli parse "明天下午3点开会"
python -m src.cli parse "Meeting with John tomorrow at 2pm"

# 创建提醒事项
python -m src.cli parse "提醒我买牛奶"
python -m src.cli parse "Remind me to call the dentist"

# 配置管理
python -m src.cli config status
python -m src.cli config set openai sk-YOUR_KEY gpt-4
python -m src.cli config set deepseek sk-YOUR_KEY deepseek-chat

# 管理项目
python -m src.cli list
python -m src.cli delete <id>
python -m src.cli delete all
```

---

## 🏗️ 技术实现

### 技术栈
- **Python 3.11+** - 后端核心逻辑
- **PyObjC EventKit** - 系统日历/提醒集成
- **TypeScript/React** - Raycast 扩展
- **OpenAI SDK / httpx** - AI API 调用

### 架构设计
```
Raycast Extension (TypeScript)
    ↓ (调用 CLI)
Python CLI (src/cli.py)
    ↓
Services (ai_client, config_manager, eventkit_bridge)
    ↓
Data Models (calendar_event, reminder, parse_result)
    ↓
macOS EventKit (系统日历/提醒)
```

### 测试覆盖
- **104 个测试用例**全部通过
- **55% 代码覆盖率**
- 关键模块覆盖率 93-100%

---

## 📦 安装指南

### 环境要求
- macOS 10.15+（Catalina 或更新）
- Python 3.11+
- Node.js 22.14+（Raycast 扩展需要）
- Raycast（免费版即可）

### 快速安装
```bash
# 1. 克隆仓库
git clone https://github.com/fulln/reminder-alf.git
cd reminder-alf

# 2. 安装 Python 依赖
python3.11 -m pip install -e .

# 3. 配置 AI 密钥
python -m src.cli config set deepseek sk-YOUR_KEY deepseek-chat

# 4. 安装 Raycast 扩展
cd raycast-extension
npm install
npm run dev
```

首次运行时，macOS 会提示授权日历和提醒事项权限。

---

## 🤔 为什么选择这个项目？

| 对比项 | Reminder-Alf | 传统方式 |
|--------|--------------|----------|
| 创建速度 | 3秒一句话 | 30秒多步操作 |
| 语言支持 | 中英文 | 依赖系统语言 |
| 同步方式 | iCloud 原生 | 需手动同步 |
| 隐私保护 | 本地处理 | 第三方服务 |
| 调用方式 | Raycast 快捷键 | 打开应用 |

---

## 🔗 项目链接

- **GitHub 仓库**：[https://github.com/fulln/reminder-alf](https://github.com/fulln/reminder-alf)
- **Release 下载**：[最新版本](https://github.com/fulln/reminder-alf/releases)
- **完整文档**：[项目文档](https://github.com/fulln/reminder-alf/tree/main/docs)

---

## 💬 写在最后

这个项目从构思到完成花了不少时间，现在已经从 Alfred 迁移到了 Raycast，可以免费使用！

如果你也想用自然语言管理日程，欢迎试用！有任何问题或建议，欢迎在 GitHub 上提 Issue 或 PR。

觉得有用的话，给个 ⭐ Star 支持一下吧！

---

**项目状态**：✅ 生产就绪  
**许可证**：MIT License  
**作者**：[@fulln](https://github.com/fulln)

---

*关键词：macOS、日历、提醒事项、AI、自然语言、Python、Raycast、开源、效率工具*
