# 1️⃣ 项目简介（Project Overview）

本项目是一个面向企业知识库建设、RAG前置治理和非结构化数据管理场景的文档治理平台（Document Governance Pipeline）。

在企业构建知识库、智能问答系统和文档检索系统过程中，原始PDF、Word、TXT等非结构化文档通常存在页眉页脚重复、OCR噪声、敏感信息泄露、内容质量不稳定以及结构化程度不足等问题，直接入库会影响检索效果和知识库质量。

本项目基于Pipeline架构构建了一套可扩展的非结构化文档治理流水线，实现文档解析、元数据提取、文本质量治理、PII脱敏、Chunk生成、数据质量校验、治理审计（Audit Trail）、指标统计（Metrics）以及标准化JSONL输出等能力。

项目采用Parser、Cleaner、Chunker、Validator等插件化设计，支持治理流程灵活扩展，为企业知识库建设、RAG数据准备和非结构化数据治理提供高质量、可追溯、可审计的数据基础。


# 2️⃣ 项目亮点（Project Highlights）
✓ Pipeline流水线架构

✓ Schema驱动设计
Document / Metadata / Chunk

✓ Audit Trail全链路审计

✓ Validation质量校验体系

✓ Metrics治理指标统计

✓ 标准化JSONL知识库输出

✓ 可扩展Parser/Cleaner/Validator插件机制 


# 3️⃣ 系统架构图（Architecture）

<img src="./img/架构图.svg" width="400" height="300"> 


# 4️⃣ 核心能力（Core Capabilities）
## 1、元数据提取 

<img src="./img/元数据提取前.png" width="400" height="300"> 

<img src="./img/元数据提取后.png" width="400" height="300">  

## 2、文本质量治理 

### - 基础文本清洗

作用：消除编码差异同时去掉多余的空格及空行 

基础文本清洗前：

<img src="./img/基础文本清洗前.png" width="400" height="300"> 

基础文本清洗后：

<img src="./img/基础文本清洗后.png" width="400" height="300"> 

### - 页眉页脚清洗 

作用：自动识别并删除跨页重复内容，减少知识库冗余信息。

页眉页脚治理前：

<img src="./img/页眉页脚去除前.png" width="400" height="300"> 

页眉页脚治理后：

<img src="./img/页眉页脚去除后.png" width="400" height="300"> 

### - OCR乱码治理

作用：自动清除OCR识别产生的异常字符，提升Chunk质量和检索准确率。

OCR乱码治理前：

<img src="./img/ocr噪音去除前.png" width="400" height="300"> 

OCR乱码治理后：

<img src="./img/ocr噪音去除后.png" width="400" height="300"> 

## 3、敏感信息治理 

作用：
避免敏感信息进入知识库，降低数据泄露风险，满足企业知识库建设和RAG场景的数据合规要求。
支持手机号、邮箱、身份证的脱敏处理 

敏感信息治理前：

<img src="./img/脱敏前.png" width="400" height="300"> 

敏感信息治理后：

<img src="./img/脱敏后.png" width="400" height="300"> 


## 4、chunk 生成 

作用：将长文档切分为标准化知识单元，便于后续知识库入库与检索。

chunk生成前：

<img src="./img/chunk前.png" width="400" height="300"> 

chunk生成后：

<img src="./img/chunk后.png" width="400" height="300"> 

## 5、数据治理质量校验 
作用：自动验证治理结果，发现数据质量问题，保证输出数据可用性。

- 单个文档治理结果校验信息

<img src="./img/单个文档数据治理质量校验1.png" width="400" height="300"> 

<img src="./img/单个文档数据治理质量校验2.png" width="400" height="300"> 
 
 
 
- 数据集整体治理结果校验信息

<img src="./img/数据治理效果数据集.png" width="400" height="300">

## 6、数据治理全链路审计 
作用：记录文档治理全流程操作轨迹，实现治理过程可追溯、可审计、可复现，便于问题定位与质量分析。

