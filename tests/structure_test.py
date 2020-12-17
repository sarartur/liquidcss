import json
import os


class Structure(object):

    
    def __init__(self, base_dir, base_folder_name = 'liq'):
        self.src = Folder(
            path = os.path.join(base_dir, base_folder_name, 'files', 'src')
        )
        self.hashed = Folder(
            path = os.path.join(base_dir, base_folder_name, 'files', 'hashed')
        )
        self.bak = Folder(
            path = os.path.join(base_dir, base_folder_name, 'files', '.bak')
        )
        self.file_map = File(
            path = os.path.join(base_dir, base_folder_name, 'files', 'fileMap.json'),
            init = r"{}"
        )
        self.selector_map = File(
            path = os.path.join(base_dir, base_folder_name, 'files', 'selectorMap.json'),
            init = r"{}"
        )
        self.settings = File(
            path = os.path.join(base_dir, base_folder_name, 'settings.json'),
            init = json.dumps(r"{}")
        )
        
    


class Folder(object):

    def __init__(self, path):
        self.path = path


class File(object):
    
    def __init__(self, path, init):
        self.path = path
        self.init = init 

    def read(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def write(self, dict_):
        with open(self.path, 'w') as file:
            json.dump(dict_, file)


if __name__ == '__main__':
    structure = Structure(os.getcwd())