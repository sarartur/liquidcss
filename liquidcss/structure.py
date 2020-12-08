import os


class StructureManager(object):


    folder_struct = dict(
        root_folder_path = os.path.join('liquidcss_'),
        css_folder_path = os.path.join('liquidcss_', 'css'),
        html_folder_path = os.path.join('liquidcss_', 'html'),
    )


    def __init__(self, base_dir):
        self.base_dir = base_dir


    def _create_folder(self, folder_struct_key):
        os.mkdir(
            os.path.join(
                self.base_dir, 
                StructureManager.folder_struct[folder_struct_key]
            )
        )


    def _validate_structure(self):
        for key, value in StructureManager.folder_struct.items():
            if os.path.isdir(os.path.join(self.base_dir, value)):
                continue
            else:
                return key


    def create_structure(self):
        missing_key = self._validate_structure()
        if missing_key:
            self._create_folder(folder_struct_key = missing_key)
            self.create_structure()
        else:
            return True
            



    