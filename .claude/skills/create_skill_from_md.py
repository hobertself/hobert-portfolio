#!/usr/bin/env python3
"""
根据skill.md文件创建完整skill项目
"""

import re
import os
from pathlib import Path

def parse_yaml_frontmatter(content):
    """解析YAML frontmatter"""
    yaml_match = re.search(r'---\s*\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        return {}

    yaml_content = yaml_match.group(1)
    # 简单解析key: value格式
    metadata = {}
    for line in yaml_content.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # 移除引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            metadata[key] = value
    return metadata

def create_skill_from_md(skill_content, output_dir):
    """从skill.md内容创建skill项目"""

    # 解析YAML frontmatter
    metadata = parse_yaml_frontmatter(skill_content)
    if not metadata:
        raise ValueError("skill.md文件缺少YAML frontmatter")

    # 获取skill名称和描述
    skill_name = metadata.get('name', 'unknown-skill')
    skill_description = metadata.get('description', 'No description')

    # 创建skill目录
    skill_path = Path(output_dir) / skill_name
    skill_path.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (skill_path / "references").mkdir(exist_ok=True)
    (skill_path / "assets").mkdir(exist_ok=True)

    # 写入SKILL.md
    with open(skill_path / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_content)

    # 创建其他必要的文件
    _create_helper_files(skill_path, metadata)

    return skill_path

def _create_helper_files(skill_path, metadata):
    """创建辅助文件"""
    skill_name = metadata.get('name', 'unknown-skill')
    skill_description = metadata.get('description', 'No description')

    # 创建README.md
    readme_content = f"""# {skill_name} Skill

{skill_description}

## 使用说明

### 触发条件

{GetTriggerConditions(skill_path / "SKILL.md")}

### 工作流程

{GetWorkflowSteps(skill_path / "SKILL.md")}

## 输出示例

{GetExampleOutput(skill_path / "SKILL.md")}

## 文件结构

```
{skill_name}/
├── SKILL.md          # 主要技能定义
├── README.md         # 说明文档
├── references/       # 参考资料（可选）
└── assets/           # 资源文件（可选）
```

## 贡献

欢迎提交Issue和Pull Request来改进这个Skill。
"""

    with open(skill_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

def GetTriggerConditions(skill_md_path):
    """获取触发条件"""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 查找触发条件部分
        trigger_match = re.search(r'## 触发条件\s*\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if trigger_match:
            return trigger_match.group(1).strip()
    return "待添加触发条件说明"

def GetWorkflowSteps(skill_md_path):
    """获取工作流程"""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 查找工作流程部分
        workflow_match = re.search(r'## 工作流程\s*\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if workflow_match:
            return workflow_match.group(1).strip()
    return "待添加工作流程说明"

def GetExampleOutput(skill_md_path):
    """获取输出示例"""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 查找示例部分
        example_match = re.search(r'## 示例\s*\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if example_match:
            return "```\n" + example_match.group(1).strip() + "\n```"
    return "待添加输出示例"

def create_skill_from_file(input_file_path, output_dir):
    """从文件创建skill项目"""
    with open(input_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return create_skill_from_md(content, output_dir)

if __name__ == "__main__":
    print("创建Skill项目选项：")
    print("1. 从粘贴的内容创建")
    print("2. 从文件创建")

    choice = input("请选择（1/2）：").strip()

    if choice == "1":
        # 从粘贴的内容创建
        print("\n请输入skill.md文件内容（输入'END'结束）：")
        skill_content = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            skill_content.append(line)
        skill_content = "\n".join(skill_content)

        output_dir = input("\n请输入输出目录路径（默认：.）") or "."

        try:
            skill_path = create_skill_from_md(skill_content, output_dir)
            print(f"\nSkill项目创建成功！")
            print(f"路径：{skill_path}")
        except Exception as e:
            print(f"创建失败：{str(e)}")

    elif choice == "2":
        # 从文件创建
        input_file = input("\n请输入skill.md文件路径：").strip()
        output_dir = input("请输入输出目录路径（默认：.）") or "."

        try:
            skill_path = create_skill_from_file(input_file, output_dir)
            print(f"\nSkill项目创建成功！")
            print(f"路径：{skill_path}")
        except Exception as e:
            print(f"创建失败：{str(e)}")

    else:
        print("无效选择")