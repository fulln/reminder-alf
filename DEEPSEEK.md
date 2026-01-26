# DeepSeek 配置指南

## 快速配置 DeepSeek

### 方法 1：使用默认 DeepSeek 端点

```bash
ral config set deepseek sk-YOUR_DEEPSEEK_API_KEY deepseek-chat
```

### 方法 2：自定义端点（如果你有自己的部署）

```bash
# 先设置环境变量
export REMINDER_ALF_DEEPSEEK_ENDPOINT=https://your-deepseek-endpoint.com/v1

# 然后配置
ral config set deepseek sk-YOUR_API_KEY deepseek-chat
```

### 方法 3：使用 custom 提供商（完全自定义）

```bash
# 设置自定义端点
export REMINDER_ALF_CUSTOM_ENDPOINT=https://api.deepseek.com/v1

# 配置
ral config set custom sk-YOUR_API_KEY deepseek-chat
```

## DeepSeek API 密钥获取

1. 访问 DeepSeek 官网：https://platform.deepseek.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制密钥（格式：`sk-...`）

## 推荐模型

- **deepseek-chat** - 通用对话模型（推荐）
- **deepseek-coder** - 代码理解模型

## 完整配置示例

```bash
# 1. 配置 DeepSeek
ral config set deepseek sk-abc123xyz456 deepseek-chat

# 2. 检查状态
ral config status

# 3. 测试
ral Meeting tomorrow at 2pm
ral 明天下午3点开会
```

## 价格对比（参考）

| 提供商 | 价格 | 特点 |
|--------|------|------|
| DeepSeek | ¥ 便宜 | 中文优化，性价比高 |
| OpenAI GPT-4 | $$$ 贵 | 最强性能 |
| OpenAI GPT-3.5 | $ 便宜 | 性价比好 |

## 故障排除

### API Key 无效

```bash
# 删除旧配置
ral config delete deepseek

# 重新配置
ral config set deepseek sk-NEW_KEY deepseek-chat
```

### 端点错误

```bash
# 检查端点设置
echo $REMINDER_ALF_DEEPSEEK_ENDPOINT

# 清除环境变量
unset REMINDER_ALF_DEEPSEEK_ENDPOINT

# 使用默认端点
ral config set deepseek sk-YOUR_KEY deepseek-chat
```

## 环境变量配置

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# DeepSeek 配置
export REMINDER_ALF_DEEPSEEK_ENDPOINT=https://api.deepseek.com/v1

# 或自定义端点
export REMINDER_ALF_CUSTOM_ENDPOINT=https://your-endpoint.com/v1
```

然后重新加载：
```bash
source ~/.zshrc
```

## 测试配置

```bash
# 英文测试
ral Meeting with John tomorrow at 2pm in Room 305

# 中文测试
ral 明天下午3点在会议室开项目评审会

# 提醒测试
ral 提醒我周五前提交报告
```

## 支持的所有提供商

| 提供商 | 配置命令 | 说明 |
|--------|---------|------|
| **DeepSeek** | `ral config set deepseek sk-... deepseek-chat` | 推荐，中文优化 |
| OpenAI | `ral config set openai sk-... gpt-4` | 最强，较贵 |
| Custom | `ral config set custom sk-... model-name` | 任意 OpenAI 兼容端点 |
