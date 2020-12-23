class InitMsgs(object):
    workspace_exists = "WorkSpace already exists"
    files_are_deployed = "Files are deployed. Ids: {}"
    hard_reset_warning = (
        "The workspace will be reset even if files are deployed. \n"
        "If the worksapce is corrupted and you can not revert deployed files, \n"
        "consider retreiving files from: \n"
        "\n"
        "\t{} \n"
        "\n"
        "The program will attempt to preserve a copy of the folder. \n"
        "Would you like to continue? (Y/N)"
    )
    succesful_init= "Succesfully created workspace"
    succesful_reset = "Succesfully reset the workspace"
    reset_cancled = "Hard reset cancled"
    workspace_does_not_exist = "No WorkSpace detected"