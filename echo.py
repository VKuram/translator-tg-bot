import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup, User
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from ai_functions import *
from keyboard import *
from language_detector import *
from translator import *

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_CHOICE = None

def get_user_fullname(user: User) -> str:
    user_data = [
        getattr(user, "id"),
        getattr(user, "first_name"),
        getattr(user, "last_name"),
        getattr(user, "username"),
    ]

    return ", ".join([str(ud) for ud in user_data if (ud is not None and ud != "")])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = INLINE_KEYBOARD
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выбери действие 💬",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем нажатие Inline-кнопки"""
    global USER_CHOICE
    query = update.callback_query
    await query.answer()  # Обязательно вызываем answer()
    
    response = BUTTON_RESPONSES[query.data]
    
    await query.edit_message_text(text=response)
    
    print(f"Нажата кнопка \"{USER_CHOICE_MAP[query.data]}\"")
    USER_CHOICE = USER_CHOICE_MAP[query.data]

    if USER_CHOICE == TRANSLATE_TEXT:
        await update.message.reply_text(
            BUTTON_RESPONSES[TRANSLATE_GUID],
            reply_markup=EXIT_KEYBOARD
        )
    elif USER_CHOICE == GPT_TEXT:
        await update.message.reply_text(
            BUTTON_RESPONSES[GPT_GUID],
            reply_markup=EXIT_KEYBOARD
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем обычные текстовые сообщения"""
    global USER_CHOICE
    user_message = update.message.text
    print(update.message.from_user)
    user = get_user_fullname(update.message.from_user)

    print(f"{user}: {user_message}")

    if user_message == EXIT_BUTTON_TEXT:
        context.user_data.clear()

        keyboard = INLINE_KEYBOARD
        reply_markup = InlineKeyboardMarkup(keyboard)
        USER_CHOICE == None
        await update.message.reply_text(
            "Выбери действие 💬",
            reply_markup=reply_markup
        )

    else:
        if USER_CHOICE == TRANSLATE_TEXT:
            target_language, source_language = detect_language(user_message)
            if target_language and source_language:
                response = translate_text(user_message, target_language, source_language)
            else:
                await update.message.reply_text(ERROR_TEXT, reply_markup=EXIT_KEYBOARD)

        elif USER_CHOICE == GPT_TEXT:
            messages_to_ai = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ]

            response = get_ai_response(messages_to_ai)

        print(f"bot: {response}")
        await update.message.reply_markdown(response, reply_markup=EXIT_KEYBOARD)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен")
    application.run_polling()

if __name__ == '__main__':
    main()