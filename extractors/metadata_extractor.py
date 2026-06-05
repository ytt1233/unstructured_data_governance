from .base_extractor import BaseExtractor
from schema.document import Document
import re
class MetadataExtractor(BaseExtractor):
    def extract(self, document: Document) -> Document:
        """
        提取 Document 的业务元数据（是什么）
        """
        text = document.raw_text or ""
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        # =========================
        # 1. title 提取
        # =========================
        title = self._extract_title_from_layout(document)

        if not title:
            title = self._extract_title(lines)

        # =========================
        # 2. category 推断
        # =========================
        category = self._infer_category(text)

        # =========================
        # 写入 domain metadata
        # =========================
        document.metadata.domain.update(
            {
                "title": title,
                "category": category,
            }
        )

        # =========================
        # audit
        # =========================
        document.audit_trail.append(
            {
                "action": "metadata_extract"
            }
        )

        return document
    
    # =========================
    # 功能：提取title
    # 规则：
    # 1. 字体为最大字体95%的行
    # 2. 取其中排在最靠上的3条
    # 3. 拼接标题
    # =========================
    def _extract_title_from_layout(self, document):

        layout = document.first_page_layout

        if not layout:
            return None
        
        #找到候选项
        candidates = []

        for block in layout.get("blocks", []):

            if block.get("type") != 0:
                continue

            for line in block.get("lines", []):

                line_text = ""
                font_size = 0
                y = None

                for span in line.get("spans", []):

                    text = span.get("text", "").strip()

                    if not text:
                        continue

                    line_text += text

                    font_size = max(
                        font_size,
                        span.get("size", 0)
                    )#遍历一行中所有片段时，记录最大字号

                    if y is None:
                        y = span.get("bbox", [0, 0, 0, 0])[1]

                if line_text:

                    candidates.append(
                        {
                            "text": line_text,
                            "font_size": font_size,
                            "y": y
                        }
                    )

        #过滤候选项中长度过短的
        filtered = []
        # print(f'candidates:{candidates}')

        for item in candidates:

            text = item["text"].strip()

            if len(text) < 4:
                continue

            filtered.append(item)

        if not filtered:
            return None

        # 找最大字号
        max_font = max(
            item["font_size"]
            for item in filtered
        )

        # 保留接近最大字号的候选
        title_candidates = [
            item
            for item in filtered
            if item["font_size"] >= max_font * 0.95
        ]

        if not title_candidates:
            return None
        
        # 按页面位置排序
        title_candidates.sort(
            key=lambda x: x["y"]
        )

        # 标题数量限制，否则可能取到正文
        title_candidates = title_candidates[:3]

        #拼接标题
        title = "\n".join(
            item["text"]
            for item in title_candidates
        )

        return title.strip()    

    def _title_score(self, item):

        text = item["text"]

        font_size = item["font_size"]

        y = item["y"] or 0

        score = 0

        # 1. 字体越大越好
        score += font_size * 20

        # 2. 越靠上越好
        score += max(0, 1000 - y)

        # 3. 长度适中
        length = len(text)

        if 5 <= length <= 50:
            score += 100

        elif length <= 80:
            score += 50

        # 4. 全数字扣分
        if text.isdigit():
            score -= 300

        # 5. 标点过多扣分

        punctuation_count = sum(
            1
            for c in text
            if c in "：:;；,，。()（）[]【】"
        )

        score -= punctuation_count * 10
        # print(f'text:{text} score:{score}')
        return score
                
    # =========================
    # title 按规则提取策略
    # =========================
    def _extract_title(self, lines):
        if not lines:
            return ""

        first_line = lines[0]
        # 规则1：长度过滤
        if 5 < len(first_line) < 60:
            return first_line

        # 规则2：找更像标题的行
        for line in lines[:5]:
            if 5 < len(line) < 60 and not re.search(r"\d{3,}", line):
                return line

        return lines[0] if lines else ""

    # =========================
    # category 简单分类
    # =========================
    def _infer_category(self, text):

        if "规划" in text or "strategy" in text.lower():
            return "规划"

        if "合同" in text or "agreement" in text.lower():
            return "法律"

        if "报告" in text or "analysis" in text.lower():
            return "报告"

        return "未知"