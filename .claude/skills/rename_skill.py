#!/usr/bin/env python3
"""
Skill重命名工具
"""

import os
import shutil
from pathlib import Path

def rename_skill(old_name, new_name):
    """重命名Skill项目"""

    # 检查源目录是否存在
    old_path = Path(".") / old_name
    if not old_path.exists():
        print(f"错误：源目录 '{old_name}' 不存在")
        return False

    # 检查目标目录是否已存在
    new_path = Path(".") / new_name
    if new_path.exists():
        print(f"错误：目标目录 '{new_name}' 已存在")
        return False

    try:
        # 重命名目录
        shutil.move(str(old_path), str(new_path))
        print(f"成功：'{old_name}' -> '{new_name}'")

        # 更新内部引用（如果有需要）
        # TODO: 如果有内部文件需要更新路径，可以在这里处理

        return True
    except Exception as e:
        print(f"重命名失败：{str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python rename_skill.py <old-name> <new-name>")
        sys.exit(1)

    old_name = sys.argv[1]
    new_name = sys.argv[2]

    rename_skill(old_name, new_name)