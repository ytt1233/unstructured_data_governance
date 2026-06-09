import re
import unicodedata
from schema.document import Document
from cleaners.base_cleaner import BaseCleaner
class TextCleaner(BaseCleaner):
    """
    基础文本清洗
    只负责通用文本规范化，不处理页眉页脚、PII、OCR噪声等
    """
    def __init__(self):
        # 可以配置一些规则，比如需要保留的空行数
        self.max_consecutive_blank_lines = 1

    def clean(self, document: Document) -> Document:
        """
        清洗 Document.raw_text 以及 Document.pages
        返回清洗后的 Document
        """
        #清洗整篇文本
        document.cleaned_text = self._clean_text(document.raw_text)
        #清洗每一页
        for page in document.pages:
            page.text = self._clean_text(
                page.text
            )
        #记录审计信息
        document.audit_trail.append(
            {
                "action": "text_clean",
                "operations": [
                "unicode_normalization",
                "remove_invisible_chars",
                "normalize_spaces",
                "normalize_blank_lines"
    ]
            }
        )

        document.processing_snapshots['after_text_clean'] = document.cleaned_text

        # print(f'基础文本清洗完成:\n{document.cleaned_text}')
        return document

    def _clean_text(self, text: str) -> str:
        """
        清洗文本
        """
        if not text:
            return text
        #1、Unicode标准化
        text = unicodedata.normalize("NFKC", text)
        # 2. 替换不可见字符（常见 OCR 垃圾字符）
        text = re.sub(r'[\x0c\x0b]', '', text)

        # 3. 去掉多余空格
        text = re.sub(r'[ \t]+', ' ', text)

        # 4. 去掉多余空行
        text = self._normalize_blank_lines(text)

        # 5. 去掉首尾多余空白
        text = text.strip()

        return text

    def _normalize_blank_lines(self, text: str) -> str:
        """
        将连续空行归一化为 self.max_consecutive_blank_lines
        """
        blank_line_pattern = r'(\n\s*){' + str(self.max_consecutive_blank_lines+1) + r',}'
        matches = re.findall(blank_line_pattern, text)
        return re.sub(blank_line_pattern, '\n'*self.max_consecutive_blank_lines, text)
