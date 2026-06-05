from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Metadata:

    # 通用 metadata
    common: Dict[str, Any] = field(default_factory=dict)

    # 领域 metadata
    domain: Dict[str, Any] = field(default_factory=dict)