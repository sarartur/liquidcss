import os
import shutil
import json
from collections import OrderedDict

from liquidcss.settings import Settings
from liquidcss.utils import create_file_id, create_file_hash


class Structure(object):

    def __init__(self, base_dir, base_folder_name):
        self.base_folder_name = base_folder_name
        self.base_dir = base_dir

        self.base = Folder(
            path = os.path.join(base_dir, self.base_folder_name)
        )
        self.src = Folder(
            path = os.path.join(base_dir, self.base_folder_name, 'files', 'src')
        )
        self.hashed = Folder(
            path = os.path.join(base_dir, self.base_folder_name, 'files', 'hashed')
        )
        self.bak = Folder(
            path = os.path.join(base_dir, self.base_folder_name, 'files', '.bak')
        )
        self.file_map = File(
            path = os.path.join(base_dir, self.base_folder_name, 'fileMap.json'),
            default = r"{}"
        ) 
        self.selector_map = File(
            path = os.path.join(base_dir, self.base_folder_name, 'selectorMap.json'),
            default = r"{}"
        )
        self.settings = File(
            path = os.path.join(base_dir, self.base_folder_name, 'settings.json'),
            default = json.dumps(Settings.default)
        )
    
    @property
    def files(self):
        return tuple(
            value for value in self.__dict__.values() if isinstance(value, File)
        )

    @property
    def folders(self):
        return tuple(
            value for value in self.__dict__.values() if isinstance(value, Folder)
        )

class WorkSpace(Structure):

    def __init__(self, base_dir, base_folder_name = 'liq'):
        Structure.__init__(self, base_dir = base_dir, base_folder_name = base_folder_name)

    @property
    def files_deployed(self):
        file_map = self.file_map
        return tuple(
            mapping['id'] for mapping in file_map.content if mapping['deployed'] == True
        )

    def touch_base_folder(self):
        if os.path.isdir(self.base_folder_name):
            return True
        
    def init(self):
        for folder in self.folders:
            try: self._create_dirs(path = folder.path)
            except FileExistsError: pass
        for file in self.files:
            try: self._create_file(path = file.path, string = file.default)
            except FileExistsError: pass

    def reset(self):
        path = os.path.join(self.base_dir, self.base_folder_name)
        shutil.rmtree(path)
        self.init()
        
    def remove_files(self, paths):
        for path in paths:
            self._remove_file(path = path)

    def create_file(self, path, string):
        self._create_file(path = path, string = string)

    def validate(self):
        for file_or_folder in tuple(*self.files, *self.folders):
            if not file_or_folder.exists:
                return False
        return True

    def register(self, path, file_id):
        self._copy(src = path, trgt = os.path.join(self.src.path, os.path.basename(path)))
        _content = self.file_map.content
        _content.update({file_id : {
            "path": path, "staged": False, "deployed": False,
            "hash": create_file_hash(
                path = os.path.join(self.src.path, os.path.basename(path))
            )
        }})
        self.file_map.content = _content

    def _copy(self, src, trgt):
        shutil.copyfile(src, trgt)

    def _create_file(self, path, string):
        with open(path, 'w') as file:
            file.write(string)

    def _create_dirs(self, path):
        os.makedirs(path)
    
    def _remove_file(self, path):
        os.remove(path)

class Folder(object):

    def __init__(self, path):
        self.path = path

    @property
    def exists(self):
        return os.path.isdir(self.path)

class File(object):
    
    def __init__(self, path, default):
        self.path = path
        self.default = default

    @property
    def content(self):
        _content = self._read()
        return _content if _content else json.loads(self.default)

    @content.setter
    def content(self, dict_):
        self._write(dict_ = dict_)

    @property
    def existis(self):
        return os.path.isfile(self.path)

    def _read(self):
        if not self.existis:
            return None
        with open(self.path, 'r') as file:
            return json.load(file)

    def _write(self, dict_):
        with open(self.path, 'w') as file:
            json.dump(dict_, file)