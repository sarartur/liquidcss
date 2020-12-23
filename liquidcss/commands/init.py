import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.settings import Settings, Messages

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
    if not settings.reset:
        if workspace.base.exists:
            raise Exception(Messages.workspace_exists)
        workspace.init()
        return
    if not workspace.base.exists:
        raise Exception(Messages.workspace_does_not_exist)
    if not settings.hard:
        deployed = workspace.files_deployed
        if deployed:
            raise Exception(Messages.files_are_deployed.format(deployed))
        workspace.reset()
        return
    else:
        print(Messages.hard_reset_warning.format(workspace.bak.path))
        user_input = input().strip().lower().startswith('y')
        if user_input:
            workspace.reset()
            return
        raise Exception(Messages.reset_cancled)

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
    init()

    
