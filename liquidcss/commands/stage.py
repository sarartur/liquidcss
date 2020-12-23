import argparse
import os


from liquidcss.settings import Settings, Messages
from liquidcss.workspace import WorkSpace
from liquidcss.parsers import create_parser
from liquidcss.stager import Stager
from liquidcss.utils import create_file_hash

"""
Command: liquidcss stage

Description:
    Parses registered files and rewrites them with hashed selectors.
    

Positional Arguments : {id}
    {id} : ID of the file.


Flags:
    [--all -a] : Designates all files.
    [--no-hash -nh] : Prevents the files selectors from hashing.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def stage(file_ids):
    workspace.selector_map.content = None
    stager = Stager(selector_map = workspace.selector_map.content)
    file_map = workspace.file_map.content
    for id_ in sorted(file_ids, key = lambda id_: settings.type_priority.index(next(
        value['type'] for value in file_map.values() if value["id"] == id_
    ))):
        file_key, file_settings = workspace.file_map.key_and_settings_from_id(id_ = id_)
        if create_file_hash(
            path = os.path.join(workspace.src.path, file_key)
        ) != file_settings['hash']:
            Exception(Messages.hash_changed)
        parser = create_parser(type_ = file_settings['type'])
        document = parser.from_file(path = os.path.join(workspace.src.path, file_key))
        if not settings.no_hash:
            stager.toggle_selector_names(objects = document.selectors)
        file_map[file_key]['staged'] = True
        workspace.file_map.content = file_map
        workspace.selector_map.content = stager.selector_map
        workspace.create_file(
            path = os.path.join(workspace.staged.path, file_key), 
            string = document.to_string()
        )

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid stage",
        description="Parses registered files and rewrites them with hashed selectors.",
    )
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        "id",
        nargs = "?",
        help="ID of the file.",
    )
    group.add_argument(
        "--all", "-a",
        action='store_true',
        help="Designate all files.",
    )
    parser.add_argument(
        "--no-hash", "-nh",
        action='store_true',
        help="Prevents the files selectors from hashing.",
    )
    parsed_args = parser.parse_args(args)
    settings.register_from_kwargs(**vars(parsed_args))
    file_ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.file_id, )
    stage(file_ids)
    
        

    


