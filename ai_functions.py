from dotenv import load_dotenv
import os
from together import Together

load_dotenv()

API_URL = "https://api.together.xyz/v1"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")

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

def get_ai_response(messages) -> str:
    try:
        client_response = client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
        )

        text_response = client_response.choices[0].message.content

        print(f"AI: {text_response}")

        return text_response

    except Exception as e:
        print(e)
        return "Что-то пошло не так, попробуй еще раз"

def format_ai_response(text_response: str) -> str:
    for end_word in END_WORDS:
        if end_word in text_response:
            text_response = text_response.split(end_word)[-1]

    return text_response.replace("<think>", "")
