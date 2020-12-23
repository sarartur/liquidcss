import argparse
import os

from liquidcss.workspace import WorkSpace 
from liquidcss.settings import Settings, Messages

"""
Command: liquidcss deploy

Description:
    Deploys staged files and reverts deployed files.

Positional Arguments : {id}
    {id} : The ID to a file.

Optional Arguments:
    [--all -a] : Designates all files.
    [--reverse -r] : Reverts deployed files.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)


def deploy(file_ids):
    file_map = workspace.file_map.content
    for id_ in file_ids:
        file_key, file_settings = workspace.file_map.key_and_settings_from_id(id_ = id_)
        if not file_key:
            raise Exception(Messages.id_not_registered)
        if not settings.reverse:
            if not file_settings['deployed']:
                workspace.copy(src = file_settings['path'], trgt = os.path.join(workspace.bak.path, file_key))
            workspace.copy(src = os.path.join(workspace.staged.path, file_key), trgt = file_settings['path'])
            file_settings['deployed'] = True
        else:
            if not file_settings['deployed']:
                raise Exception(Messages.file_is_not_deployed)
            workspace.copy(src = os.path.join(workspace.bak.path, file_key), trgt = file_settings['path'])
            file_settings['deployed'] = False
        workspace.file_map.content = file_map

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid deploy",
        description="Deploys staged files and reverts deployed files.",
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
        help="Designates all files.",
    )
    parser.add_argument(
        "--reverse", '-r',
        action = 'store_true',
        help = "Reverts deployed files."
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    deploy(file_ids = file_ids)
    
        

    
