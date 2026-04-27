# create_db.py
import glob
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ЗАГРУЖАЕМ ВСЕ .txt ФАЙЛЫ ИЗ ПАПКИ data
print("Читаю все файлы из папки data/")

all_text = ""

# Находим все .txt файлы в папке data
txt_files = glob.glob("data/*.txt")

if not txt_files:
    print("Ошибка: Не найдено ни одного .txt файла в папке data/")
    exit(1)

for file_path in txt_files:
    print(f"   Читаю: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        # Добавляем название файла как разделитель
        all_text += f"\n\n=== Файл: {file_path} ===\n\n{file_content}\n"

print(f" Загружено файлов: {len(txt_files)}")
print(f"   Общий размер текста: {len(all_text)} символов")

# РАЗБИВАЕМ НА КУСОЧКИ
print("\n Разбиваю текст на кусочки")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_text(all_text)
print(f"   Получилось {len(chunks)} кусочков")

# СОЗДАЁМ ВЕКТОРНЫЕ ПРЕДСТАВЛЕНИЯ
print("\n Создаю векторные представления (это может некоторое время)")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# СОХРАНЯЕМ FAISS ИНДЕКС
print("\n Создаю FAISS индекс и сохраняю")
vector_store = FAISS.from_texts(chunks, embeddings)
vector_store.save_local("faiss_index")

print("\n Готово! База знаний сохранена в папку 'faiss_index'")
print(f"   В базе {len(chunks)} кусочков из {len(txt_files)} файлов")