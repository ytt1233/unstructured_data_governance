# Document Governance Report

## 1. Document Info
- doc_id: 盈康生命：2026年一季度报告
- file_name: 盈康生命：2026年一季度报告.PDF
- file_type: .PDF
- pages: 11
- raw_chars: 11595
- clean_chars: 10541

## 2. Metadata
- title: 盈康生命科技股份有限公司
2026年第一季度报告
- category: 法律

## 3. Metrics

### toc
- removed_toc_lines: 0

### chunk
- chunk_count: 30
- avg_chunk_size: 381.8
- min_chunk_size: 23
- max_chunk_size: 500

### text_quality
- chars_before: 11595
- chars_after: 10874
- removed_chars: 721
- char_reduction_rate: 6.22%
- blank_lines_before: 258
- blank_lines_after: 0
- blank_lines_removed: 258

### header_footer
- removed_headers: 17
- removed_footers: 0
- total_pages: 11

### pii
- phone_count: 0
- email_count: 0
- id_card_count: 0
- total_pii: 0

### ocr_noise
- text_length_before: 10554
- text_length_after: 10541
- removed_noise_chars: 13
- noise_ratio: 0.12%

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
- header_footer_clean | {'action': 'header_footer_clean', 'removed_headers': 17, 'removed_footers': 0, 'total_pages': 11}
- toc_clean | {'action': 'toc_clean', 'removed_toc_lines': 0}
- ocr_noise_clean | {'action': 'ocr_noise_clean', 'removed_noise_chars': 13}
- pii_clean | {'action': 'pii_clean', 'phone_count': 0, 'email_count': 0, 'id_card_count': 0}
- fixed_chunk | {'action': 'fixed_chunk', 'strategy': 'fixed', 'configured_chunk_size': 500, 'overlap': 50, 'chunk_count': 30}