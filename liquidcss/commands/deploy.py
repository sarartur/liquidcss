import argparse
import os

from liquidcss.workspace import WorkSpace 
from liquidcss.settings import Settings, Messages, DocConfig
from liquidcss.utils import display_output

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
    to_console = []
    for id_ in file_ids:
        file_map = workspace.file_map.content
        doc_config = workspace.file_map.settings_from_id(id_ = id_, file_settings = DocConfig)
        if not doc_config.key:
            return [*to_console, Messages.id_not_registered.format(id = id_)]
        if not settings.reverse:
            to_console.append(Messages.file_deployed.format(id = id_, path = doc_config.path))
            if not doc_config.deployed:
                workspace.copy(src = doc_config.path, trgt = os.path.join(workspace.bak.path, doc_config.key))
            workspace.copy(src = os.path.join(workspace.staged.path, doc_config.key), trgt = doc_config.path)
            doc_config.deployed = True
        else:
            if not doc_config.deployed:
                return [*to_console, Messages.file_is_not_deployed]
            workspace.copy(src = os.path.join(workspace.bak.path, doc_config.key), trgt = doc_config.path)
            doc_config.deployed = False
            to_console.append(Messages.deploy_reversed.format(id = id_, path = doc_config.path))
        workspace.file_map.content = {**file_map, **{doc_config.key: doc_config.values}}
    return to_console


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
    to_console = deploy(file_ids = file_ids)
    display_output(to_console)
    
        

    
