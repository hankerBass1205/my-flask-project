"""輔助工具函式模組。"""


def multiply(a: int, b: int) -> int:
    """計算兩個整數的乘積。"""
    return a * b


def capitalize_words(text: str) -> str:
    """將字串中每個單字的首字母轉為大寫。"""
    return " ".join(word.capitalize() for word in text.split())
