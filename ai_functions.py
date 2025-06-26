import asyncio
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from together import Together

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

client = Together(api_key=TOGETHER_API_KEY, base_url=API_URL, max_retries=5)

async def get_ai_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    messages: list[dict[str, str]],
    ai_model: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
) -> str:
    stop_animation = asyncio.Event()

    loading_message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Подожди, думаю... "
    )

    async def send_loading_message():
        spinner = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]
        while not stop_animation.is_set():
            for frame in spinner:
                if stop_animation.is_set():
                    break
                try:
                    await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=loading_message.message_id,
                        text=f"Подожди, думаю... {frame}"
                    )
                    await asyncio.sleep(0.15)
                except:
                    break

    loading_task = asyncio.create_task(send_loading_message())

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
        await loading_message.delete()

        return text_response

    except Exception as e:
        context.user_data["ai_response_received"] = True

        print(e)
        await loading_message.edit_text("Произошла ошибка при обработке запроса")

        return ""

    finally:
        # 9. Гарантированная очистка
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
