import os


class StructureManager(object):


    folder_struct = dict(
        root_folder_path = os.path.join('liquidcss_'),
        css = os.path.join('liquidcss_', 'css'),
        html = os.path.join('liquidcss_', 'html'),
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

    @property
    def _missing_key(self):
        for key, value in StructureManager.folder_struct.items():
            if os.path.isdir(os.path.join(self.base_dir, value)):
                continue
            else:
                return key


    def create_file(self, type_, file_name, string):
        path = os.path.join(self.base_dir, StructureManager.folder_struct[type_], file_name)
        with open(path, 'w') as file:
            file.write(string.decode('ascii'))


    def validate_structure(self):
        missing_key = self._missing_key
        if missing_key:
            self._create_folder(folder_struct_key = missing_key)
            self.validate_structure()
        else:
            return True
            



    