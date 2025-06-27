import asyncio

from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes

from constants import ERROR_MESSAGE, START_MESSAGE
from keyboard import START_INLINE_KEYBOARD, EXIT_KEYBOARD, MODELS_INLINE_KEYBOARD

async def reply_start_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вывод Inline-кнопки выбора начального действия"""
    await update.message.reply_text(
        START_MESSAGE, 
        reply_markup=START_INLINE_KEYBOARD,
    )

async def reply_model_choice_message(query: CallbackQuery):
    """Вывод Inline-кнопки выбора модели AI"""
    await query.edit_message_text(
        "Выбери модель AI 🦾",
        reply_markup=MODELS_INLINE_KEYBOARD
    )

async def reply_markdown_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
    """Отправка markdown-сообщения"""
    await update.message.reply_markdown(
        message_text,
        reply_markup=EXIT_KEYBOARD,
    )

async def reply_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
    """Отправка markdown-сообщения"""
    await update.message.reply_text(
        message_text,
        reply_markup=EXIT_KEYBOARD,
    )

async def reply_error_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка сообщения об ошибке"""
    await update.message.reply_text(
        ERROR_MESSAGE + "\n" + START_MESSAGE,
        reply_markup=START_INLINE_KEYBOARD,
    )

async def send_loading_message(update: Update, context: ContextTypes.DEFAULT_TYPE, stop_animation: asyncio.Event):
    """Отправка сообщения ожидания со спиннером"""
    loading_message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Подожди, думаю... "
    )

    spinner = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]

    while not stop_animation.is_set():
        for frame in spinner:
            if stop_animation.is_set():
                await loading_message.delete()
                break
            try:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=loading_message.message_id,
                    text=f"Подожди, думаю... {frame}"
                )
                await asyncio.sleep(0.15)
            except:
                await loading_message.delete()
                break

    loading_message.delete()
