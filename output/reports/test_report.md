# Document Governance Report

## 1. Document Info
- doc_id: test
- file_name: test.txt
- file_type: .txt
- pages: 1
- raw_chars: 441
- clean_chars: 435

## 2. Metadata
- title: 这是第一段。
- category: 未知

## 3. Metrics

### toc
- removed_toc_lines: 0

### chunk
- chunk_count: 1
- avg_chunk_size: 435.0
- min_chunk_size: 435
- max_chunk_size: 435

### text_quality
- chars_before: 441
- chars_after: 436
- removed_chars: 5
- char_reduction_rate: 1.13%
- blank_lines_before: 5
- blank_lines_after: 0
- blank_lines_removed: 5

### header_footer
- removed_headers: 0
- removed_footers: 0
- total_pages: 1

### pii
- phone_count: 1
- email_count: 1
- id_card_count: 0
- total_pii: 2

### ocr_noise
- text_length_before: 436
- text_length_after: 436
- removed_noise_chars: 0
- noise_ratio: 0.0%

## 4. Validation Summary
- pass: 6
- fail: 0
- total: 6
- pass_rate: 1.0
- overall_status: PASS

## 5. Audit Trail (Top 10)
- txt_parse | {'action': 'txt_parse'}
- metadata_extract | {'action': 'metadata_extract'}
- text_clean | {'action': 'text_clean', 'operations': ['unicode_normalization', 'remove_invisible_chars', 'normalize_spaces', 'normalize_blank_lines']}
- header_footer_clean | {'action': 'header_footer_clean', 'removed_headers': 0, 'removed_footers': 0, 'total_pages': 1}
- toc_clean | {'action': 'toc_clean', 'removed_toc_lines': 0}
- ocr_noise_clean | {'action': 'ocr_noise_clean', 'removed_noise_chars': 0}
- pii_clean | {'action': 'pii_clean', 'phone_count': 1, 'email_count': 1, 'id_card_count': 0}
- fixed_chunk | {'action': 'fixed_chunk', 'strategy': 'fixed', 'configured_chunk_size': 500, 'overlap': 50, 'chunk_count': 1}