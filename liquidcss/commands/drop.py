import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages

"""
Command: liquidcss drop

Description:
    Removes files from the WorkSpace.

Positional Arguments : {file_key}
    {id} : The ID to a file.

Optional Arguments:
    [--all -a] : Designates all files.
    [--hard -h] : Will remove a file even if it is deployed.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def drop(file_ids):
    file_map = workspace.file_map.content
    for id_ in file_ids:
        file_key, file_settings = workspace.file_map.key_and_settings_from_id(id_ = id_)
        if not settings.hard and file_settings['deployed']:
            raise Exception(Messages.file_is_deployed)
        workspace.remove_files(paths = (
            os.path.join(workspace.src.path, file_key),
            os.path.join(workspace.staged.path, file_key),
            os.path.join(workspace.bak.path, file_key)
        ))
        del file_map[file_key]
        workspace.file_map.content = file_map

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid drop",
        description="Removes files from the workspace."
    )
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        "id",
        nargs = "?",
        help="The ID to a file.",
    )
    group.add_argument(
        "--all", "-a",
        action='store_true',
        help="Designates all files."
    )
    parser.add_argument(
        "--hard",
        action = "store_true",
        help="Will remove a file even if it is deployed."
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    drop(file_ids = file_ids)
        