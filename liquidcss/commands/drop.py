import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages
from liquidcss.utils import display_output

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

def drop(ids):
    to_console = []
    file_map = workspace.file_map.content
    for id_ in ids:
        doc_config = workspace.file_map.key_and_settings_from_id(id_ = id_)
        if not settings.hard and doc_config.deployed:
            return [*to_console, Messages.file_is_deployed]
        workspace.remove_files(paths = (
            os.path.join(workspace.src.path, doc_config.key),
            os.path.join(workspace.staged.path, doc_config.key),
            os.path.join(workspace.bak.path, doc_config.key)
        ))
        del file_map[doc_config.key]
        workspace.file_map.content = file_map
        to_console.append(Messages.file_dropped.format(id_, doc_config.path))
    return to_console


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
    ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    to_console = drop(ids = ids)
    display_output(to_console)

        