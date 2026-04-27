# test_db.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Загружаем сохранённый индекс
print("Загружаю индекс FAISS")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Задаём тестовый вопрос
question = "Что такое Agile?"  # Можно свой вопрос

print(f"\n Вопрос: {question}\n")
print("Ищу похожие кусочки...\n")

# Ищем 3 самых релевантных кусочка
results = vector_store.similarity_search(question, k=3)

for i, doc in enumerate(results, 1):
    print(f"--- Результат {i} ---")
    print(doc.page_content)
    print()