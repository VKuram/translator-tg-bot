from dotenv import load_dotenv
import os
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

def get_ai_response(
    messages: list[dict[str, str]],
    ai_model: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
) -> str:
    try:
        client_response = client.chat.completions.create(
            model=ai_model,
            messages=messages,
        )

        text_response = client_response.choices[0].message.content

        print(f"AI: {text_response}")

        return text_response

    except Exception as e:
        print(e)
        return "Что-то пошло не так, попробуй еще раз"

def get_formatted_ai_response(text_response: str) -> str:
    for end_word in END_WORDS:
        if end_word in text_response:
            text_response = text_response.split(end_word)[-1]

    return text_response.replace("<think>", "")

def get_ai_model(model_name: str) -> str:
    return AI_MODELS.get(model_name)
