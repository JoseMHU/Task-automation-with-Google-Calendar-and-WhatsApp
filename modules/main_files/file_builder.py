import os
import pickle
import json
from datetime import datetime
import pandas as pd

class File:
    def __init__(self, path: str):
        self._path = path
        self.file = {}
        self.found = True

    def add_item(self, data: dict):
        for key in data:
            self.file[key] = data[key]
        with open(self._path, "wb") as file:
            pickle.dump(self.file, file)

    def delete_item(self, key):
        try:
            self.file.pop(key)
            with open(self._path, "wb") as file:
                pickle.dump(self.file, file)
        except KeyError:
            print("Valor no encontrado")


class PKLFile(File):
    def __init__(self, path: str):
        File.__init__(self, path)
        if os.path.exists(self._path):
            with open(self._path, "rb") as file:
                self.file = pickle.load(file)
        else:
            self.found = False
            with open(self._path, "wb") as file:
                pickle.dump(self.file, file)


class PKLFileDF(PKLFile):
    def __init__(self, path: str):
        PKLFile.__init__(self, path)
        self.file = pd.DataFrame(self.file)

class JsonFile(File):
    def __init__(self, path="modules/settings/config.json"):
        File.__init__(self, path)
        if os.path.exists(self._path):
            with open(self._path, "r") as file:
                self.file = json.load(file)
        else:
            self.found = False
            month = datetime.now().month
            with open("modules/settings/file_path.txt", "r") as file:
                path_txt = file.readline().rstrip()
                sheet_name = file.readline()
            self.file = {
                'path': path_txt,
                'sheet_name': sheet_name,
                'last_modified': os.path.getmtime(path_txt),
                'month': month
            }
            with open(self._path, "w") as file:
                json.dump(self.file, file, indent=4)

    def delete_item(self, key):
        pass

    def add_item(self, data: dict):
        pass

    def save(self):
        with open(self._path, "w") as file:
            json.dump(self.file, file, indent=4)


config_json = JsonFile()
