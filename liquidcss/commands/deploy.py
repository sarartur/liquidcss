import argparse
import os

from liquidcss.workspace import WorkSpace 
from liquidcss.settings import Settings

"""
Command: liquidcss deploy

Description:
    Deploys staged files.

Positional Arguments: {file_id}
    {file_id} - key to a staged file.

Optional Arguments:
    [--all -a] - allows skipping of 'file_key' argument and specifies all files.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = WorkSpace)


def deploy(file_ids):
    file_map = workspace.file_map.content
    for id_ in file_ids:
        dict_ = next(
            value for value in file_map.values() if value["id"] == id_
        )
        workspace.copy(src = dict_['path'], trgt = os.path.join(workspace.bak.path, dict_['name']))
        workspace.copy(src = os.path.join(workspace.staged.path, dict_['name']), trgt = dict_['path'])
        dict_['deployed'] = True
        workspace.file_map.content = file_map

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid deploy",
        description="Deploys staged files.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "id",
        nargs = "?",
        help="Resets the work space. The reset will be blocked if there are files deployed.",
    )
    group.add_argument(
        "--all", "-a",
        action='store_true',
        help="Resets the work space. The reset will be blocked if there are files deployed.",
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.vaules()
    ) if settings.all else tuple(parsed_args.file_id, )
    deploy(file_ids = file_ids)
    
        

    
