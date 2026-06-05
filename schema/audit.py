from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditRecord:
    timestamp: datetime

    stage: str

    rule_name: str

    action: str

    message: str

    severity: str