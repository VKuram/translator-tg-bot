from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from ai_functions import (
    get_ai_message_log,
    get_ai_model,
    get_ai_response, 
    get_formatted_ai_response,
    get_prompt_message_log, 
    get_user_message_log,
)
from constants import (
    AI_MODELS_MAP,
    BUTTON_RESPONSES,
    ERROR_MESSAGE,
    EXIT_BUTTON_TEXT,
    GPT_GUID,
    GPT_TEXT,
    TELEGRAM_BOT_TOKEN,
    TRANSLATE_TEXT,
    START_CHOICE_MAP,
)
from messages import(
    reply_error_message,
    reply_markdown_message,
    reply_model_choice_message,
    reply_start_message,
    reply_text_message,
)
from translator import translate_text
from user_data import delete_user_cache, get_user_full_name, init_db, load_user_cache, save_user_cache

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка /start, отправка стартовых Inline-кнопок выбора начального действия"""
    await reply_start_message(update, context)

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка /whoami, отправка данных пользователя"""
    print(get_user_full_name(update.message.from_user))
    await update.message.reply_markdown(
        get_user_full_name(update.message.from_user),
    )
    await reply_start_message(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия Inline-кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data in START_CHOICE_MAP.keys():  # Если выбрано начальное действие
        start_choice = START_CHOICE_MAP.get(query.data)

        print(f"Нажата кнопка \"{start_choice}\"")  # Лог нажатой кнопки
        context.user_data["user_choice"] = START_CHOICE_MAP.get(query.data)

        if start_choice == TRANSLATE_TEXT:  # Если выбран переводчик
            await query.edit_message_text(
                text=BUTTON_RESPONSES.get(query.data)
            )

        if start_choice == GPT_TEXT and not context.user_data.get("model_selected"):  # Если выбран чат-бот
            await reply_model_choice_message(query)

    if query.data in AI_MODELS_MAP.keys():  # Если выбрана модель AI
        context.user_data["model_selected"] = True
        context.user_data["selected_model"] = query.data

        await query.edit_message_text(
            text=f"Выбрана модель: {query.data}" + "\n" + BUTTON_RESPONSES.get(GPT_GUID)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    user_message = update.message.text
    user_full_name = get_user_full_name(update.message.from_user)
    user_id = getattr(update.message.from_user, "id")

    print(f"{user_full_name}: {user_message}")  # Лог данных пользователя и сообщения

    if user_message == EXIT_BUTTON_TEXT:  # Если нажата кнопка выхода
        context.user_data.clear()
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
        except Exception as e:
            print(f"Ошибка при удалении: {e}")  # Лог ошибки удаления сообщения пользователя

        context.user_data["user_choice"] = None  # Очистка выбора
        context.user_data["model_selected"] = False  # Очистка модели

        delete_user_cache(user_id)  # Очистка кэша

        await reply_start_message(update, context)

    else:
        if context.user_data.get("user_choice") == TRANSLATE_TEXT:  # Если выбран переводчик
            try:
                translation_response = translate_text(user_message)

                await reply_markdown_message(update, context, translation_response)
            except:
                await reply_text_message(update, context, translation_response)
                await reply_start_message(update, context)

        elif context.user_data.get("user_choice") == GPT_TEXT:  # Если выбран чат-бот
            init_db()

            messages_log = load_user_cache(user_id)

            if not messages_log:
                messages_log = [get_prompt_message_log()]

            messages_log.append(get_user_message_log(user_message))

            ai_model = get_ai_model(context.user_data.get("selected_model"))
            ai_response = await get_ai_response(update, context, messages_log, ai_model)

            if ai_response == ERROR_MESSAGE:
                await reply_error_message(update, context)
            else:
                messages_log.append(get_ai_message_log(ai_response))

                save_user_cache(user_id, messages_log)

                ai_response = get_formatted_ai_response(ai_response)

                try:
                    await reply_markdown_message(update, context, ai_response)
                except:
                    await reply_text_message(update, context, ai_response)

        else:
            await reply_error_message(update, context)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("whoami", whoami))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен")
    application.run_polling()

if __name__ == "__main__":
    main()