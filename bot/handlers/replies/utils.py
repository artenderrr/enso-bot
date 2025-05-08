def escape_markdown(content: str) -> str:
    RESERVED = set("*_[](){}~`>#+-=|.!")
    return "".join((f"\\{i}" if i in RESERVED else i) for i in content)
