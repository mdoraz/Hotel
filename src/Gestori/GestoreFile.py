import json
import pickle
from pathlib import Path

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

    @staticmethod
    def leggiDictPickle(pathFile : Path) -> dict:
        try:
            dictionary = GestoreFile.leggiPickle(pathFile)
        except FileNotFoundError:
            dictionary = {}
        
        if not isinstance(dictionary, dict):
            raise TypeError(f"{pathFile.name} has been corrupted and can't be restored.\nTo fix the issue, delete it.")
        return dictionary
    
    @staticmethod
    def leggiListPickle(pathFile : Path) -> list:
        try:
            mylist = GestoreFile.leggiPickle(pathFile)
        except FileNotFoundError:
            mylist = {}
        
        if not isinstance(mylist, list):
            raise TypeError(f"{pathFile.name} has been corrupted and can't be restored.\nTo fix the issue, delete it.")
        return mylist
