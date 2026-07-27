import json
from typing import Any

import rich_click as click


def echo_json(data: Any) -> None:
    click.echo(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
