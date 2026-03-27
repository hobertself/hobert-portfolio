#!/usr/bin/env python3
"""
初始化实习经历转化Skill
"""

import os
import sys
from pathlib import Path

def init_skill(skill_name, output_dir):
    """创建Skill目录结构"""

    # 创建主目录
    skill_path = Path(output_dir) / skill_name
    skill_path.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (skill_path / "scripts").mkdir(exist_ok=True)
    (skill_path / "references").mkdir(exist_ok=True)
    (skill_path / "references" / "industry-terms").mkdir(exist_ok=True)
    (skill_path / "references" / "capability-frameworks").mkdir(exist_ok=True)
    (skill_path / "references" / "star-examples").mkdir(exist_ok=True)
    (skill_path / "references" / "quantification-patterns").mkdir(exist_ok=True)
    (skill_path / "assets").mkdir(exist_ok=True)
    (skill_path / "assets" / "resume-templates").mkdir(exist_ok=True)
    (skill_path / "assets" / "output-formats").mkdir(exist_ok=True)

    # 创建基础脚本文件
    scripts = [
        ("document-parser.py", """# 文档解析模块
# 用于解析各种格式的实习文档并提取关键信息

def parse_document(file_path):
    \"\"\"解析文档并返回结构化数据\"\"\"
    # TODO: 实现文档解析逻辑
    pass

def extract_key_info(content):
    \"\"\"提取关键信息：职位、公司、时间等\"\"\"
    # TODO: 实现信息提取逻辑
    pass
"""),
        ("star-processor.py", """# STAR法则处理模块
# 用于按STAR法则组织实习经历

def process_star_content(basic_info, duties, actions, results):
    \"\"\"处理STAR结构内容\"\"\"
    # TODO: 实现STAR处理逻辑
    pass

def quantify_results(results):
    \"\"\"量化成果，提取数据点\"\"\"
    # TODO: 实现量化逻辑
    pass
"""),
        ("keyword-optimizer.py", """# 关键词优化模块
# 用于行业术语和关键词优化

def optimize_industry_terms(content, industry):
    \"\"\"优化行业术语\"\"\"
    # TODO: 实现关键词优化逻辑
    pass

def get_industry_keywords(industry):
    \"\"\"获取行业关键词库\"\"\"
    # TODO: 实现关键词库加载
    pass
"""),
        ("capability-mapper.py", """# 能力矩阵映射模块
# 用于将经历映射到核心能力维度

def map_capabilities(content, framework):
    \"\"\"映射到能力框架\"\"\"
    # TODO: 实现能力映射逻辑
    pass

def get_capability_framework(framework_name):
    \"\"\"获取能力框架\"\"\"
    # TODO: 实现框架加载
    pass
"""),
        ("growth-tracker.py", """# 成长轨迹追踪模块
# 用于分析能力成长过程

def analyze_growth_trajectory(duties_timeline):
    \"\"\"分析成长轨迹\"\"\"
    # TODO: 实现成长轨迹分析
    pass

def generate_growth_narrative(growth_points):
    \"\"\"生成成长叙事\"\"\"
    # TODO: 实现成长叙事生成
    pass
""")
    ]

    for filename, content in scripts:
        with open(skill_path / "scripts" / filename, "w", encoding="utf-8") as f:
            f.write(content)

    # 创建初始的SKILL.md
    skill_md = """---
name: resume-project-experience
description: 将实习文档转化为高质量简历实习经历。按STAR法则组织内容，优化行业术语，映射核心能力，展示成长轨迹。当用户提到"简历"、"实习经历"、"工作经历"时使用。
---

# 实习经历转化 Skill

## 功能概述

将实习相关文档转化为高质量的简历实习经历，全面提升简历竞争力。

## 核心功能

1. **STAR法则结构化**
   - 背景（Situation）：描述工作背景和任务
   - 职责（Task）：说明具体职责和目标
   - 行动（Action）：陈述采取的行动，动词开头
   - 成果（Result）：量化成果和影响

2. **智能优化模块**
   - 行业术语和关键词优化
   - 能力矩阵映射展示
   - 成长轨迹呈现
   - 数据量化成果

3. **分模块处理流程**
   - 自动处理基础内容
   - 引导确认关键点
   - 确保输出质量

## 使用指南

### 基本使用

当用户提供实习文档时：
1. 首先解析文档内容
2. 按STAR法则组织信息
3. 优化行业术语和表达
4. 映射核心能力维度
5. 呈现成长轨迹
6. 确认并输出最终版本

### 输入格式支持

- Word文档 (.doc, .docx)
- PDF文件 (.pdf)
- Markdown文件 (.md)
- 纯文本文件 (.txt)

### 输出标准

所有输出必须：
- 使用STAR法则结构
- 包含量化数据
- 使用行业术语
- 展示能力矩阵
- 呈现成长轨迹

## 质量控制

- 每个模块完成后确认关键信息
- 确保数据准确性
- 保持专业语言风格
- 突出核心竞争力
"""

    with open(skill_path / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_md)

    # 创建基础的行业术语库
    industry_terms = {
        "互联网/科技": [
            "用户体验", "敏捷开发", "数据驱动", "产品迭代", "用户增长",
            "系统架构", "性能优化", "技术栈", "前后端", "API设计"
        ],
        "金融": [
            "风险管理", "资产配置", "投资分析", "量化模型", "财务报表",
            "合规审查", "风控体系", "信贷审批", "财富管理", "投资组合"
        ],
        "咨询": [
            "战略规划", "商业模式", "市场调研", "竞争分析", "解决方案",
            "客户访谈", "项目交付", "流程优化", "成本控制", "价值创造"
        ]
    }

    with open(skill_path / "references" / "industry-terms" / "basic_terms.txt", "w", encoding="utf-8") as f:
        for industry, terms in industry_terms.items():
            f.write(f"## {industry}\n")
            for term in terms:
                f.write(f"- {term}\n")
            f.write("\n")

    print(f"Skill '{skill_name}' 已创建成功！")
    print(f"路径: {skill_path}")
    print("\n接下来需要:")
    print("1. 完善各个模块的Python脚本实现")
    print("2. 添加更多的行业术语和能力框架")
    print("3. 准备STAR法则和量化模式的示例")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python init_skill.py <skill-name> <output-directory>")
        sys.exit(1)

    skill_name = sys.argv[1]
    output_dir = sys.argv[2]

    init_skill(skill_name, output_dir)