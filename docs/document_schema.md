
## 概述(Overview)

`Document` 是非结构化数据治理系统中的核心数据对象。所有管道组件都操作同一`Document`实例，并逐步向该对象中添加内容，如解析内容、治理结果、验证结果、度量、审计信息。

`Document` is the core data object of the Unstructured Data Governance Framework.
All pipeline components operate on the same `Document` instance and progressively enrich it with parsed content, governance results, validation results, metrics, and audit information.


# Document Structure

```text
Document
│
├── Basic Information
├── Parsed Content
├── Metadata
├── Chunk Data
├── Metrics
├── Validation Results
├── Audit Trail
└── Sample Records
```

---

# 1. Basic Information

## doc_id

### Description

Unique identifier of the document.

### Producer

* PDFLoader

### Example

```python
"8f7c9f9e-6b7a-4d3e-a9a2-12d3f8b6d123"
```

---

## file_name

### Description

Original file name.

### Producer

* PDFLoader

### Example

```python
"Annual_Report_2025.pdf"
```

---

## file_path

### Description

Absolute path of the source file.

### Producer

* PDFLoader

---

## file_type

### Description

Document type.

### Producer

* PDFLoader

### Example

```python
"pdf"
```

---

# 2. Parsed Content

## raw_text

### Description

Original text extracted from the source document before any governance processing.

### Producer

* PDFParser

### Example

```python
"Company Annual Report..."
```

---

## cleaned_text

### Description

Text after governance processing.

This field is continuously updated by cleaners.

### Producer

* TextCleaner
* HeaderFooterCleaner
* OCRNoiseCleaner
* PiiCleaner

### Consumer

* FixedChunker
* Validators
* Metrics

---

## pages

### Description

Page-level document representation.

### Producer

* PDFParser

### Structure

```python
[
    Page(
        page_num=1,
        text="..."
    )
]
```

---

# 3. Metadata

## metadata.common

### Description

Common metadata extracted from documents.

### Producer

* MetadataExtractor

### Example

```python
{
    "title": "...",
    "source": "...",
    "category": "..."
}
```

---

## metadata.domain

### Description

Domain-specific metadata.

### Producer

* MetadataExtractor

### Example

```python
{
    "company_name": "...",
    "report_year": 2025
}
```

---

# 4. Chunk Data

## chunks

### Description

Chunked content used for retrieval and knowledge base ingestion.

### Producer

* FixedChunker

### Example

```python
[
    Chunk(
        chunk_id="...",
        text="...",
        page_num=1
    )
]
```

---

# 5. Metrics

## metrics

### Description

Governance statistics generated after processing.

### Producer

* TextQualityMetric
* HeaderFooterMetric
* PiiMetric
* OCRNoiseMetric
* ChunkMetric (built into FixedChunker)

---

## metrics["text_quality"]

### Description

Text cleaning statistics.

### Example

```python
{
    "chars_before": 2912,
    "chars_after": 2908,
    "removed_chars": 4,
    "char_reduction_rate": "0.14%",
    "blank_lines_before": 3,
    "blank_lines_after": 0,
    "blank_lines_removed": 3
}
```

---

## metrics["header_footer"]

### Description

Header/footer governance statistics.

### Example

```python
{
    "removed_headers": 3,
    "removed_footers": 0,
    "total_pages": 3
}
```

---

## metrics["pii"]

### Description

PII governance statistics.

### Example

```python
{
    "phone_count": 0,
    "email_count": 1,
    "id_card_count": 0,
    "total_pii": 1
}
```

---

## metrics["ocr_noise"]

### Description

OCR noise cleaning statistics.

### Example

```python
{
    "text_length_before": 2827,
    "text_length_after": 2820,
    "removed_noise_chars": 7,
    "noise_ratio": "0.25%"
}
```

---

## metrics["chunk"]

### Description

Chunk generation statistics.

### Example

```python
{
    "chunk_count": 7,
    "avg_chunk_size": 430.43,
    "min_chunk_size": 215,
    "max_chunk_size": 500
}
```

---

# 6. Validation Results

## validation_results

### Description

Quality validation results produced by validators.

### Producer

* MetadataValidator
* ContentLengthValidator
* OCRNoiseValidator
* HeaderFooterValidator
* ChunkValidator
* PiiValidator

---

## Example

```python
{
    "metadata": {
        "rule": "metadata_completeness"
        "status": "FAIL",
        "missing_fields": ["category"],
        "warnings": ["Title is unusually short"]
    },

    "content_length": {
        "rule": "minimum_context_length"
        "status": "PASS",
        "length": 500,
        "min_length": 500,
        "warnings": []
    },

    "ocr_noise": {
        "rule": "ocr_noise_detection"
        "status": "PASS"
        "noise_chars": 0,
        "total_chars": 500,
        "warnings": [],
        "message": 
    },
    "header_footer": {
        "rule": "header_footer_detection"
        "status": "PASS",
        "suspicious_count": 0,
        "suspicious_lines": 0,
        "warnings": []
    },
    "chunk": {
        "rule": "chunk_integrity",
        "status": "PASS",
        "chunk_count": 7,
        "empty_chunk_count": 0,
        "warnings": []
    },
    "pii": {
        "rule": "pii_validation",
        "status": "PASS",
        "remaining_phone_count": 0,
        "remaining_email_count": 0,
        "remaining_id_card_count": 0,
        "warnings": []
    }
}
```

---

# 7. Audit Trail

## audit_trail

### Description

Governance operation history.

Records what actions were performed during processing.

### Producer

* PDFparser
* MetadataExtractor
* TextCleaner
* HeaderFooterCleaner
* OCRNoiseCleaner
* PiiCleaner
* FixedChunker

### Example

```python
[
    {
        "action": "pdf_parse",
    }
    {
        "action": "metadata_extract",
    }
    {
        "action": "text_clean",
    }
    {
        "action": "header_footer_clean",
        "removed_headers": 3
        "removed_footers": 0
        "total_pages": 3
    },

    {
        "action": "ocr_noise_clean",
        "removed_noise_chars": 7
    }
    {
        "action": "pii_clean",
        "phone_count": 1,
        "email_count": 1,
        "id_card_count": 0,
    }
    {
        "action": "fixed_chunk",
        "strategy": "fixed",
        "configured_chunksize": 500,
        "overlap": 50,
        "chunk_count": 7,
"
    }
]
```

---

# 8. Sample Records

## sample_records

### Description

Representative governance examples.

Used for report display and governance verification.

### Producer

* PiiCleaner

### Example

```python
[
    {
        "type": "pii",
        "before": "Email: test@abc.com",
        "after": "Email: [EMAIL]"
    }
]
```

---

# Document Lifecycle

```text
PDF
 │
 ▼
Loader
 │
 ▼
Parser
 │
 ▼
Metadata Extractor
 │
 ▼
Cleaners
 │
 ▼
Chunker
 │
 ▼
Validators
 │
 ▼
Metrics
 │
 ▼
Report
 │
 ▼
Exporter
```

The Document object is passed through every stage of the pipeline and continuously enriched until final governance outputs are generated.
