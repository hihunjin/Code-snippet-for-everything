from datetime import datetime


def get_current_date() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")
