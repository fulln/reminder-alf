# Reminder-Alf Alfred 工作流安装指南

## 📋 前置要求

### 必需
1. **macOS 10.15+** (Catalina 或更高版本)
2. **Alfred 5 with Powerpack** (需要购买 Powerpack 才能使用工作流)
3. **Python 3.11** (推荐通过 Homebrew 安装)
4. **AI API 密钥** (OpenAI 或 DeepSeek)

### 检查 Python 版本
```bash
python3.11 --version
```

如果没有安装，使用 Homebrew 安装：
```bash
brew install python@3.11
```

## 🚀 安装步骤

### 第一步：安装 Python 依赖

在项目目录中运行：

```bash
cd /Users/fulln/opensource/python/reminder-alf

# 安装依赖
python3.11 -m pip install -e .
```

这会安装以下依赖：
- pyobjc-framework-EventKit (macOS 系统集成)
- alfred-workflow (Alfred 工作流框架)
- keyring (安全密钥存储)
- openai (OpenAI API)
- httpx (HTTP 客户端)

### 第二步：运行设置脚本

```bash
chmod +x setup.sh
./setup.sh
```

这会：
- ✅ 检查 Python 版本
- ✅ 安装依赖
- ✅ 运行测试
- ✅ 创建配置目录

### 第三步：创建 Alfred 工作流

#### 方法 1：手动创建（推荐）

1. **打开 Alfred Preferences**
   - 按 `⌘ + ,` 或点击 Alfred 图标 → Preferences

2. **进入 Workflows 标签**
   - 点击左侧的 "Workflows"

3. **创建新工作流**
   - 点击左下角的 `+` 按钮
   - 选择 "Blank Workflow"

4. **填写工作流信息**
   ```
   Name: Reminder-Alf
   Bundle ID: com.reminder-alf
   Description: AI-powered calendar and reminder management
   Category: Productivity
   Created By: 你的名字
   ```

5. **添加 Keyword 输入**
   - 右键点击画布 → Inputs → Keyword
   - 配置：
     - Keyword: `ral`
     - With Space: ✅ 勾选
     - Argument Required: Optional
     - Title: Reminder-Alf
     - Subtext: Parse natural language to create events and reminders

6. **添加 Run Script 动作**
   - 右键点击画布 → Actions → Run Script
   - 配置：
     - Language: `/usr/local/bin/python3.11`
     - with input as argv
     - 勾选 "Escaping: Backquotes, Dollars and Backslashes"

   - **脚本内容**（重要！）：
     ```python
     #!/usr/bin/env python3.11
     # -*- coding: utf-8 -*-

     import sys
     import os

     # 设置项目路径
     project_path = "/Users/fulln/opensource/python/reminder-alf"
     sys.path.insert(0, os.path.join(project_path, "src"))

     # 导入 Alfred 工作流
     from workflow import Workflow3

     def main(wf):
         """主入口"""
         # 导入主模块
         from main import main as app_main

         # 运行应用
         return app_main(wf)

     if __name__ == "__main__":
         wf = Workflow3()
         sys.exit(wf.run(main))
     ```

7. **连接组件**
   - 从 Keyword 拖动连接线到 Run Script

8. **保存工作流**
   - 按 `⌘ + S`

#### 方法 2：导入工作流文件（如果创建了 .alfredworkflow 文件）

```bash
# 创建工作流包（在项目目录中）
cd /Users/fulln/opensource/python/reminder-alf
# 将 workflow 目录打包
# (需要手动完成)
```

## ⚙️ 配置 AI 提供商

### 配置 OpenAI

1. 获取 API Key：访问 https://platform.openai.com/api-keys

2. 在 Alfred 中配置：
   ```bash
   ral config set openai sk-YOUR_API_KEY gpt-4
   ```

   或使用 GPT-3.5：
   ```bash
   ral config set openai sk-YOUR_API_KEY gpt-3.5-turbo
   ```

### 配置 DeepSeek

1. 获取 API Key：访问 https://platform.deepseek.com/

2. 在 Alfred 中配置：
   ```bash
   ral config set deepseek sk-YOUR_API_KEY deepseek-chat
   ```

   其他模型选项：
   - `deepseek-chat` (通用对话，推荐)
   - `deepseek-coder` (代码理解优化)

### 检查配置状态

```bash
ral config status
```

应该看到：
```
✅ Configured
Provider: openai
Model: gpt-4
```

## 🔐 授权系统权限

首次使用时，macOS 会请求权限：

### 1. Calendar 权限
当你第一次创建日历事件时：
- 系统会弹出对话框
- 点击 "OK" 授予权限

手动授权：
```
System Settings → Privacy & Security → Calendar
→ 勾选 Alfred 或 Python
```

### 2. Reminders 权限
当你第一次创建提醒时：
- 系统会弹出对话框
- 点击 "OK" 授予权限

手动授权：
```
System Settings → Privacy & Security → Reminders
→ 勾选 Alfred 或 Python
```

## ✅ 测试工作流

### 1. 测试基本功能

在 Alfred 中输入：
```bash
ral help
```

应该看到帮助信息。

### 2. 测试配置

```bash
ral config status
```

应该显示你的配置信息。

### 3. 测试解析

```bash
ral Meeting tomorrow at 2pm
```

