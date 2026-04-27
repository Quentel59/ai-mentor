import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import YandexGPT

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FOLDER_ID = os.getenv("YC_FOLDER_ID")
API_KEY = os.getenv("YC_API_KEY")

logging.basicConfig(level=logging.INFO)

print("Загрузка...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

llm = YandexGPT(
    folder_id=FOLDER_ID,
    api_key=API_KEY,
    temperature=0.7
)


def get_answer(question: str) -> str:
    # Поиск в базе
    docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])

    # Запрос к YandexGPT
    prompt = f"""Ты ментор по проектам. Отвечай только на основе контекста.
Если ответа нет в контексте, скажи об этом.

Контекст:
{context}

Вопрос: {question}"""

    try:
        return llm.invoke(prompt)
    except Exception as e:
        return f"Ошибка: {e}\n\nНайденные фрагменты:\n{context}"


async def handle(update: Update, context):
    answer = get_answer(update.message.text)
    await update.message.reply_text(answer)


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
print("Бот запущен")
app.run_polling()