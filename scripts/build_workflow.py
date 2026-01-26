#!/usr/bin/env python3
"""
生成 Alfred 工作流包 (.alfredworkflow)

使用方法:
    python3 build_workflow.py

输出:
    Reminder-Alf.alfredworkflow (可以直接导入 Alfred)
"""

import os
import json
import shutil
import sys
from pathlib import Path
import zipfile

def create_workflow_package():
    """创建 Alfred 工作流包"""

    project_root = Path(__file__).parent
    workflow_dir = project_root / "workflow"
    output_file = project_root / "Reminder-Alf.alfredworkflow"

    print("🔨 生成 Reminder-Alf 工作流包...")
    print()

    # 检查必要文件
    plist_file = workflow_dir / "info.plist"
    if not plist_file.exists():
        print("❌ 错误: workflow/info.plist 不存在")
        sys.exit(1)

    run_script = workflow_dir / "run_script.py"
    if not run_script.exists():
        print("❌ 错误: workflow/run_script.py 不存在")
        sys.exit(1)

    # 创建临时工作目录
    temp_dir = project_root / ".workflow_temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    try:
        print("📦 打包工作流文件...")

        # 复制 info.plist 到根目录
        shutil.copy2(plist_file, temp_dir / "info.plist")

        # 复制 run_script.py 到根目录
        shutil.copy2(run_script, temp_dir / "run_script.py")

        # 复制 icon.png 如果存在
        icon_file = workflow_dir / "icon.png"
        if icon_file.exists():
            shutil.copy2(icon_file, temp_dir / "icon.png")

        # 复制 src 目录到临时目录
        print("📦 复制 Python 源代码...")
        src_temp = temp_dir / "src"
        shutil.copytree(project_root / "src", src_temp)

        # 创建 README
        readme = temp_dir / "README.txt"
        readme.write_text("""Reminder-Alf - AI-powered Calendar and Reminder Management

Installation:
1. Double-click this workflow to import into Alfred
2. Configure AI: ral config set openai sk-YOUR_KEY gpt-4
3. Start using: ral Meeting tomorrow at 2pm

For more help: ral help
""")

        # 创建 ZIP 包
        print("🎁 创建 .alfredworkflow 文件...")
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(temp_dir):
                # 排除 __pycache__ 和 .pyc 文件
                dirs[:] = [d for d in dirs if d != '__pycache__']

                for file in files:
                    if file.endswith('.pyc'):
                        continue
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zf.write(file_path, arcname)

        print()
        print("=" * 50)
        print("✅ 工作流包创建成功！")
        print("=" * 50)
        print()
        print(f"📁 文件位置: {output_file}")
        print(f"📊 文件大小: {output_file.stat().st_size / 1024:.1f} KB")
        print()
        print("🚀 下一步:")
        print("  1. 双击 Reminder-Alf.alfredworkflow 文件")
        print("  2. Alfred 会自动导入工作流")
        print("  3. 运行: ral config set openai sk-YOUR_KEY gpt-4")
        print("  4. 开始使用: ral Meeting tomorrow at 2pm")
        print()

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    create_workflow_package()
