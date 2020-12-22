import argparse
import os

from liquidcss.workspace import WorkSpace 
from liquidcss.settings import Settings

"""
Command: liquidcss deploy

Description:
    Deploys staged files.

Positional Arguments: {file_id}
    {id} - The id to a staged file.

Optional Arguments:
    [--all -a] - allows skipping of 'file_key' argument and specifies all files.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)


def deploy(file_ids):
    file_map = workspace.file_map.content
    for id_ in file_ids:
        file_key, file_settings = next((
            (key, value) for key, value in file_map.items() if value["id"] == id_
        ), (None, None))
        if not file_key:
            raise Exception("The file with that Id does not exist")
        if not settings.reverse:
            if not file_settings['deployed']:
                workspace.copy(src = file_settings['path'], trgt = os.path.join(workspace.bak.path, file_key))
            workspace.copy(src = os.path.join(workspace.staged.path, file_key), trgt = file_settings['path'])
            file_settings['deployed'] = True
        else:
            if not file_settings['deployed']:
                raise Exception("File is not deployed")
            workspace.copy(src = os.path.join(workspace.bak.path, file_key), trgt = file_settings['path'])
            file_settings['deployed'] = False
            workspace.remove_files(paths = (os.path.join(workspace.bak.path, file_key), ))
        workspace.file_map.content = file_map

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid deploy",
        description="Deploys and undeploysstaged files.",
    )
    group = parser.add_mutually_exclusive_group(required = True)
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
    parser.add_argument(
        "--reverse", '-r',
        action = 'store_true',
        help = "reverts the currently deployed files"
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    deploy(file_ids = file_ids)
    
        

    
