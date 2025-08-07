import json
import logging
from dataclasses import is_dataclass
from enum import Enum, StrEnum
from pathlib import Path

logger = logging.getLogger('pytest_plugins.utils')

def get_project_root(marker: str = ".git") -> Path | None:
    path = Path(__file__).resolve()
    for parent in path.parents:
        if (parent / marker).exists():
            return parent
    return None


def serialize_data(obj):
    if isinstance(obj, (Enum, StrEnum)):
        return obj.value
    if is_dataclass(obj):
        return obj.__dict__
    logger.error(f'Object is not serializable: {obj}')
    raise TypeError(f"Type {type(obj)} not serializable")


def open_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_as_json(path: Path, data: dict, default: callable = None) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as json_file:
        text = json.dumps(data, indent=4, default=default) if default else json.dumps(data, indent=4)
        json_file.write(text)


def save_as_markdown(path: Path, data: str) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as md_file:
        md_file.write(data)
