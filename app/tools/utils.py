from typing import Iterable, Callable


def sanitize_string(query_parameter: str) -> str:
    return "".join(char for char in query_parameter if char.isalpha() or char in "_")

def formatter(sequence: Iterable, element_modifier: Callable) -> Iterable:
    return (element_modifier(element) for element in sequence)
