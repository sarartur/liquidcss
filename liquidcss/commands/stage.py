import argparse
import os


from liquidcss.settings import Settings, Messages, DocConfig
from liquidcss.workspace import WorkSpace
from liquidcss.parsers import create_parser
from liquidcss.stager import Stager
from liquidcss.utils import create_file_hash, display_output

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

def stage(ids):
    to_console = []
    stager = Stager(selector_map = dict())
    for id_ in ids:
        if not workspace.file_map.settings_from_id(id_ = id_, file_settings = DocConfig):
            return [*to_console, Messages.id_not_registered.format(id = id_)]
    for id_ in settings.sort_by_priority(ids = ids, file_map = workspace.file_map.content):
        file_map = workspace.file_map.content
        doc_config = workspace.file_map.settings_from_id(id_ = id_, file_settings = DocConfig)
        if create_file_hash(
            path = os.path.join(workspace.src.path, doc_config.key)
        ) != doc_config.hash:
            return [*to_console, Messages.hash_changed]
        parser = create_parser(type_ = doc_config.type)
        document = parser.from_file(path = os.path.join(workspace.src.path, doc_config.key))
        if not settings.no_hash:
            stager.toggle_selector_names(objects = document.selectors)
        doc_config.staged = True
        workspace.file_map.content = {**file_map, **{doc_config.key: doc_config.values}}
        workspace.selector_map.content = stager.selector_map
        workspace.create_file(
            path = os.path.join(workspace.staged.path, doc_config.key), 
            string = document.to_string()
        )
        to_console = [*to_console, Messages.file_staged.format(id = id_)]
    return to_console

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
    ids = tuple(
        dict_['id'] for dict_ in workspace.file_map.content.values()
    ) if settings.all else tuple(parsed_args.id, )
    to_console = stage(ids)
    display_output(to_console)
        

    


