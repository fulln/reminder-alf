# 🚀 Reminder-Alf 快速开始指南

## 方法选择

### 🎯 方法 1：一键自动安装（推荐，最简单）

**只需 3 个命令：**

```bash
cd /path/to/reminder-alf

# 1. 一键安装（包含依赖安装、测试、生成工作流）
bash quick-install.sh

# 2. 双击导入到 Alfred（或运行下面的命令）
open Reminder-Alf.alfredworkflow

# 3. 配置 AI（在 Alfred 中输入）
ral config set openai sk-YOUR_API_KEY gpt-4
```

**就这么简单！**✅

---

### 🔧 方法 2：仅生成工作流包（已有依赖）

如果你已经安装过依赖，只想重新生成工作流包：

```bash
cd /path/to/reminder-alf

# 生成 .alfredworkflow 文件
python3.11 build_workflow.py

# 双击导入
open Reminder-Alf.alfredworkflow
```

---

### 📝 方法 3：手动安装（完全控制）

查看 [INSTALL_ALFRED.md](INSTALL_ALFRED.md) 获取详细的手动安装步骤。

---

## 📦 方法 1 详细说明

### 第一步：运行一键安装脚本

```bash
cd /path/to/reminder-alf
bash quick-install.sh
```

**脚本会自动完成：**
1. ✅ 检查 Python 3.11 是否安装
2. ✅ 安装所有 Python 依赖
3. ✅ 运行测试确保一切正常
4. ✅ 生成 `Reminder-Alf.alfredworkflow` 文件
5. ✅ 创建配置目录

**输出示例：**
```
🚀 Reminder-Alf 一键安装
================================

1️⃣  检查 Python 3.11...
   ✅ 找到: Python 3.11.7

2️⃣  安装 Python 依赖...
   ✅ 依赖安装完成

3️⃣  运行测试...
   ✅ 所有测试通过

4️⃣  生成 Alfred 工作流包...
   ✅ 工作流包创建成功

5️⃣  创建配置目录...
   ✅ 目录创建完成

✅ 安装完成！
```

### 第二步：导入工作流到 Alfred

**自动方式：**
```bash
open Reminder-Alf.alfredworkflow
```

**或手动方式：**
1. 在 Finder 中找到 `Reminder-Alf.alfredworkflow`
2. 双击该文件
3. Alfred 会弹出导入对话框
4. 点击 "Import" 按钮

![Alfred Import](https://i.imgur.com/example.png)

### 第三步：配置 AI 供应商

**获取 API 密钥：**

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

**在 Alfred 中配置：**

```bash
# OpenAI (推荐 GPT-4)
ral config set openai sk-YOUR_API_KEY gpt-4

# 或 GPT-3.5 (更便宜)
ral config set openai sk-YOUR_API_KEY gpt-3.5-turbo

# DeepSeek (中文优化，性价比高)
ral config set deepseek sk-YOUR_API_KEY deepseek-chat
```

**验证配置：**
```bash
ral config status
```

应该看到：
```
✅ Configured
Provider: openai
Model: gpt-4
```

### 第四步：测试工作流

**测试帮助命令：**
```bash
ral help
```

**测试解析（英文）：**
```bash
ral Meeting tomorrow at 2pm
```

**测试解析（中文）：**
```bash
ral 明天下午3点开会
```

**应该看到：**
- ⏳ 正在解析...
- 📅 解析结果显示
- ✅ 创建成功消息

---

## 🔑 授权系统权限

**首次使用时，macOS 会请求权限：**

### Calendar 权限
- 第一次创建日历事件时会弹出对话框
- 点击 "OK" 授予权限

### Reminders 权限
- 第一次创建提醒时会弹出对话框
- 点击 "OK" 授予权限

**如果拒绝了，手动授权：**
```
System Settings → Privacy & Security → Calendar/Reminders
→ 勾选 Alfred 或 Python
```

---

## 📖 使用示例

### 创建日历事件

```bash
# 基本事件
ral Meeting tomorrow at 2pm

# 带地点
ral Lunch with Sarah at Downtown Cafe at noon

# 全天事件
ral Conference from Feb 1 to Feb 3

# 中文
ral 明天下午3点开会
ral 下周一上午10点团队站会
```

### 创建提醒

```bash
# 简单提醒
ral Remind me to buy milk

# 带截止日期
ral Submit report by Friday at 5pm

# 高优先级
ral URGENT: Call doctor tomorrow

# 中文
ral 提醒我买牛奶
ral 周五前提交报告
```

### 管理项目

```bash
# 列出最近创建的项目
ral list

# 删除特定项目
ral delete event-123

# 删除所有
ral delete all

# 删除 7 天前的
ral delete old 7
```

---

## ⚡ 快速命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `ral <文本>` | 解析并创建 | `ral Meeting at 2pm` |
| `ral config status` | 查看配置 | - |
| `ral config set` | 设置配置 | `ral config set openai sk-... gpt-4` |
| `ral config endpoint` | 设置自定义端点 | `ral config endpoint https://api.deepseek.com` |
| `ral config timeout` | 设置超时时间 | `ral config timeout 30` |
| `ral config tokens` | 设置最大 Tokens | `ral config tokens 2000` |
| `ral list [N]` | 列出最近 N 个项目 | `ral list 20` |
| `ral delete <id>` | 删除特定项目 | `ral delete event-123` |
| `ral delete all` | 删除所有 | - |
| `ral delete old [N]` | 删除 N 天前的 | `ral delete old 7` |
| `ral help` | 显示帮助 | - |

---

## 🔧 故障排除

### 问题：找不到 python3.11

**解决：**
```bash
# 安装 Python 3.11
brew install python@3.11

# 重新运行安装
bash quick-install.sh
```

### 问题：工作流没反应

**检查：**

1. 查看 Alfred 调试器
   - Alfred Preferences → Workflows
   - 点击右上角 🐛 图标
   - 输入命令查看错误

2. 手动测试：
```bash
cd /path/to/reminder-alf
python3.11 -c "from src.main import main; print('OK')"
```

### 问题：AI 解析失败

**原因：**
- API 密钥无效
- 网络问题
- 输入太模糊

**解决：**
```bash
# 重新配置
ral config delete
ral config set openai sk-NEW_KEY gpt-4

# 使用更明确的输入
ral Meeting tomorrow at 2pm    ✅ 好
ral meeting tomorrow            ❌ 太模糊
```

---

## 📂 文件位置

| 内容 | 位置 |
|------|------|
| 工作流包 | `Reminder-Alf.alfredworkflow` |
| 配置文件 | `~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/config.json` |
| 追踪数据 | `~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/tracking.json` |
| 日志 | `~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/logs/` |

---

## 🎉 开始使用！

安装完成后，只需在 Alfred 中输入：

```bash
ral Meeting tomorrow at 2pm
```

就这么简单！🚀

**需要帮助？**
```bash
ral help
```

**更多文档：**
- [完整安装指南](INSTALL_ALFRED.md)
- [使用文档](README.md)
- [开发文档](DEVELOPMENT.md)

---

**Enjoy! 🎊**
