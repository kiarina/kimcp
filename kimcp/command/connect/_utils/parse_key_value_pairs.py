from .split_key_value import split_key_value


def parse_key_value_pairs(
    items: tuple[str, ...],
    *,
    option_name: str,
) -> dict[str, str]:
    result: dict[str, str] = {}

    for item in items:
        key, value = split_key_value(item, option_name=option_name)
        result[key] = value

    return result
