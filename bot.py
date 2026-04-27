import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

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

# Кнопки главного меню
main_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("Задать вопрос"), KeyboardButton("О боте")],
    [KeyboardButton("Источники знаний"), KeyboardButton("Помощь")]
], resize_keyboard=True)


def get_answer(question: str) -> str:
    """Получение ответа от YandexGPT на основе базы знаний"""
    docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""Ты ментор по управлению проектами. Отвечай только на основе контекста.
Если ответа нет в контексте, скажи: "В загруженной базе знаний нет информации по этому вопросу."

Контекст:
{context}

Вопрос студента: {question}

Дай понятный, структурированный ответ на русском языке."""

    try:
        return llm.invoke(prompt)
    except Exception as e:
        return f"⚠️ Ошибка: {e}\n\nНайденные фрагменты:\n{context}"


async def start(update: Update, context):
    """Приветственное сообщение с кнопками"""
    welcome_text = """
*Привет! Я ИИ-ментор по управлению проектами*

Я помогаю студентам с вопросами по:
• Agile и Scrum
• DevOps и SAFe
• Техническому заданию (ТЗ)
• Управлению ИТ-проектами

 *Как я работаю:*
Я ищу ответы только в проверенных материалах и формулирую ответ с помощью YandexGPT.

*Просто нажми кнопку "Задать вопрос" и напиши, что тебя интересует!*

*Примеры вопросов:*
• Что такое спринт в Scrum?
• Как правильно составить ТЗ?
• Какие роли есть в Agile?
• Чем DevOps отличается от Agile?
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard)


async def about_bot(update: Update, context):
    """Информация о боте"""
    text = """
*О боте*

*Название:* AI Mentor
*Версия:* 1.0
*Технологии:* RAG, YandexGPT, FAISS, LangChain

*Что умеет:*
• Отвечать на вопросы по управлению проектами
• Искать информацию только в проверенных источниках
• Формулировать понятные ответы
"""
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard)


async def sources(update: Update, context):
    """Источники знаний"""
    text = """
*Источники знаний*

База знаний содержит материалы по:
• Agile-методологиям
• Scrum-фреймворку
• DevOps-практикам
• SAFe-фреймворку
• Техническому заданию (ТЗ)
• Управлению ИТ-проектами

*Обновление:* База пополняется по мере добавления новых статей в папку `data/`
"""
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard)


async def help_command(update: Update, context):
    """Справка по использованию"""
    text = """
*Помощь*

*Как задать вопрос:*
1. Нажми кнопку "Задать вопрос"
2. Напиши свой вопрос текстом
3. Дождись ответа (обычно 5-10 секунд)

*Команды:*
/start — Главное меню
/help — Эта справка

*Советы:*
• Задавай конкретные вопросы
• Если ответ неполный — переформулируй вопрос
• Бот отвечает только на основе загруженных материалов

*Примеры хороших вопросов:*
"Объясни, что такое спринт в Scrum"
"Какие артефакты есть в Agile?"
"Из каких этапов состоит DevOps?"
"""
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard)


async def ask_question(update: Update, context):
    """Обработка нажатия кнопки 'Задать вопрос'"""
    text = "*Напиши свой вопрос текстом.*\n\nЯ найду ответ в базе знаний и отвечу тебе."
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard)


async def handle_message(update: Update, context):
    """Обработка текстовых сообщений (не команд)"""
    user_text = update.message.text
    user_name = update.effective_user.first_name

    # Если пользователь нажал кнопку с вопросом
    if user_text == "Задать вопрос":
        await ask_question(update, context)
        return

    # Если пользователь нажал кнопку "О боте"
    if user_text == "ℹО боте":
        await about_bot(update, context)
        return

    # Если пользователь нажал кнопку "Источники знаний"
    if user_text == "Источники знаний":
        await sources(update, context)
        return

    # Если пользователь нажал кнопку "Помощь"
    if user_text == "Помощь":
        await help_command(update, context)
        return

    # Обычный текстовый вопрос
    print(f"Вопрос от {user_name}: {user_text}")

    # Отправляем статус "печатает"
    await update.message.chat.send_action(action="typing")

    # Получаем ответ
    answer = get_answer(user_text)

    # Отправляем ответ (Telegram лимит 4096 символов)
    if len(answer) > 4000:
        answer = answer[:4000] + "\n\n... (ответ обрезан)"

    await update.message.reply_text(answer, parse_mode="Markdown")


def main():
    """Запуск бота"""
    print("   Бот запущен и готов к работе!")
    print("   Найди своего бота в Telegram и напиши /start")
    print("   Нажми Ctrl+C для остановки\n")

    app = Application.builder().token(TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()