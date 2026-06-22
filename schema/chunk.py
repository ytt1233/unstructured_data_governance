from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 可选字段
    source_doc_id: Optional[str] = None  # 来源文档
    page_num: Optional[int] = None       # 页码
    source_location: str = ""  #来源位置
    embedding: Optional[List[float]] = None  # 预留给后续RAG