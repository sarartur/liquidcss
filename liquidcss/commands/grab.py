import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages
from liquidcss.utils import create_file_key

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
    file_map = workspace.file_map.content
    for path in paths:
        file_key = create_file_key(path)
        if not settings.over:
            if file_map.get(file_key):
                raise Exception(Messages.path_already_registered.format(path = path))
        ext = os.path.basename(path).split('.')[-1]
        type_ = next((key.split('_')[0] for key, value in settings.extensions.items() if ext in value), None)
        if not type_:
            raise Exception(Messages.unkown_extension)
        try: workspace.copy(src = path, trgt = os.path.join(workspace.src.path, file_key))
        except FileNotFoundError: raise Exception(Messages.file_not_found.format(path = path))
        workspace.register(path = path, file_key = file_key, type_ = type_)

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
    grab(paths = paths)
