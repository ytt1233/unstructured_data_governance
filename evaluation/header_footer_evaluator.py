from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
import json
from pathlib import Path 
import os

# 1、页眉识别率
df = pd.read_excel('./example_docs/header.xlsx')

y_true = df['is_header_manual']   # 人工标注
y_pred = df['is_header_auto'].fillna(0)   # 根据规则自动计算的结果

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("Header Precision:", precision)
print("Header Recall:", recall)
print("Header F1:", f1)





# 2、页脚识别率
df = pd.read_excel('./example_docs/footer.xlsx')

y_true = df['is_footer_manual']   # 人工标注
y_pred = df['is_footer_auto'].fillna(0)   # 根据规则自动计算的结果

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("Footer Precision:", precision)
print("Footer Recall:", recall)
print("Footer F1:", f1)


# 3、页眉页脚重复次数
def count_repeats(path: str,joint: str):
    data = []
    total = 0
    with open(r"./example_docs/header_footer_info.txt", "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            data.append(item)
    for item in data:
        file_name = item.get("file_name")
        if file_name:
            base, ext = os.path.splitext(file_name)
            if ext.lower() == ".pdf":
                file_name = base + joint  
            file_path = os.path.join(path, file_name) 
        with open(file_path, "r", encoding="utf-8") as f: 
            content = f.read()
        counts = {}
        for s in item.get("header_footer_info"): 
            counts[s] = content.count(s)
            total += content.count(s)
    return total

total = count_repeats(r"./example_docs/raw_docs/text",".txt")
print(f'页眉页脚重复次数原为:{total}')
total = count_repeats(r"./example_docs/governed_docs/text","_cleaned.txt")
print(f'页眉页脚重复次数治理后为:{total}')
          
    

# 5 、文本冗余程度 
def count_redundancy(directory: Path):
    if not directory.exists(): 
        print(f"❌ 目录不存在: {directory}")
        return
    length = 0
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".txt":
            content = file_path.read_text(encoding='utf-8')      
            length += len(content)          # 字符数
    return length
count_raw = count_redundancy(Path(r"./example_docs/raw_docs/text"))
count_governed = count_redundancy(Path(r"./example_docs/governed_docs/text"))
score = round((count_raw - count_governed) / count_raw, 2) * 100
print(f'冗余程度下降了:{score}个百分点')