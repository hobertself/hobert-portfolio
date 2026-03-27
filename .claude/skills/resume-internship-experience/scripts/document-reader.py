# 文档读取模块
# 专门用于从各类实习文档中读取和解析信息

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class DocumentReader:
    """文档读取器，支持多种格式"""

    def __init__(self):
        self.supported_formats = ['.docx', '.pdf', '.md', '.txt', '.doc']

    def read_document(self, file_path: str) -> Dict[str, Any]:
        """
        读取文档并返回结构化数据

        Args:
            file_path: 文档路径

        Returns:
            包含文档结构和内容的字典
        """
        file_path = Path(file_path)

        # 检查文件是否存在
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 检查文件格式
        file_extension = file_path.suffix.lower()
        if file_extension not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {file_extension}")

        # 根据文件类型读取
        if file_extension == '.pdf':
            content = self._read_pdf(file_path)
        elif file_extension in ['.doc', '.docx']:
            content = self._read_word(file_path)
        elif file_extension == '.md':
            content = self._read_markdown(file_path)
        else:
            content = self._read_text(file_path)

        # 解析文档结构
        structured_data = self._parse_document_structure(content)

        return {
            'file_path': str(file_path),
            'file_type': file_extension,
            'content': content,
            'structured_data': structured_data,
            'basic_info': self._extract_basic_info(structured_data)
        }

    def _read_pdf(self, file_path: Path) -> str:
        """读取PDF文件"""
        try:
            import PyPDF2
            content = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
            return content
        except ImportError:
            raise ImportError("需要安装PyPDF2库来读取PDF文件: pip install PyPDF2")

    def _read_word(self, file_path: Path) -> str:
        """读取Word文档"""
        try:
            import docx
            doc = docx.Document(file_path)
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
            return content
        except ImportError:
            raise ImportError("需要安装python-docx库来读取Word文件: pip install python-docx")

    def _read_markdown(self, file_path: Path) -> str:
        """读取Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"读取Markdown文件失败: {str(e)}")

    def _read_text(self, file_path: Path) -> str:
        """读取文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"读取文本文件失败: {str(e)}")

    def _parse_document_structure(self, content: str) -> Dict[str, Any]:
        """解析文档结构"""
        # 按段落分割内容
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

        # 检测可能的标题
        headers = []
        body_content = []

        for para in paragraphs:
            # 简单的标题检测（包含"实习"、"工作"、"项目"等关键词）
            if (len(para) < 50 and
                any(keyword in para for keyword in ['实习', '工作', '项目', '职责', '成果', '经历'])):
                headers.append(para)
            else:
                body_content.append(para)

        return {
            'headers': headers,
            'paragraphs': paragraphs,
            'body_content': body_content
        }

    def _extract_basic_info(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取基本信息"""
        content = ' '.join(structured_data['paragraphs'])

        # 提取公司名称
        company_patterns = [
            r'在(.+?)公司',
            r'(.+?)有限公司',
            r'(.+?)集团',
            r'(.+?)科技',
            r'(.+?)网络'
        ]

        company = None
        for pattern in company_patterns:
            match = re.search(pattern, content)
            if match:
                company = match.group(1)
                break

        # 提取职位
        position_patterns = [
            r'(.+?)实习生',
            r'(.+?)助理',
            r'(.+?)工程师',
            r'(.+?)分析师',
            r'(.+?)顾问'
        ]

        position = None
        for pattern in position_patterns:
            match = re.search(pattern, content)
            if match:
                position = match.group(1)
                break

        # 提取时间
        time_patterns = [
            r'(\d{4})\.(\d{1,2})-(\d{4})\.(\d{1,2})',
            r'(\d{4})年(\d{1,2})月-(\d{4})年(\d{1,2})月',
            r'(\d{4})\.(\d{1,2})至今',
            r'(\d{4})年(\d{1,2})月至今'
        ]

        time_range = None
        for pattern in time_patterns:
            match = re.search(pattern, content)
            if match:
                time_range = match.group(0)
                break

        # 提取工作内容关键词
        work_keywords = []
        keyword_patterns = [
            ('负责', 3),
            ('参与', 2),
            ('协助', 2),
            ('完成', 2),
            ('开发', 3),
            ('设计', 3),
            ('分析', 2),
            ('测试', 2),
            ('管理', 2),
            ('优化', 2)
        ]

        for keyword, weight in keyword_patterns:
            if keyword in content:
                work_keywords.extend([keyword] * weight)

        # 去重并按权重排序
        work_keywords = list(set(work_keywords))

        return {
            'company': company,
            'position': position,
            'time_range': time_range,
            'work_keywords': work_keywords,
            'content_length': len(content)
        }

def extract_internship_info_from_document(file_path: str) -> Dict[str, Any]:
    """
    从文档中提取实习信息的主函数

    Args:
        file_path: 文档路径

    Returns:
        包含实习信息的结构化数据
    """
    reader = DocumentReader()
    document_data = reader.read_document(file_path)

    # 进一步提取具体的工作内容和成果
    content = document_data['content']

    # 提取具体工作内容
    work_content = extract_work_content(content)

    # 提取成果数据
    achievements = extract_achievements(content)

    # 确定行业
    industry = identify_industry(content)

    # 更新结构化数据
    document_data['internship_info'] = {
        'work_content': work_content,
        'achievements': achievements,
        'industry': industry
    }

    return document_data

def extract_work_content(content: str) -> List[str]:
    """提取工作内容"""
    work_items = []

    # 按句子分割
    sentences = re.split(r'[。！？\n]', content)

    for sentence in sentences:
        sentence = sentence.strip()
        if (len(sentence) > 10 and
            any(keyword in sentence for keyword in ['负责', '参与', '协助', '完成', '开发', '设计', '分析', '测试'])):
            work_items.append(sentence)

    return work_items[:10]  # 取前10条

def extract_achievements(content: str) -> List[str]:
    """提取成果"""
    achievements = []

    # 查找包含数字的句子
    sentences = re.split(r'[。！？\n]', content)

    for sentence in sentences:
        sentence = sentence.strip()
        if (len(sentence) > 10 and
            re.search(r'\d+%', sentence) or  # 包含百分比
            re.search(r'\d+万', sentence) or  # 包含万
            re.search(r'\d+亿', sentence) or  # 包含亿
            re.search(r'\d+倍', sentence) or  # 包含倍
            re.search(r'\d+', sentence) and ('提升' in sentence or '降低' in sentence or '增加' in sentence)):
            achievements.append(sentence)

    return achievements[:8]  # 取前8条

def identify_industry(content: str) -> str:
    """识别所属行业"""
    industry_keywords = {
        '互联网/科技': ['互联网', '科技', '软件', '网络', '技术', '产品', '数据', '算法', '开发'],
        '金融': ['银行', '证券', '基金', '保险', '金融', '投资', '财务', '风控'],
        '咨询': ['咨询', '战略', '管理', '市场', '调研', '分析', '方案'],
        '教育': ['教育', '培训', '学校', '学生', '课程', '教学']
    }

    content_lower = content.lower()
    industry_scores = {}

    for industry, keywords in industry_keywords.items():
        score = sum(content_lower.count(keyword) for keyword in keywords)
        industry_scores[industry] = score

    # 返回得分最高的行业
    if max(industry_scores.values()) > 0:
        return max(industry_scores, key=industry_scores.get)
    else:
        return '其他'

# 使用示例
if __name__ == "__main__":
    # 测试文档读取
    test_file = "test_internship.docx"
    if os.path.exists(test_file):
        try:
            data = extract_internship_info_from_document(test_file)
            print("基本信息:")
            print(f"公司: {data['basic_info']['company']}")
            print(f"职位: {data['basic_info']['position']}")
            print(f"时间: {data['basic_info']['time_range']}")
            print(f"行业: {data['internship_info']['industry']}")
            print("\n工作内容:")
            for item in data['internship_info']['work_content'][:3]:
                print(f"- {item}")
            print("\n成果:")
            for item in data['internship_info']['achievements'][:3]:
                print(f"- {item}")
        except Exception as e:
            print(f"读取文档失败: {str(e)}")
    else:
        print("测试文件不存在")