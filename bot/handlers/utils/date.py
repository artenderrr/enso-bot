from datetime import date, timedelta

DATE_KEYWORDS = {
    "сегодня": lambda: date.today(),
    "вчера": lambda: date.today() - timedelta(days=1),
    "позавчера": lambda: date.today() - timedelta(days=2)
}

def is_valid_date_format(date: str) -> bool:
    if not isinstance(date, str):
        return False
    if date in DATE_KEYWORDS:
        return True
    parts = date.split(".")
    return (
        len(date) == 10 and
        len(parts) == 3 and
        all(part.isdigit() for part in parts)
    )

def normalize_date(date: str) -> str:
    if date in DATE_KEYWORDS:
        date_object = DATE_KEYWORDS[date]() # type: ignore[no-untyped-call]
        return date_object.strftime("%d.%m.%Y")
    return date
