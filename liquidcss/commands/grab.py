import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings
from liquidcss.utils import create_file_id

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
        return list(file.readlines())

def grab(paths):
    file_map = workspace.file_map.content
    for path in paths:
        file_id = create_file_id(path)
        if not settings.over:
            if file_map.get(file_id):
                raise Exception("A file with that path is already registered.")
        workspace.register(path = path, file_id = file_id)

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid grab",
        description="adds files to the workspace",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        'file',
        description = "the path to the file"
    )
    group.add_argument(
        "-read --r",
        help="read in paths from a txt file.",
    )
    parser.add_argument(
        "--over", "-o",
        action='store_true',
        help="overwrites any files with the matching path.",
    )
    parsed_args = parser.parse_args(args)
    paths =  _read_in_txt(parsed_args.read) if parsed_args.read else [parsed_args.file, ],
    settings.update_from_argparse(args = parsed_args)
    grab(paths = paths)
