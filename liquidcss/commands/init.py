import argparse
import os

from liquidcss.workspace import WorkSpace
from liquidcss.msgs import (
    files_are_deployed_msg, workspace_exists_msg,
    hard_reset_warning_msg, succesful_init_msg, 
    succesful_reset_msg, reset_cancled, workspace_does_not_exist
)
from liquidcss.settings import Settings

"""
Command: liquidcss init

Description:
    Intializes the workspace.

Optional Arguments:
    [--reset -r] - resets the work space. The reset will be blocked if there are files deployed.
    [--hard] - resets the work space.
"""

workspace = WorkSpace(base_dir = os.getcwd())
settings = Settings(workspace = workspace)

def init():
    if not settings.reset:
        if workspace.base.exists:
            raise Exception(workspace_exists_msg)
        workspace.init()
        return succesful_init_msg
    if not workspace.base.exists:
        raise Exception(workspace_does_not_exist)
    if not settings.hard:
        deployed = workspace.files_deployed
        if deployed:
            raise Exception(files_are_deployed_msg.format(deployed))
        workspace.reset()
        return succesful_reset_msg
    else:
        print(hard_reset_warning_msg.format(workspace.bak.path))
        user_input = input().strip().lower().startswith('y')
        if user_input:
            workspace.reset()
            return succesful_reset_msg
        raise Exception(reset_cancled)

def main(args):
    parser = argparse.ArgumentParser(
        prog="liquid init",
        description="initializes or resets the works space",
    )
    parser.add_argument(
        "--reset", "-r",
        action='store_true',
        help="Resets the work space. The reset will be blocked if there are files deployed.",
    )
    parser.add_argument(
        "--hard",
        action='store_true',
        help="Bypasses the default block on --reset",
    )
    parsed_args = parser.parse_args(args)
    if parsed_args.hard and not parsed_args.reset:
        parser.error("[--hard] can not be passed in without [--reset -r]")
    settings.register_from_kwargs(**vars(parsed_args))

    msg = init()
    print(msg)

    
