from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from ai_functions import AI_MODELS_MAP

from constants import EXIT_BUTTON_TEXT, GPT_GUID, GPT_TEXT, TRANSLATE_GUID, TRANSLATE_TEXT

EXIT_KEYBOARD = ReplyKeyboardMarkup([[EXIT_BUTTON_TEXT]], resize_keyboard=False, one_time_keyboard=True)  # Кнопка завершения

START_INLINE_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(TRANSLATE_TEXT, callback_data=TRANSLATE_GUID),
        InlineKeyboardButton(GPT_TEXT, callback_data=GPT_GUID)
    ]
])  # Inline-кнопки выбора действия

MODELS_INLINE_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(model_name, callback_data=model_name) for model_name in AI_MODELS_MAP.keys()
    ]
])  # Inline-кнопки выбора модели AI
