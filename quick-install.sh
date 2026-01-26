#!/bin/bash
# 一键完整安装脚本
# 使用: bash quick-install.sh

set -e

echo "🚀 Reminder-Alf 一键安装"
echo "================================"
echo ""

# 检查 Python 3
echo "1️⃣  检查 Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未找到"
    echo ""
    echo "安装方法:"
    echo "  brew install python3"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "   ✅ 找到: $PYTHON_VERSION"
echo ""

# 获取项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 安装 Python 依赖
echo "2️⃣  安装 Python 依赖..."
python3 -m pip install -e . -q 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ 依赖安装完成"
else
    echo "   ❌ 依赖安装失败"
    exit 1
fi
echo ""

# 运行测试
echo "3️⃣  运行测试..."
python3 -m pytest tests/ -q --tb=no 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ 所有测试通过"
else
    echo "   ⚠️  某些测试失败 (可以继续)"
fi
echo ""

# 创建工作流包
echo "4️⃣  生成 Alfred 工作流包..."
python3 build_workflow.py
echo ""

# 创建配置目录
echo "5️⃣  创建配置目录..."
CONFIG_DIR="$HOME/Library/Application Support/Alfred/Workflow Data/com.reminder-alf"
mkdir -p "$CONFIG_DIR/logs"
echo "   ✅ 目录创建完成: $CONFIG_DIR"
echo ""

# 完成提示
echo "================================"
echo "✅ 安装完成！"
echo "================================"
echo ""
echo "📦 下一步:"
echo ""
echo "1️⃣  打开工作流文件:"
echo "    open Reminder-Alf.alfredworkflow"
echo ""
echo "   或者双击文件导入 Alfred"
echo ""
echo "2️⃣  获取 API 密钥:"
echo "    - OpenAI: https://platform.openai.com/api-keys"
echo "    - DeepSeek: https://platform.deepseek.com/"
echo ""
echo "3️⃣  配置 AI 供应商:"
echo "    ral config set openai sk-YOUR_KEY gpt-4"
echo ""
echo "4️⃣  开始使用:"
echo "    ral Meeting tomorrow at 2pm"
echo "    ral 明天下午3点开会"
echo ""
echo "📚 更多帮助: ral help"
echo ""
