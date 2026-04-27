# AI Mentor — ИИ-ассистент для студентов

RAG-бот для консультирования по управлению проектами. Работает на базе YandexGPT и FAISS

1. Клонировать репозиторий
git clone https://github.com/ТВОЙ_ЛОГИН/ai-mentor.git
cd ai-mentor

2. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate   # для Windows
source venv/bin/activate  # для Mac/Linux

3. Установить зависимости
pip install -r requirements.txt

4. Создать файл .env
В папке проекта создай файл .env и добавь:

TELEGRAM_BOT_TOKEN=токен_от_BotFather
YC_FOLDER_ID=твой_folder_id
YC_API_KEY=твой_api_ключ

api и folder id брать из yandexcloud, для этого нужно зарегистрироваться и получить api ключ:

1.Перейди на cloud.yandex.ru
2.Нажми "Начать работу" → войди через Яндекс ID
3.Создай платёжный аккаунт (нужно привязать карту, но не спишут — дают пробный грант 4000-6000₽ на первое время)
4.В консоли управления выбери облако
5.Перейди в каталог → вкладка "Сервисные аккаунты"
6.Нажми "Создать сервисный аккаунт"
7.Назови его ai-mentor
8.Добавь роль ai.languageModels.user
9.Выбери созданный сервисный аккаунт
10.Нажми "Создать новый ключ" → "Создать API-ключ"
11.В поле "Область действия" укажи yc.ai.languageModels.execute
12.Нажми "Создать"

Подробнее тут
https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key

5.Создать базу знаний
Положи текстовые файлы со статьями в папку data/ (формат .txt)

Запусти создание базы:
python create_db.py

6. Запустить бота
python bot.py


Как добавить новую статью:
- Положи файл .txt в папку data/
- Запусти python create_db.py
- Перезапусти бота

Используемые технологии

  Python 3.12+

  YandexGPT

  FAISS

  LangChain

  Telegram Bot API
