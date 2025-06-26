import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from messages import *

async def send_loading_message(update: Update, context: ContextTypes.DEFAULT_TYPE, stop_animation: asyncio.Event):
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