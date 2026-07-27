import rich_click as click


def split_key_value(item: str, *, option_name: str) -> tuple[str, str]:
    if "=" not in item:
        raise click.ClickException(f"{option_name} expects KEY=VALUE format: {item}")

    key, value = item.split("=", 1)
    if not key:
        raise click.ClickException(f"{option_name} key must not be empty: {item}")

    return key, value
