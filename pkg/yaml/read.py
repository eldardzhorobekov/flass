from typing import Any

import yaml


def read(path: str) -> Any:
    with open(path) as f:
        content = yaml.safe_load(f)
    return content
