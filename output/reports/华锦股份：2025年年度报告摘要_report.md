# Document Governance Report

## 1. Document Info
- doc_id: 华锦股份：2025年年度报告摘要
- file_name: 华锦股份：2025年年度报告摘要.PDF
- file_type: .PDF
- pages: 3
- raw_chars: 2912
- clean_chars: 2815

## 2. Metadata
- title: 北方华锦化学工业股份有限公司2025年年度报告摘要
- category: 规划

## 3. Metrics

### chunk
- chunk_count: 7
- avg_chunk_size: 430.43
- min_chunk_size: 215
- max_chunk_size: 500

### text_quality
- chars_before: 2912
- chars_after: 2908
- removed_chars: 4
- char_reduction_rate: 0.14%
- blank_lines_before: 3
- blank_lines_after: 0
- blank_lines_removed: 3

### header_footer
- removed_headers: 3
- removed_footers: 0
- total_pages: 3

### pii
- phone_count: 0
- email_count: 1
- id_card_count: 0
- total_pii: 1

### ocr_noise
- text_length_before: 2827
- text_length_after: 2820
- removed_noise_chars: 7
- noise_ratio: 0.25%

## 4. Validation Summary
- pass: 6
- fail: 0
- total: 6
- pass_rate: 1.0
- overall_status: PASS

## 5. Audit Trail (Top 10)
- pdf_parse | {'action': 'pdf_parse'}
- metadata_extract | {'action': 'metadata_extract'}
- text_clean | {'action': 'text_clean', 'operations': ['unicode_normalization', 'remove_invisible_chars', 'normalize_spaces', 'normalize_blank_lines']}
- header_footer_clean | {'action': 'header_footer_clean', 'removed_headers': 3, 'removed_footers': 0, 'total_pages': 3}
- ocr_noise_clean | {'action': 'ocr_noise_clean', 'removed_noise_chars': 7}
- pii_clean | {'action': 'pii_clean', 'phone_count': 0, 'email_count': 1, 'id_card_count': 0}
- fixed_chunk | {'action': 'fixed_chunk', 'strategy': 'fixed', 'configured_chunk_size': 500, 'overlap': 50, 'chunk_count': 7}