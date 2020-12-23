class Settings(object):

    default = {
        "worksapce_folder_name": "liq",
        "css_ext": ["css"],
        "js_ext": ["js"],
        "html_ext": ["html"]
    }

    def __init__(self, workspace = None):

        self.type_priority = [
            'css', 'html', 'js'
        ]

        #All possible attributes that can registered.
        self.reset = False
        self.hard = False
        self.over = False
        self.no_hash = False
        self.all = False
        self.reverse = False
        self.css_ext = list()
        self.js_ext = list()
        self.html_ext = list()
        
        self.register_from_kwargs(
            **workspace.settings.content
        )

    def register_from_kwargs(self, **kwargs):
        self.__dict__.update(**kwargs)

    @property
    def extensions(self):
        return {key: value for key, value in  self.__dict__.items() if key.endswith('_ext')}

class Messages(object):
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
    status = (
        "\t[File ID: {id}]\n"
        "\t  name: {name}\n"
        "\t  path: {path}\n"
        "\t  type: {type}\n"
        "\t  hash: {hash}\n"
        "\t  staged: {staged}\n"
        "\t  deployed: {deployed}\n"
    )
    id_not_registered = "No file with that ID is registered"
    hash_changed = "The file has been changed after it was registered by the work space."
    path_already_registered = (
        "\tA file with that path is already registered: \n"
        "\t  {path}"
    )
    unkown_extension = "File with unknown extension"
    file_not_found = "File not found at {path}."
    file_is_deployed = "File is deployed"
    file_is_not_deployed = "File is not deployed"