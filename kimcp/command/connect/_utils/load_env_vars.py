import os

import rich_click as click


def load_env_vars(items: tuple[str, ...]) -> dict[str, str]:
    result: dict[str, str] = {}

    for env_name in items:
        if env_name not in os.environ:
            raise click.ClickException(f"Environment variable not found for --env-from: {env_name}")
        result[env_name] = os.environ[env_name]

    return result
