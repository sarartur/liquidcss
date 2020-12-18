import argparse
import os


from liquidcss.settings import Settings
from liquidcss.workspace import WorkSpace
from liquidcss.parsers import create_parser
from liquidcss.stager import Stager
from liquidcss.utils import create_file_hash

"""
Command: liquidcss stage

Description:
    Used to read in and then rewrite the files from unstaged to staged folder.

Positional Arguments:{file-key}
    {id} - id of the unstaged file.


Flags:
    [--all -a] - hashes selectors in all unstaged files.
    [--no-hash -nh] - still rewrites files after reading them in, but
                        does not hash the selectors.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def stage(file_ids):
    stager = Stager(selector_map = workspace.selector_map)
    file_map = workspace.file_map.conent
    for id_ in sorted(file_ids, key = lambda id_: settings.type_priority.index(next(
        value['type'] for value in file_map.values() if value["id"] == id_
    ))):
        file_key, dict_ = next(
            (key, value) for key, value in file_map.items() if value["id"] == id_
        )
        if create_file_hash(
            path = os.path.join(workspace.src, dict_["path"])
        ) != dict_['hash']:
            Exception("The file has been changed after it was registered by the work space.")
        parser = create_parser(type_ = dict_['type'])
        document = parser.from_file(path = os.path.join(workspace.src, dict_["path"]))
        if not settings.no_hash:
            stager.toggle_selector_names(objects = document.selectors)
        file_map[file_key]['staged'] = True
        workspace.file_map.content = file_map
        workspace.create_file(
            path = os.path.join(workspace.staged, dict_['path']), 
            string = document.to_string()
        )

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid stage",
        description="initializes or resets the works space",
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
    parser.add_argument(
        "--no-hash", "-nh",
        action='store_true',
        help="Bypasses the default block on --reset",
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.vaules()
    ) if settings.all else tuple(parsed_args.file_id, )
    stage(file_ids)
    
        

    


