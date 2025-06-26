def _detect_language_balance(text: str) -> tuple[str]:
    en_count = sum(1 for char in text if "a" <= char <= "z" or "A" <= char <= "Z")
    ru_count = sum(1 for char in text if "а" <= char <= "я" or "А" <= char <= "Я" or char in "ёЁ")

    if (en_count == ru_count) or ((en_count + ru_count) == 0):
        return "auto", "ru"
    elif en_count > ru_count:
        return "ru", "en"
    elif ru_count > en_count:
        return "en", "ru"

def detect_language(text: str) -> tuple[str]:
    if not isinstance(text, str):
        return None, None
    en_chars = set("abcdefghijklmnopqrstuvwxyz")
    ru_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

    has_en = any(char in en_chars for char in text.lower())
    has_ru = any(char in ru_chars for char in text.lower())

    if has_en and not has_ru:
        return "ru", "en"
    elif has_ru and not has_en:
        return "en", "ru"
    else:
        return _detect_language_balance(text.lower())  # Смешанный текст
