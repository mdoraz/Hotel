import json
import pickle
from pathlib import Path

from src.Utilities.exceptions import CorruptedFileError

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
        
        if not pathFile.exists(): # se il file non esiste (ma il percorso fino alla cartella in cui si trova esiste)
            with open(pathFile, 'x') as file: # il file viene creato
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
            if not isinstance(dictionary, dict):
                raise CorruptedFileError(f"{pathFile.name} has been corrupted and can't be restored.\nTo fix the issue, delete it.")
        except FileNotFoundError:
            dictionary = {}
        
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

    
    @staticmethod
    def absolutePath(fileName : str, directory : Path) -> str:  # type: ignore
        """Searches fileName in the given directory. If the file is found, its absolute path is returned, else an empty string."""
        if not directory.is_dir():
            return ''
        for path in directory.iterdir():
            if path.is_file() and path.name == fileName:
                return str(path.resolve())
            elif path.is_dir():
                absolutePath = GestoreFile.absolutePath(fileName, path) # se path è una directory applico ricorsivamente la funzione
                if absolutePath != '': # se è stato trovato il file nella directory 'path'
                    return absolutePath
        return '' # se non entro in nessun if che contiene return, quindi se non ho trovato nessun file che corrisponde a fileName in directory

