def sanitize_string(query_parameter: str) -> str:
    return "".join(char for char in query_parameter if char.isalpha() or char in "_")
