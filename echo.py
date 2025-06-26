import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from ai_functions import *
from keyboard import *
from language_detector import *
from translator import *
from user_data import *

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_thinking_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет временное сообщение и возвращает его ID"""
    message = await update.message.reply_text("⏳ Подожди, думаю...")
    return message.message_id

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int):
    """Удаляет сообщение с указанным ID"""
    try:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_id
        )
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup(START_INLINE_KEYBOARD)
    await update.message.reply_text(
        "Выбери действие 💬",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем нажатие Inline-кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data in AI_MODELS.keys():
        context.user_data["model_selected"] = True
        context.user_data["selected_model"] = query.data

        await query.edit_message_text(text=f"Выбрана модель: {query.data}." + "\n" + BUTTON_RESPONSES.get(GPT_GUID))

    user_choice = USER_CHOICE_MAP.get(query.data)

    if user_choice:
        print(f"Нажата кнопка \"{user_choice}\"")
        context.user_data["user_choice"] = user_choice

    if context.user_data["user_choice"] == TRANSLATE_TEXT:
        await query.edit_message_text(text=BUTTON_RESPONSES[query.data])

    if context.user_data["user_choice"] == GPT_TEXT and not context.user_data.get("model_selected"):
        if not context.user_data.get("model_selected"):
            reply_markup = InlineKeyboardMarkup(MODELS_INLINE_KEYBOARD)

            await query.edit_message_text(
                "Выбери модель AI:",
                reply_markup=reply_markup
            )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем обычные текстовые сообщения"""

    user_message = update.message.text
    user_data = get_user_fullname(update.message.from_user)
    user_id = getattr(update.message.from_user, "id")

    print(f"{user_data}: {user_message}")

    if user_message == EXIT_BUTTON_TEXT:
        context.user_data.clear()

        keyboard = START_INLINE_KEYBOARD
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data["user_choice"] = None
        context.user_data["model_selected"] = False
        delete_user_cache(user_id)
        await update.message.reply_text(
            "Выбери действие 💬",
            reply_markup=reply_markup
        )

    else:
        if context.user_data["user_choice"] == TRANSLATE_TEXT:
            target_language, source_language = detect_language(user_message)
            if target_language and source_language:
                ai_response = translate_text(user_message, target_language, source_language)
            else:
                await update.message.reply_text(ERROR_TEXT, reply_markup=EXIT_KEYBOARD)

        elif context.user_data["user_choice"] == GPT_TEXT:
            init_db()

            user_messages = load_user_cache(user_id)

            thinking_messsage_id = await send_thinking_message(update, context)

            if not user_messages:
                user_messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                ]
            user_messages.append(
                {
                    "role": "user",
                    "content": user_message,
                },
            )

            ai_model = get_ai_model(context.user_data.get("selected_model"))
            ai_response = get_ai_response(user_messages, ai_model)

            user_messages.append(
                {
                    "role": "assistant",
                    "content": ai_response,
                },            
            )

            save_user_cache(user_id, user_messages)

            ai_response = get_formatted_ai_response(ai_response)
            
            await delete_message(update, context, thinking_messsage_id)

        print(f"bot: {ai_response}")
        try:
            await update.message.reply_markdown(ai_response, reply_markup=EXIT_KEYBOARD)
        except:
            await update.message.reply_text(ai_response, reply_markup=EXIT_KEYBOARD)
            

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен")
    application.run_polling()

if __name__ == "__main__":
    main()