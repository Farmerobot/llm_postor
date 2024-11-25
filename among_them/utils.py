import json
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Generator

import toml


@contextmanager
def raise_or_quit(msg: str, quit: bool = False) -> Generator[None, None, None]:
    try:
        yield
    except Exception as ex:
        if quit:
            print(msg + ", quitting...")
            sys.exit(1)
        raise ex


def _read(path: str, label: str, parser: Callable, quit: bool = False) -> dict:
    pathlib_path = Path(path)
    with raise_or_quit(f"Could not read the file {str(path)}", quit):
        content = pathlib_path.read_text()

    with raise_or_quit(f'Could not parse {label} file "{str(path)}"', quit):
        return parser(content)


def read_toml(path: str, quit: bool = False) -> dict:
    return _read(path, "toml", toml.loads, quit)


def read_json(path: str, quit: bool = False) -> dict:
    return _read(path, "json", json.loads, quit)
