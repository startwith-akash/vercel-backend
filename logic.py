def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters to prevent injection attacks"""
    banned = ["<", ">", "{", "}", ";", "script"]
    for b in banned:
        text = text.replace(b, "")
    return text


def calculate_actual(answer: str) -> int:
    """
    Calculate actual skill level based on response quality
    - Longer, detailed responses = higher skill level
    - Shorter responses = lower skill level
    """
    if len(answer) > 40:
        return 4
    elif len(answer) > 20:
        return 3
    else:
        return 1