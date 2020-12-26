import argparse
import os
from pathlib import Path

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages
from liquidcss.utils import create_file_key, display_output

"""
Command: liquidcss grab

Description:
    Registers files with the WorkSpace. 

Positional Arguments : {path}
    {path} : The path to the file.

Flags:
    [-o --over] : Overwrites a registered file with the matching path.
    [-r --read] : Reads in a txt file containing paths.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def _read_in_txt(path):
    with open(path, 'r') as file:
        return tuple(path.strip() for path in file.readlines())

def grab(paths):
    to_console = []
    file_map = workspace.file_map.content
    for path in paths:
        key = create_file_key(path)
        if not settings.over:
            if file_map.get(key):
                return [*to_console, Messages.path_already_registered.format(path = path)]
        type_ = settings.get_type(ext = Path(path).suffix.replace('.', ''))
        if not type_:
            return [*to_console, Messages.unknown_extension]
        try: workspace.copy(src = path, trgt = os.path.join(workspace.src.path, key))
        except FileNotFoundError: return [*to_console, Messages.file_not_found.format(path = path)]
        workspace.register(path = path, key = key, type_ = type_)
        to_console.append(Messages.file_registered.format(path = path))
    return to_console

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid grab",
        description="Registers files with the workspace.",
    )
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        'file',
        nargs = "?",
        help = "The path to the file."
    )
    group.add_argument(
        "--read", "-r",
        help="Reads in a txt file containing paths.",
    )
    parser.add_argument(
        "--over", "-o",
        action='store_true',
        help="Overwrites a registered file with the matching path.",
    )
    parsed_args = parser.parse_args(args)
    paths =  _read_in_txt(parsed_args.read) if parsed_args.read else [parsed_args.file, ]
    settings.register_from_kwargs(args = parsed_args)
    to_console = grab(paths = paths)
    display_output(to_console)

