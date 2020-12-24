import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages, DocConfig
from liquidcss.utils import create_file_key, display_output

"""
Command: liquidcss status

Description:
    Displays information about the files registered with the WorkSpace.

Positional Arguments:{id}
    {id} - ID of the file.

Flags:
    [-a --all] : Designates all files.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def status(ids):
    to_console = []
    for id_ in ids:
        doc_config = workspace.file_map.settings_from_id(id_ = id_, file_settings = DocConfig)
        if not doc_config:
            return [*to_console, Messages.id_not_registered]
        to_console.append(Messages.status.format(**doc_config.values))
    return to_console
    
def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid status",
        description="Displays information about the files registered with the WorkSpace.",
    )
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        'id',
        nargs = "?",
        help = "ID of the file."
    )
    group.add_argument(
        "--all", "-a",
        action = "store_true",
        help="Designates all files.",
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    to_console = status(ids = ids)
    display_output(to_console)
