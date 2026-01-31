# 🚀 Reminder-Alf 快速开始指南

## 安装

### 一键安装

```bash
cd /path/to/reminder-alf

# 安装依赖和 ral 命令
python3.11 -m pip install -e .

# 配置 AI（推荐 DeepSeek，中文优化，性价比高）
ral config set deepseek sk-YOUR_API_KEY deepseek-chat

# 开始使用！
ral parse "明天下午3点开会"
```

**就这么简单！**✅

### 验证安装

```bash
# 检查 ral 命令是否可用
ral help

# 如果提示找不到命令，需要重新加载 shell
source ~/.zshrc
# 或
hash -r
```

---

## 使用方式

### 方式 1：CLI 命令行

```bash
# 创建事件/提醒
ral parse "Meeting tomorrow at 2pm"
ral parse "明天下午3点开会"

# 查看配置
ral config status

# 列出最近创建的项目
ral list

# 帮助
ral help
```

### 方式 2：Raycast 扩展（可视化界面）

```bash
cd /path/to/reminder-alf/raycast-extension
npm install
npm run dev
```

然后在 Raycast 中搜索 **"Reminder Alf"**。

---

## AI 配置

### 获取 API 密钥

- **DeepSeek**: https://platform.deepseek.com/
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

### 配置命令

```bash
# DeepSeek (推荐中文，性价比高)
ral config set deepseek sk-YOUR_API_KEY deepseek-chat

# OpenAI (推荐 GPT-4)
ral config set openai sk-YOUR_API_KEY gpt-4

# 或 GPT-3.5 (更便宜)
ral config set openai sk-YOUR_API_KEY gpt-3.5-turbo

# 验证配置
ral config status
```

---

## 系统权限

首次使用时，macOS 会请求以下权限：

- **日历权限** - 创建日历事件时弹出
- **提醒事项权限** - 创建提醒时弹出

点击 **OK** 授予权限即可。

**如果拒绝了权限，手动授权：**
```
System Settings → Privacy & Security → Calendar/Reminders
→ 勾选 Terminal 或 Python
```

---

## 使用示例

### 创建日历事件

```bash
ral parse "Meeting tomorrow at 2pm"
ral parse "明天下午3点开会"
ral parse "下周一上午10点团队站会"
```

### 创建提醒

```bash
ral parse "Remind me to buy milk"
ral parse "提醒我买牛奶"
ral parse "周五前提交报告"
```

### 管理项目

```bash
# 列出最近 10 个项目
ral list

# 列出最近 20 个项目
ral list 20

# 删除特定项目
ral delete <item-id>

# 删除所有项目
ral delete all

# 删除 7 天前的项目
ral delete old 7
```

---

## 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `ral parse <文本>` | 解析并创建 | `ral parse "Meeting at 2pm"` |
| `ral config status` | 查看配置 | - |
| `ral config set` | 设置配置 | `ral config set openai sk-... gpt-4` |
| `ral config endpoint` | 设置自定义端点 | `ral config endpoint https://api.example.com` |
| `ral config timeout` | 设置超时时间 | `ral config timeout 30` |
| `ral config tokens` | 设置最大 Tokens | `ral config tokens 2000` |
| `ral list [N]` | 列出最近 N 个项目 | `ral list 20` |
| `ral delete <id>` | 删除特定项目 | `ral delete event-123` |
| `ral delete all` | 删除所有 | - |
| `ral delete old [N]` | 删除 N 天前的 | `ral delete old 7` |
| `ral help` | 显示帮助 | - |

---

## 故障排除

### 问题：找不到 ral 命令

```bash
# 重新安装
python3.11 -m pip install -e .

# 刷新 shell
hash -r
# 或
source ~/.zshrc
```

### 问题：找不到 python3.11

```bash
# 安装 Python 3.11
brew install python@3.11

# 重新安装
python3.11 -m pip install -e .
```

### 问题：AI 解析失败

```bash
# 检查配置
ral config status

# 重新配置
ral config delete
ral config set deepseek sk-NEW_KEY deepseek-chat
```

---

## 配置文件位置

| 内容 | 位置 |
|------|------|
| 配置文件 | `~/.config/reminder-alf/config.json` |
| 追踪数据 | `~/.config/reminder-alf/tracking.json` |
| API 密钥 | macOS Keychain (service: `reminder-alf`) |

---

## 更多文档

- [Raycast 安装指南](INSTALL_RAYCAST.md)
- [DeepSeek 配置](DEEPSEEK.md)
- [开发文档](DEVELOPMENT.md)

---

**Enjoy! 🎊**
