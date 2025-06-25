from telegram import InlineKeyboardButton, ReplyKeyboardMarkup

from guid_generator import get_guid_from_value

EXIT_BUTTON_TEXT = "❌ Завершить ❌"
TRANSLATE_TEXT = "Переводчик"
GPT_TEXT = "Чат-бот"
TRANSLATE_GUID = get_guid_from_value(TRANSLATE_TEXT)
GPT_GUID = get_guid_from_value(GPT_TEXT)

USER_CHOICE_MAP = {
    TRANSLATE_GUID: TRANSLATE_TEXT,
    GPT_GUID: GPT_TEXT,
}

EXIT_KEYBOARD = ReplyKeyboardMarkup([[EXIT_BUTTON_TEXT]], resize_keyboard=True)
INLINE_KEYBOARD = [
        [
            InlineKeyboardButton(TRANSLATE_TEXT, callback_data=TRANSLATE_GUID),
            InlineKeyboardButton(GPT_TEXT, callback_data=GPT_GUID)
        ]
    ]

BUTTON_RESPONSES = {
    TRANSLATE_GUID: "Введи текст, который необходимо перевести",
    GPT_GUID: "Начни задавать вопросы, я попробую на них ответить"
}

ERROR_TEXT = "Что-то неразборчивое, попробуй снова"