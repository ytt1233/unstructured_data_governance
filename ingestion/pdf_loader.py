from pathlib import Path

from ingestion.base_load import BaseLoader
from schema.document import Document


class PDFLoader(BaseLoader):

    def load(self, file_path: str) -> Document:

        path = Path(file_path)

        document = Document(
            doc_id=path.stem,
            file_name=path.name,
            file_type=path.suffix,
            file_path=str(path),
        )

        return document