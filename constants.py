import os

from dotenv import load_dotenv

from guid_generator import get_guid_from_value

load_dotenv()

API_URL = "https://api.together.xyz/v1"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
AI_MODELS = {
    "DeepSeek": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "Meta Vision": "meta-llama/Llama-Vision-Free",
    "Meta 3.3": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "Arcee AFM": "arcee-ai/AFM-4.5B-Preview",
}

SYSTEM_PROMPT = (
"Тебе будут поступать разные вопросы, или просто пользователь захочет что-то написать. Есть несколько правил: \n"
"1. Отвечай на русском языке. \n"
"2. Выдавай информацию сжато и четко. \n"
"3. Не здоровайся, если с тобой не поздоровались, не спрашивай, можешь ли чем-то еще помочь, только отвечай на "
"поставленный вопрос. \n"
"4. Поддерживай диалог так, чтобы твое сообщение могло быть последним в диалоге, без лишних вопросов. \n"
"5. Если для решения нужно еще что-то знать, то просто перечисли, чего не хватило для решения. \n"
"6. Не додумывай за пользователя, что он от тебя хочет. Если неясно сразу, то так и напиши, перечисли, чего не хватило"
". \n"
"7. Если нужно форматирование текста, то используй метод парсинга Markdown (например, блок кода передавай внутри ```)"
)

END_WORDS = ["</think>"]

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

EXIT_BUTTON_TEXT = "-    Выход 🔌    -"
TRANSLATE_TEXT = "Переводчик"
GPT_TEXT = "Чат-бот"

TRANSLATE_GUID = get_guid_from_value(TRANSLATE_TEXT)
GPT_GUID = get_guid_from_value(GPT_TEXT)

BUTTON_RESPONSES = {
    TRANSLATE_GUID: "Введи текст, который необходимо перевести ⌨️",
    GPT_GUID: "Начни задавать вопросы, я попробую на них ответить 💭"
}

START_MESSAGE = "Выбери действие 💬"
ERROR_MESSAGE = "Что-то неразборчивое, попробуй снова 🤖"

USER_CHOICE_MAP = {
    TRANSLATE_GUID: TRANSLATE_TEXT,
    GPT_GUID: GPT_TEXT,
}
