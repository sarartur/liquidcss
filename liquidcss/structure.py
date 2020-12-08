import os


class StructureManager(object):

    base_folder_name = 'liquidcss_'
    folder_struct = dict(
        root_folder_path = os.path.join(base_folder_name),
        css = os.path.join(base_folder_name, 'batch', 'css'),
        html = os.path.join(base_folder_name, 'batch', 'html'),
        mapping = os.path.join(base_folder_name, 'batch')
    )

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def _create_folder(self, folder_struct_key: str):
        os.makedirs(
            os.path.join(
                self.base_dir, 
                StructureManager.folder_struct[folder_struct_key]
            )
        )

    @property
    def _missing_key(self: str) -> str:
        for key, value in StructureManager.folder_struct.items():
            if os.path.isdir(os.path.join(self.base_dir, value)):
                continue
            else:
                return key

    def create_file(self, type_: str, file_name: str, string: str):
        path = os.path.join(self.base_dir, StructureManager.folder_struct[type_], file_name)
        with open(path, 'w') as file:
            file.write(string)

    def validate_structure(self):
        missing_key = self._missing_key
        if missing_key:
            self._create_folder(folder_struct_key = missing_key)
            self.validate_structure()



    