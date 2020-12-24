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
        self.workspace = workspace

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

    def sort_by_priority(self, ids, file_map):
        return sorted(ids, key = lambda id_: self.type_priority.index(next(
            value['type'] for value in file_map.values() if value["id"] == id_
        )))

    def register_from_kwargs(self, **kwargs):
        self.__dict__.update(**kwargs)

    @property
    def extensions(self):
        return {key: value for key, value in  self.__dict__.items() if key.endswith('_ext')}

    def get_type(self, ext):
        return next(
            (key.split('_')[0] for key, value in self.extensions.items() if ext in value), None
        )

class DocConfig(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    @property
    def values(self):
        return {key: value for (key, value) in self.__dict__.items() if key != 'key'}


class Messages(object):
    workspace_exists = "\tWorkSpace already exists."
    files_are_deployed = "\tFiles are deployed. Ids: {}"
    successfull_init= "\tSuccessfully created workspace."
    successfull_reset = "\tSuccessfully reset the workspace."
    no_workspace_found = "\tNo WorkSpace found."
    status = (
        "\t[ID: {id}]\n"
        "\t  name: {name}\n"
        "\t  path: {path}\n"
        "\t  type: {type}\n"
        "\t  hash: {hash}\n"
        "\t  staged: {staged}\n"
        "\t  deployed: {deployed}\n"
    )
    id_not_registered = "\tNo file with ID: {id} is registered."
    hash_changed = "\tFile has been changed after it was registered."
    path_already_registered = (
        "\tFile the path is already registered. \n"
        "\t  {path}"
    )
    unknown_extension = "\tFile with unknown extension."
    file_not_found = "\tFile not found at {path}."
    file_is_deployed = "\tFile is deployed."
    file_is_not_deployed = "\tFile is not deployed."
    file_staged = (
        "\tFile staged:\n"
        "\t  ID: {id}"
    )
    workspace_created = "\tWorksSpace created."
    workspace_reset = "\tWorkSpace reset."
    file_registered = (
        "\tFile registered to the WorkSpace with the following path:\n"
        "\t  {path}"
    )
    file_dropped = (
        "\tRemoved the following file from the WorkSpace:\n"
        "\t  ID: {id}\n"
        "\t  path: {path}\n"
    )
    file_deployed = (
        "\tDeployed the following file.\n"
        "\t  ID: {id}\n"
        "\t  path: {path}\n"
    )
    deploy_reversed = (
        "\tReversed deployment of the following file.\n"
        "\t  ID: {id}\n"
        "\t  path: {path}\n"
    )