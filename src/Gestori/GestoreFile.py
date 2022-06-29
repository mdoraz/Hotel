import json
import pickle
from pathlib import Path
import src.Attori

class GestoreFile:

    @staticmethod
    def backup():
        pass

    @staticmethod
    def leggiPickle(pathFile : Path) -> object:
        with open(pathFile, 'rb') as file:
            oggetto = pickle.load(file)
            return oggetto

    @staticmethod
    def salvaPickle(oggetto : object, pathFile : Path):
        
        if not pathFile.exists():
            with open(pathFile, 'w') as file:
                pass
        with open(pathFile, 'wb') as file:
            pickle.dump(oggetto, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def leggiJson(pathFile : Path) -> dict:
        with open(pathFile, 'r') as file:
            return json.load(file)