应该：
- ✅ 调用 AI 解析
- ✅ 显示解析结果
- ✅ 创建日历事件
- ✅ 显示成功消息

### 4. 测试中文

```bash
ral 明天下午3点开会
```

应该正常工作！

## 📝 使用示例

### 创建日历事件

```bash
# 基本事件
ral Meeting tomorrow at 2pm

# 带地点
ral Lunch with Sarah at Downtown Cafe tomorrow at noon

# 全天事件
ral Conference from Feb 1 to Feb 3

# 中文
ral 明天下午3点在会议室开会
ral 下周一上午10点团队站会
```

### 创建提醒

```bash
# 简单提醒
ral Remind me to buy milk

# 带截止日期
ral Submit report by Friday at 5pm

# 高优先级
ral URGENT: Call doctor tomorrow at 10am

# 中文
ral 提醒我买牛奶
ral 周五下午5点前提交报告
```

### 管理项目

```bash
# 列出最近创建的项目
ral list

# 列出最近 20 个
ral list 20

# 删除特定项目
ral delete event-123

# 删除所有
ral delete all

# 删除 7 天前的
ral delete old 7
```

## 🔧 故障排除

### 问题 1: "Command not found: python3.11"

**解决方案**：
```bash
# 安装 Python 3.11
brew install python@3.11

# 或使用系统 Python
# 修改 Alfred 工作流脚本中的 python3.11 为 python3
```

### 问题 2: "No module named 'workflow'"

**解决方案**：
```bash
# 重新安装依赖
cd /Users/fulln/opensource/python/reminder-alf
python3.11 -m pip install -e . --force-reinstall
```

### 问题 3: "Calendar access denied"

**解决方案**：
1. 打开 System Settings → Privacy & Security → Calendar
2. 找到 Alfred 或 Python
3. 勾选允许访问

### 问题 4: "Invalid API key"

**解决方案**：
```bash
# 删除旧配置
ral config delete

# 重新配置
ral config set openai sk-YOUR_NEW_KEY gpt-4
```

### 问题 5: "No items found" (解析失败)

**可能原因**：
- 输入太模糊
- 缺少时间信息（对于日历事件）
- AI 无法理解

**解决方案**：
- ✅ 明确指定时间：`ral meeting tomorrow at 2pm`
- ❌ 避免模糊：`ral meeting tomorrow`

### 问题 6: 工作流没有响应

**调试步骤**：

1. 检查 Python 是否可执行：
   ```bash
   /usr/local/bin/python3.11 --version
   ```

2. 手动测试脚本：
   ```bash
   cd /Users/fulln/opensource/python/reminder-alf
   python3.11 -c "from src.main import main; print('OK')"
   ```

3. 查看 Alfred 调试器：
   - Alfred Preferences → Workflows
   - 点击右上角虫子图标 🐛
   - 输入命令查看错误信息

4. 查看日志：
   ```bash
   cat ~/Library/Application\ Support/Alfred/Workflow\ Data/com.reminder-alf/logs/reminder-alf.log
   ```

## 📂 配置文件位置

```bash
# 配置文件
~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/config.json

# 追踪数据
~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/tracking.json

# 日志文件
~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/logs/

# API 密钥（在 macOS Keychain 中）
# 使用 Keychain Access 应用查看：
# Service: alfred-reminder-alf
```

## 🔄 更新工作流

如果代码有更新：

```bash
cd /Users/fulln/opensource/python/reminder-alf

# 拉取更新
git pull

# 重新安装依赖
python3.11 -m pip install -e . --upgrade

# 运行测试
python3.11 -m pytest tests/
```

## 🎯 高级配置

### 自定义 AI 端点

```bash
# 设置环境变量
export REMINDER_ALF_OPENAI_ENDPOINT=https://your-api.com/v1

# 然后配置
ral config set custom YOUR_API_KEY your-model
```

### 调整日志级别

编辑 `~/.config/reminder-alf/config.json`：
```json
{
  "log_level": "DEBUG"
}
```

### 批量导入

如果有大量项目需要创建，可以写脚本：

```python
#!/usr/bin/env python3.11
import sys
sys.path.insert(0, "/Users/fulln/opensource/python/reminder-alf/src")

from services.parse_service import ParseService
from services.config_manager import ConfigManager

config_manager = ConfigManager()
config = config_manager.get_configuration()
parse_service = ParseService(config)

texts = [
    "Meeting tomorrow at 2pm",
    "Lunch with John on Friday",
    "Remind me to buy milk"
]

for text in texts:
    result = parse_service.parse_input(text)
    print(f"✅ {text}")
```

## 💡 使用技巧

### 1. 快速创建
直接输入自然语言，不需要 `rem` 前缀：
```
Alfred: meeting tomorrow at 2pm
```

### 2. 批量操作
使用 list 命令查看所有项目，然后批量删除：
```bash
ral list
ral delete all
```

### 3. 定期清理
设置定时任务清理旧项目：
```bash
# 每周清理 30 天前的项目
ral delete old 30
```

## 🎉 安装完成！

现在你可以开始使用 Reminder-Alf 了！

**快速开始：**
```bash
rem Meeting with team tomorrow at 2pm
rem 明天下午3点开会
rem Remind me to call John
```

**需要帮助？**
```bash
ral help
```

---

**遇到问题？** 查看 [README.md](README.md) 或提交 Issue
