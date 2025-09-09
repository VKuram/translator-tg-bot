import asyncio

from telegram import Update
from telegram.ext import ContextTypes
from together import Together

from constants import API_URL, AI_MODELS_MAP, END_WORDS, ERROR_MESSAGE, TOGETHER_API_KEY, SYSTEM_PROMPT
from messages import send_loading_message

client = Together(api_key=TOGETHER_API_KEY, base_url=API_URL, max_retries=5)

async def get_ai_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    messages: list[dict[str, str]],
    ai_model: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
) -> str:
    """Получение ответа на запрос от AI"""
    stop_animation = asyncio.Event()

    loading_task = asyncio.create_task(send_loading_message(update, context, stop_animation))

    try:
        loop = asyncio.get_event_loop()
        client_response = await loop.run_in_executor(None, lambda: client.chat.completions.create(
            model=ai_model,
            messages=messages,
        ))  # Голый ответ AI

        text_response = client_response.choices[0].message.content  # Текст ответа

        print(f"AI: {text_response}")  # Лог ответа от AI

        stop_animation.set()
        await loading_task

        return text_response

    except Exception as e:
        context.user_data["ai_response_received"] = True

        print(e)  # Лог ошибки

        return ERROR_MESSAGE

    finally:
        stop_animation.set()
        if not loading_task.done():
            loading_task.cancel()

def get_formatted_ai_response(text_response: str) -> str:
    """Форматирование ответа от AI"""
    for end_word in END_WORDS:
        if end_word in text_response:
            text_response = text_response.split(end_word)[-1]

    return text_response.replace("<think>", "")

def get_ai_model(model_name: str) -> str:
    """Получение модели AI"""
    return AI_MODELS_MAP.get(model_name)

def get_prompt_message_log() -> dict[str, str]:
    """Получение лога промпта"""
    return {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }

def get_user_message_log(message_text: str)-> dict[str, str]:
    """Получение лога сообщения пользователя"""
    return {
        "role": "user",
        "content": message_text,
    }

def get_ai_message_log(message_text: str)-> dict[str, str]:
    """Получение лога сообщения AI"""
    return {
        "role": "assistant",
        "content": message_text,
    }
