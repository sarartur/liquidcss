import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings
from liquidcss.utils import create_file_key

"""
Command: liquidcss grab

Description:
    Used to intially add files to the workspace. 

Positional Arguments:{file_path}
    {file_path} - the path to the file to be grabbed.

Flags:
    [-o --over] : overwrites a file.
    [-r --read] : reads in a txt file of paths.
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
                raise Exception("A file with that path is already registered.")
        ext = os.path.basename(path).split('.')[-1]
        type_ = next((key.split('_')[0] for key, value in settings.extensions.items() if ext in value), None)
        if not type_:
            raise Exception("File with unknown extension")
        try: workspace.copy(src = path, trgt = os.path.join(workspace.src.path, file_key))
        except FileNotFoundError: raise Exception(f"File not found at {path}.")
        workspace.register(path = path, file_key = file_key, type_ = type_)

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid grab",
        description="Used to intially add files to the workspace. ",
    )
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        'file',
        nargs = "?",
        help = "the path to the file"
    )
    group.add_argument(
        "--read", "-r",
        help="read in paths from a txt file.",
    )
    parser.add_argument(
        "--over", "-o",
        action='store_true',
        help="overwrites any files with the matching path.",
    )
    parsed_args = parser.parse_args(args)
    paths =  _read_in_txt(parsed_args.read) if parsed_args.read else [parsed_args.file, ]
    settings.register_from_kwargs(args = parsed_args)
    grab(paths = paths)
