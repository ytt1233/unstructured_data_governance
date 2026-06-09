from ingestion.pdf_loader import PDFLoader

from parser.pdf_parser import PDFParser

from extractors.metadata_extractor import MetadataExtractor

from cleaners.text_cleaner import TextCleaner
from cleaners.header_footer_cleaner import HeaderFooterCleaner
from cleaners.pii_cleaner import PiiCleaner
from cleaners.ocr_noise_cleaner import OCRNoiseCleaner

from chunkers.fixed_chunker import FixedChunker

from validators.metadata_validator import MetadataValidator
from validators.content_length_validator import ContentLengthValidator
from validators.ocr_noise_validator import OCRNoiseValidator
from validators.header_footer_validators import HeaderFooterValidator
from validators.chunk_validator import ChunkValidator
from validators.pii_validator import PiiValidator

from metrics.cleaning_metric import CleaningMetric
from metrics.text_quality_metric import TextQualityMetric
from metrics.header_footer_metric import HeaderFooterMetric
from metrics.pii_metric import PiiMetric
from metrics.ocr_noise_metric import OCRNoiseMetric
from report.report_generator import ReportGenerator

from exporters.json_exporter import JsonExporter


class PipelineManager:

    def __init__(self):

        # ========= Loader / Parser =========
        self.loader = PDFLoader()
        self.parser = PDFParser()

        # ========= Extractors =========
        self.extractors = [
            MetadataExtractor()
        ]

        # ========= Cleaners =========
        self.cleaners = [
            TextCleaner(),
            HeaderFooterCleaner(n_lines=3, min_repeat=2),
            OCRNoiseCleaner(),
            PiiCleaner()
        ]

        # ========= Chunkers =========
        self.chunkers = [
            FixedChunker(chunk_size=500)
        ]

        # ========= Validators =========
        self.validators = [
            MetadataValidator(),
            ContentLengthValidator(min_length=100),
            OCRNoiseValidator(),
            HeaderFooterValidator(),
            ChunkValidator(),
            PiiValidator()
        ]

        # ========= Metrics =========
        self.metrics = [
            TextQualityMetric(),
            HeaderFooterMetric(),
            PiiMetric(),
            OCRNoiseMetric(),
        ]

        # ========= Report =========
        self.reporter = ReportGenerator()

        # ========= Export =========
        self.exporter = JsonExporter()
    def run(self, file_path: str):

        # =========================
        # 1. LOAD
        # =========================
        document = self.loader.load(file_path)
        # document.audit_trail.append({"step": "load"})

        print("Loaded:", document.file_name)

        # =========================
        # 2. PARSE
        # =========================
        document = self.parser.parse(document)
        print("Parsed pages:", len(document.pages))

        # =========================
        # 3. EXTRACT (metadata must be BEFORE clean/chunk)
        # =========================
        for extractor in self.extractors:
            document = extractor.extract(document)

        # =========================
        # 4. CLEAN
        # =========================
        for cleaner in self.cleaners:
            document = cleaner.clean(document)
        print("123")
        # =========================
        # 5. CHUNK
        # =========================
        for chunker in self.chunkers:
            document = chunker.chunk(document)
        print("456")
        # =========================
        # 6. VALIDATE
        # =========================
        for validator in self.validators:
            document = validator.validate(document)
        print("789")
        # =========================
        # 7. METRICS
        # =========================
        for metric in self.metrics:
            document = metric.calculate(document)

        # =========================
        # 8. REPORT
        # =========================
        self.reporter.generate(document)
        print("1011")
        # =========================
        # 9. EXPORT
        # =========================
        self.exporter.export(document)

        return document