from dataclasses import dataclass, field
from typing import List, Dict, Any
from schema.metadata import Metadata
from schema.chunk import Chunk

@dataclass
class Block:
    block_id: str
    text: str
    block_type: str   # paragraph/table/header/footer
    page_num: int
    bbox: tuple | None = None

@dataclass
class Page:
    page_num: int
    text: str
    blocks: List[Block] = field(default_factory=list)

@dataclass
class Document:
    doc_id: str
    file_name: str
    file_type: str
    file_path: str

    raw_text: str = ""
    cleaned_text: str = ""


    pages: List[Page] = field(default_factory=list)

    metadata: Metadata = field(default_factory=Metadata)#描述固有属性

    audit_trail: List[Any] = field(default_factory=list)

    chunks: List[Chunk] = field(default_factory=list)

    validation_results: Dict = field(default_factory=dict)

    metrics: dict = field(default_factory=dict)#描述治理结果

    first_page_layout: dict = field(default_factory=dict)

    sample_records: List[Dict] = field(default_factory=list)

    processing_snapshots: dict = field(default_factory=dict)