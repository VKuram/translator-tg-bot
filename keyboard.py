from telegram import InlineKeyboardButton, ReplyKeyboardMarkup

from ai_functions import AI_MODELS

from constants import EXIT_BUTTON_TEXT, TRANSLATE_TEXT, GPT_TEXT, TRANSLATE_GUID, GPT_GUID

EXIT_KEYBOARD = ReplyKeyboardMarkup([[EXIT_BUTTON_TEXT]], resize_keyboard=True)
START_INLINE_KEYBOARD = [
    [
        InlineKeyboardButton(TRANSLATE_TEXT, callback_data=TRANSLATE_GUID),
        InlineKeyboardButton(GPT_TEXT, callback_data=GPT_GUID)
    ]
]
MODELS_INLINE_KEYBOARD = [
    [
        InlineKeyboardButton(model_name, callback_data=model_name) for model_name in AI_MODELS.keys()
    ]
]

