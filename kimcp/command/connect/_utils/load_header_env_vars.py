import rich_click as click

from .split_key_value import split_key_value


def load_header_env_vars(items: tuple[str, ...]) -> dict[str, str]:
    result: dict[str, str] = {}

    for item in items:
        header_name, env_name = split_key_value(item, option_name="--header-from-env")
        value = _load_required_env_var(env_name)
        result[header_name] = value

    return result


def _load_required_env_var(env_name: str) -> str:
    import os

    if env_name not in os.environ:
        raise click.ClickException(
            f"Environment variable not found for --header-from-env: {env_name}"
        )

    return os.environ[env_name]
