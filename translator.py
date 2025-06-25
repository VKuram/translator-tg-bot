import requests

def translate_text(text, target_language="ru", source_language="auto"):
    url = "https://translate.googleapis.com/translate_a/single"
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
