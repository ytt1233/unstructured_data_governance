from typing import List
from collections import Counter
from schema.document import Document
from cleaners.base_cleaner import BaseCleaner
class HeaderFooterCleaner(BaseCleaner):
    """
    基于重复行的页眉/页脚清理器。
    原理：
        - 统计每页前几行和后几行的重复出现次数
        - 频率高的认为是页眉/页脚
        - 删除这些行
    """
    def __init__(self,n_lines: int=3,min_repeat: int=2):
        """
        :param n_lines: 每页前后取几行候选
        :param min_repeat: 出现次数>=min_repeat的才删除
        """
        self.n_lines = n_lines
        self.min_repeat = min_repeat

    def clean(self, document: Document) -> Document:
        """
        清洗 Document.pages 中的页眉页脚
        """
        if document.pages is None:
            return document 
        
        #收集页眉页脚候选
        header_candidates = []
        footer_candidates = []
        for page in document.pages:
            if not page.text: # 跳过空页面，防止 split 出错
                continue
            lines = page.text.split("\n")
            header_candidates.extend(lines[:self.n_lines])
            # print(f'页眉:{lines[:self.n_lines]}')
            footer_candidates.extend(lines[-self.n_lines:])
        # print(f'页眉列表:{header_candidates}')
        # print(f'页脚列表:{footer_candidates}')

        #统计重复次数
        header_counter  = Counter(header_candidates)
        footer_counter = Counter(footer_candidates)

        #确定需要删除的内容
        header_to_remove =  [line for line, count in header_counter.items() if count >= self.min_repeat]
        footer_to_remove = [line for line, count in footer_counter.items() if count >= self.min_repeat]
        # print(f"页眉页脚候选：{len(header_candidates)}行，{len(footer_candidates)}行")
        # print(f'页眉：{header_to_remove}')
        # print(f'页脚{footer_to_remove}')

        #清理页眉页脚
        cleaned_pages = []
        removed_headers = 0
        removed_footers = 0

        for page in document.pages:
            lines = page.text.split("\n")
            new_lines = []

            header_end = min(
                self.n_lines,
                len(lines)
            )

            footer_start = max(
                header_end,
                len(lines) - self.n_lines
            )

            header_lines = lines[:header_end]

            middle_lines = lines[header_end:footer_start]

            footer_lines = lines[footer_start:]

            #删除页眉
            for line in header_lines:

                if line in header_to_remove:
                    removed_headers += 1
                else:
                    new_lines.append(line)
            #正文
            new_lines.extend(middle_lines)

            # 删除页脚
            for line in footer_lines:

                if line in footer_to_remove:
                    removed_footers += 1
                else:
                    new_lines.append(line)

            page.text = "\n".join(new_lines)


        #更新 cleaned_text
        document.cleaned_text = "\n".join(page.text for page in document.pages)


        # 记录审计信息
        document.audit_trail.append(
            {
                "action": "header_footer_clean",
                "removed_headers": removed_headers,
                "removed_footers": removed_footers,
                "total_pages": len(document.pages),
            }
        )

        document.processing_snapshots["after_header_footer"] = document.cleaned_text
        # print("Header Footer Cleaner:")
        # for page in document.pages:
        #     print(page.text)
        #     print("*"*50)
        return document
            