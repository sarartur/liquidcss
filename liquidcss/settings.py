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