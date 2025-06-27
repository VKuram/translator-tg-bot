def _detect_language_balance(text: str) -> tuple[str]:
    en_count = sum(1 for char in text.lower() if "a" <= char <= "z")
    ru_count = sum(1 for char in text.lower() if "а" <= char <= "я" or char == "ё")

    if ru_count > en_count:
        return "auto", "en"
    else:
        return "auto", "ru"

def detect_language(text: str) -> tuple[str]:
    """Определение, с какого на какой язык требуется перевод"""
    if not isinstance(text, str):
        return None, None
    en_chars = set("abcdefghijklmnopqrstuvwxyz")
    ru_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

    has_en = any(char in en_chars for char in text.lower())
    has_ru = any(char in ru_chars for char in text.lower())

    if has_ru and not has_en:
        return "auto", "en"
    else:
        return _detect_language_balance(text.lower())  # Смешанный текст
