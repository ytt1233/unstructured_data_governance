from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Rule:
    rule_id: str

    rule_name: str

    validator: str

    enabled: bool = True

    parameters: Dict[str, Any] = None