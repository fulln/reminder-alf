#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alfred 工作流入口脚本
"""

import sys
import os
import json

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# 添加 src 目录到 Python 路径（最优先）
sys.path.insert(0, parent_dir)

try:
    # 现在可以导入 src 包的模块
    from src.workflow.input_handler import InputHandler
    from src.workflow.command_router import CommandRouter
    from src.workflow.handlers import (
        handle_config_command,
        handle_parse_command,
        handle_delete_command,
        handle_list_command,
        handle_help_command,
        handle_clean_command,
    )
    from src.utils.logger import get_logger

    logger = get_logger(__name__)

    def main():
        """主入口"""
        try:
            # 获取输入
            query = sys.argv[1] if len(sys.argv) > 1 else ""

            # 解析输入
            input_handler = InputHandler()
            parsed_input = input_handler.parse(query)

            # 路由命令
            command_router = CommandRouter()
            command_router.register("parse", handle_parse_command)
            command_router.register("config", handle_config_command)
            command_router.register("delete", handle_delete_command)
            command_router.register("list", handle_list_command)
            command_router.register("clean", handle_clean_command)
            command_router.register("help", handle_help_command)
            command_router.register_default(handle_help_command)

            # 执行命令
            feedback = command_router.route(parsed_input)

            # 输出 Alfred JSON
            print(feedback.to_json())

        except Exception as e:
            logger.error(f"Main error: {e}", exc_info=True)
            # 输出错误 JSON
            error_json = {
                "items": [{
                    "title": "❌ Error",
                    "subtitle": str(e),
                    "valid": False
                }]
            }
            print(json.dumps(error_json))
            sys.exit(1)

    if __name__ == "__main__":
        main()

except Exception as e:
    # 如果导入失败，输出调试信息
    import traceback
    error_json = {
        "items": [{
            "title": "❌ Import Error",
            "subtitle": str(e),
            "valid": False
        }]
    }
    print(json.dumps(error_json))
    sys.exit(1)




