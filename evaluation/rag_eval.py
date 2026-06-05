from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SimpleNodeParser
import fitz
import os
import json
import ollama

os.environ['HF_HUB_OFFLINE'] = '1'


# 1️⃣ embedding（给RAG用）
local_model_path = r"D:/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8"
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh")
embed_model = HuggingFaceEmbedding(model_name=local_model_path)
print("--------ok-----")

# 2️⃣ embedding（给评估用）
# model = SentenceTransformer("BAAI/bge-small-zh")
model = SentenceTransformer(local_model_path)

def similarity_score(answer, ground_truth):
    emb1 = model.encode([answer])
    emb2 = model.encode([ground_truth])
    return cosine_similarity(emb1, emb2)[0][0]


# 3️⃣ 数据集
def load_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # 校验字段（防止后面踩坑）
    for item in dataset:
        assert "question" in item
        assert "ground_truth" in item
        assert "keywords" in item

    return dataset

dataset = load_dataset("./example_docs/dataset.json")

# 4️⃣ 构建index

def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return Document(text=text)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return Document(text=text)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

#文档解析为document
docs = []
folder = "./example_docs/raw_docs/test" 
# folder = "./example_docs/governed_docs" 

for file in os.listdir(folder):
    if file.endswith((".pdf", ".txt")):
        docs.append(load_document(os.path.join(folder, file)))
#NodeParser解析为小块
parser = SimpleNodeParser.from_defaults(chunk_size=500)  # 每个 Node 约 500 字
nodes = parser.get_nodes_from_documents(docs)

#用node建立向量索引
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model   # ⭐ 核心
)
retriever = index.as_retriever(similarity_top_k=2)

# 5️⃣ 评估
#关键词命中率函数
def keyword_hit_score(answer, keywords):
    print(f'answer: {answer}')
    print(f'keywords: {keywords}')
    hit = 0
    for kw in keywords:
        if kw in answer:
            hit += 1
    return hit / len(keywords)
#调用模型生成答案
def generate_with_qwen(prompt, model_name):
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Ollama 调用失败: {e}")
        return ""
#评估
def evaluate(retriever, dataset):
    total_sim = 0
    total_kw = 0

    for item in dataset:
        q = item["question"]
        gt = item["ground_truth"]
        keywords = item["keywords"]

        retrieved_nodes = retriever.retrieve(q)
        print(f'retrieved_nodes: {retrieved_nodes}')
        for i, node in enumerate(retrieved_nodes):
            print(f"\n--- Node {i} --- begin")      
            print(node.text[:200])
            print(f"\n--- Node {i} --- end")
        contexts = [node.text for node in retrieved_nodes]
        answer = " ".join(contexts[:2])
        print(f"Answer: {answer}")
        prompt = f"""基于以下文档内容回答问题。只给出答案，不要多余解释。
        文档内容：
        {contexts}
        问题：{q}
        答案："""
        # 调用本地 Qwen 模型
        generated = generate_with_qwen(prompt, model_name="qwen2.5:7b")
        print(f"Generated: {generated}")
        #两种评估
        sim_score = similarity_score(generated, gt)
        kw_score = keyword_hit_score(answer, keywords)

        print(f"\nQ: {q}")
        print(f"A: {answer}")
        print(f"Similarity: {sim_score:.2f}")
        print(f"Keyword Hit: {kw_score:.2f}")

        total_sim += sim_score
        total_kw += kw_score

    return total_sim / len(dataset), total_kw / len(dataset)

# 6️⃣ 输出
avg_sim, avg_kw = evaluate(retriever, dataset)

print(f"\nAverage Similarity: {avg_sim:.2f}")
print(f"Average Keyword Hit: {avg_kw:.2f}")