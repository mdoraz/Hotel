from Servizi.Assegnabile import Assegnabile

class Ombrellone(Assegnabile):
    
    def __init__(self, numero : int):
        self._numero = numero

    def getNumero(self) -> int:
        return self._numero

    def setNumero(self, numero : int):
        self._numero = numero
    
    def assegna(self, datiAssegnamento : dict):
        pass

    def terminaAssegnamento(self):
        pass