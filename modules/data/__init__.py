#L'ensemble des données partagées avec le reste du projet, accesible depuis l'ensemble des fichiers.
#Les trucs importants quoi
#config.json

import json

class Obj(dict):
    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            value = Obj(value)
        return value

with open("config.json") as file:
    raw = file.read()

data = Obj(json.loads(raw))