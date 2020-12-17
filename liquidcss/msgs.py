workspace_exists_msg = "WorkSpace already exists"

files_are_deployed_msg = (
    r"Files are deployed. Run liquid revert {file} "
    "" + "to undeploy files. Deployed file ids {}"
)

hard_reset_warning_msg = (
    "The workspace will be reset even if files are deployed. \n"
    "If the worksapce is corrupted and you can not revert deployed files, \n"
    "consider retreiving files from: \n"
    "\n"
    "\t{} \n"
    "\n"
    "The program will attempt to preserve a copy of the folder. \n"
    "Would you like to continue? (Y/N)"
)

succesful_init_msg = "Succesfully created workspace"

succesful_reset_msg = "Succesfully reset the workspace"

reset_cancled = "Hard reset cancled"

workspace_does_not_exist = "No WorkSpace detected"