import asyncio

from telegram import Update
from telegram.ext import ContextTypes
from together import Together

from messages import *
from constants import API_URL, AI_MODELS, END_WORDS, ERROR_TEXT, TOGETHER_API_KEY

client = Together(api_key=TOGETHER_API_KEY, base_url=API_URL, max_retries=5)

async def get_ai_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    messages: list[dict[str, str]],
    ai_model: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
) -> str:
    stop_animation = asyncio.Event()

    loading_task = asyncio.create_task(send_loading_message(update, context, stop_animation))

    try:
        loop = asyncio.get_event_loop()
        client_response = await loop.run_in_executor(None, lambda: client.chat.completions.create(
            model=ai_model,
            messages=messages,
        ))

        text_response = client_response.choices[0].message.content

        print(f"AI: {text_response}")

        stop_animation.set()
        await loading_task

        return text_response

    except Exception as e:
        context.user_data["ai_response_received"] = True

        print(e)

        return ERROR_TEXT

    finally:
        stop_animation.set()
        if not loading_task.done():
            loading_task.cancel()

def get_formatted_ai_response(text_response: str) -> str:
    for end_word in END_WORDS:
        if end_word in text_response:
            text_response = text_response.split(end_word)[-1]

    return text_response.replace("<think>", "")

def get_ai_model(model_name: str) -> str:
    return AI_MODELS.get(model_name)
