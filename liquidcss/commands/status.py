import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages
from liquidcss.utils import create_file_key

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

def status(file_ids):
    for id_ in file_ids:
        file_key, file_settings = workspace.file_map.key_and_settings_from_id(id_ = id_)
        if not file_key:
            raise Exception(Messages.id_not_registered)
        print(Messages.status.format(**file_settings))
    
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
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    status(file_ids = file_ids)
