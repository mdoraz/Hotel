import pickle
from pathlib import Path

class GestoreFile:

    @staticmethod
    def backup():
        pass

    @staticmethod
    def leggiDaFile(pathFile : Path) -> object:
        with open(pathFile, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def salvaSuFile(oggetto : object, pathFile : Path):
        
        if not pathFile.exists():
            with open(pathFile, 'w') as file:
                pass
        with open(pathFile, 'wb') as file:
            pickle.dump(oggetto, file, pickle.HIGHEST_PROTOCOL)
