def is_valid_tin(inn: str) -> bool:
    if not inn.isdigit():
        return False
    if len(inn) == 10 or len(inn) == 12:
        return True
    return False
