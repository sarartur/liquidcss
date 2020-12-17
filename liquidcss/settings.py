class Settings(object):

    default = {
        "worksapce_folder_name": "liq",
        "css_ext": ["css"],
        "js_ext": ["js"],
        "html_ext": ["html"]
    }

    def __init__(self, workspace):
        self.reset = False
        self.hard = False
        self.over = False
        self.css_ext = list()
        self.js_ext = list()
        self.html_ext = list()
        
        self.update_from_dict(
            **workspace.settings.content
        )

    def update_from_argparse(self, args):
        self.update_from_dict(**vars(args))

    def update_from_dict(self, **kwargs):
        self.__dict__.update(**kwargs)