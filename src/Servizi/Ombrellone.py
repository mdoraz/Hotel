from pathlib import Path
from src.Servizi.Assegnabile import Assegnabile
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.exceptions import CorruptedFileError

class Ombrellone(Assegnabile):
    
    def __init__(self, numero : int):
        super().__init__()
        self._numero = numero

    def getNumero(self) -> int:
        return self._numero

    def setNumero(self, numero : int):
        self._numero = numero
    
    def assegna(self, datiAssegnamento : dict):
        self._assegnato = True
        # salvo la variazione
        paths = GestoreFile.leggiJson(Path('paths.json'))
        ombrelloni = GestoreFile.leggiDictPickle(Path(paths['ombrelloni']))
        ombrelloni[self._numero] = self
        GestoreFile.salvaPickle(ombrelloni, Path(paths['ombrelloni']))

    def terminaAssegnamento(self):
        self._assegnato = False
        # salvo la variazione
        paths = GestoreFile.leggiJson(Path('paths.json'))
        ombrelloni = GestoreFile.leggiDictPickle(Path(paths['ombrelloni']))
        
        if not isinstance(ombrelloni, dict): # se il file ha cambiato contenuto dal momento in cui è stato letto questo ombrellone ad ora
            raise CorruptedFileError(f'{Path(paths["ombrelloni"]).name} has been corrupted. To fix the issue, delete it.')
        
        ombrelloni[self._numero] = self
        GestoreFile.salvaPickle(ombrelloni, Path(paths['ombrelloni']))

    def __str__(self):
        return f'ombrellone {self._numero}'