<img src="./img/数据治理全链路审计1.png" width="400" height="300"> 

<img src="./img/数据治理全链路审计2.png" width="400" height="300"> 

## 7、数据治理指标统计 
作用：统计治理过程中的关键质量指标，
量化评估数据治理效果，
为治理优化和质量监控提供数据支撑。

<img src="./img/数据治理指标统计.png" width="400" height="300">

# 5️⃣ 快速开始（Quick Start）


## 1、下载代码

```bash
git clone https://github.com/ytt1233/ai-unstructured-data-governance.git

cd ai-unstructured-data-governance
```
## 2、安装依赖

```bash
pip install -r requirements.txt
```
## 3、准备文档 (Prepare Documents)

将待治理文档放入：

```text
example_docs/raw_docs/
```

例如：

```text
example_docs/raw_docs/
├── 华锦股份：2025年年度报告摘要.PDF
├── 盈康生命：2026年一季度报告.PDF
```
## 4、运行流水线 (Run Pipeline)

```bash
python main.py --input example_docs/raw_docs
```
## 5、查看治理结果 (Output)

治理结果输出到：

```text
├─ output/
│   ├─ reports/
│   │   ├─ 华锦股份：2025年年度报告摘要_report.json
│   │   ├─ 华锦股份：2025年年度报告摘要_report.md 
│   │   ├─ 盈康生命：2026年一季度报告_report.json
│   │   ├─ 盈康生命：2026年一季度报告_report.md
│   │   └─ dataset_report.md
```
**其中"华锦股份：2025年年度报告摘要_report"为单个文件治理结果** 

输出内容包括：

* Metadata
* Metrics
* Validation Results
* Audit Trail

截图如下：

<img src="./img/单文件报告1.png" width="400" height="300"> 

<img src="./img/单文件报告2.png" width="400" height="300"> 

<img src="./img/单文件报告3.png" width="400" height="300"> 

<img src="./img/单文件报告4.png" width="400" height="300">




**其中"dataset_report.md"为整个数据集治理结果** 

输出内容包括
* Dataset Summary
* Validation Summary
* Governance Effectiveness
* Dataset Insights
* Recommendations 

截图如下：

<img src="./img/数据集报告1.png" width="400" height="300"> 

<img src="./img/数据集报告2.png" width="400" height="300"> 

<img src="./img/数据集报告3.png" width="400" height="300"> 


# 6️⃣ jsonl 输出（Output Example）
  
治理完成后输出标准化知识库格式：

{
  "doc_id": doc_id, 

  "file_name": file_name, 

  "file_type": file_type, 

  "metadata": {}, 

  "metrics": {}, 

  "validation_results": {}, 

  "audit_trail": [], 

  "chunks": [] 
  
}

部分展示：

<img src="./img/json.png" width="600" height="400">

完整输出见：output/governed_docs

# 7️⃣ 技术栈
Language
- Python

Document Processing
- PyMuPDF
- Regex

Architecture
- Pipeline Architecture
- Dataclass Schema

Data Format
- JSON
- JSONL

Engineering
- Audit Trail
- Validation Framework
- Metrics Framework      

# 8️⃣ 后续规划
Roadmap

V1.0 — Core Governance Pipeline
✓ PDF Parser
✓ Metadata Extraction
✓ Header/Footer Cleaning
✓ OCR Noise Cleaning
✓ PII Masking
✓ Chunk Generation
✓ Validation Framework
✓ Metrics Collection
✓ Audit Trail
✓ JSON Export
✓ JSONL Export
✓ Document Report
✓ Dataset Report

V1.1 — Multi-Format Support
□ TOC Cleaner
□ TXT Parser
□ DOCX Parser

V1.2 — Advanced Document Understanding
□ Table Extraction
□ Layout Analysis
□ Figure Detection

V1.3 — Governance Persistence
□ Audit Trail Persistence
□ Governance History Tracking
□ Incremental Processing


