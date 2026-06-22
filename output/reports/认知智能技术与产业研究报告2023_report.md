# Document Governance Report

## 1. Document Info
- doc_id: 认知智能技术与产业研究报告2023
- file_name: 认知智能技术与产业研究报告2023.pdf
- file_type: .pdf
- pages: 29
- raw_chars: 16743
- clean_chars: 14982

## 2. Metadata
- title: 认知智能技术与应用研究报告（2023 年）
- category: 规划

## 3. Metrics

### toc
- removed_toc_lines: 22

### chunk
- chunk_count: 52
- avg_chunk_size: 308.92
- min_chunk_size: 1
- max_chunk_size: 500

### text_quality
- chars_before: 16743
- chars_after: 16713
- removed_chars: 30
- char_reduction_rate: 0.18%
- blank_lines_before: 29
- blank_lines_after: 0
- blank_lines_removed: 29

### header_footer
- removed_headers: 31
- removed_footers: 0
- total_pages: 29

### pii
- phone_count: 0
- email_count: 0
- id_card_count: 0
- total_pii: 0

### ocr_noise
- text_length_before: 16067
- text_length_after: 14982
- removed_noise_chars: 4
- noise_ratio: 0.02%

## 4. Validation Summary
- pass: 7
- fail: 0
- total: 7
- pass_rate: 1.0
- overall_status: PASS

## 5. Audit Trail (Top 10)
- pdf_parse | {'action': 'pdf_parse'}
- metadata_extract | {'action': 'metadata_extract'}
- text_clean | {'action': 'text_clean', 'operations': ['unicode_normalization', 'remove_invisible_chars', 'normalize_spaces', 'normalize_blank_lines']}
- header_footer_clean | {'action': 'header_footer_clean', 'removed_headers': 31, 'removed_footers': 0, 'total_pages': 29}
- toc_clean | {'action': 'toc_clean', 'removed_toc_lines': 22}
- ocr_noise_clean | {'action': 'ocr_noise_clean', 'removed_noise_chars': 4}
- pii_clean | {'action': 'pii_clean', 'phone_count': 0, 'email_count': 0, 'id_card_count': 0}
- fixed_chunk | {'action': 'fixed_chunk', 'strategy': 'fixed', 'configured_chunk_size': 500, 'overlap': 50, 'chunk_count': 52}