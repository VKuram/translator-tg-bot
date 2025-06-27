import requests

from language_detector import detect_language

def translate_text(text: str) -> str:
    """Перевод текста с автоопределением языков"""
    url = "https://translate.googleapis.com/translate_a/single"
    source_language, target_language = detect_language(text)

    params = {
        "client": "gtx",
        "sl": source_language,  # исходный язык (auto = автоопределение)
        "tl": target_language,  # целевой язык (ru, en, fr и т. д.)
        "dt": "t",
        "q": text,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        translated_text = response.json()[0][0][0]
        return f"`{translated_text}`"
    else:
        return f"Ошибка: {response.status_code}"
