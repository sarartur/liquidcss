import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages
from liquidcss.utils import display_output

"""
Command: liquidcss init

Description:
    Initializes the WorkSpace.

Optional Arguments:
    [--reset -r] : Resets the WorkSpace.
    [--hard, -hr] : Resets the WorkSpace even if files are deployed.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def init():
    to_console = []
    if settings.reset:
        if settings.hard:
            workspace.reset()
            return [*to_console, Messages.workspace_reset]
        deployed = workspace.files_deployed
        if deployed:
            return [*to_console, Messages.files_are_deployed.format(deployed)]
        workspace.reset()
        return [*to_console, Messages.workspace_reset]
    if workspace.base.exists:
        return [*to_console, Messages.workspace_exists]
    workspace.init()
    return [*to_console, Messages.workspace_created]

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid init",
        description="Initializes the WorkSpace.",
    )
    parser.add_argument(
        "--reset", "-r",
        action='store_true',
        help="Resets the WorkSpace.",
    )
    parser.add_argument(
        "--hard", "-hr",
        action='store_true',
        help="Resets the WorkSpace even if files are deployed.",
    )
    parsed_args = parser.parse_args(args)
    if parsed_args.hard and not parsed_args.reset:
        parser.error("[--hard] can not be passed in without [--reset -r]")
    settings.register_from_kwargs(**vars(parsed_args))
    to_console = init()
    display_output(to_console)

    
