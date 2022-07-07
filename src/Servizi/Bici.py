from datetime import datetime
from src.Servizi.Prenotabile import Prenotabile
from src.Servizi.Assegnabile import Assegnabile
from src.GestioneVacanza.NoleggioBici import NoleggioBici

class Bici(Prenotabile, Assegnabile):
    
    def __init__(self, numero : int, tipo : bool):
        self._numero = numero
        self._tipo = tipo
        self._orariPrenotati = []

    def getNumero(self) -> int:
        return self._numero

    def getTipo(self) -> bool:
        return self._tipo

    def setNumero(self, numero : int):
        self._numero = numero

    def setTipo(self, tipo : bool):
        self._tipo = tipo

    def aggiungiOrarioPrenotazione(self, orario : datetime):
        self._orariPrenotati.append(orario)
    
    def rimuoviOrarioPrenotazione(self, orario : datetime):
        self._orariPrenotati.remove(orario)
    
    def prenota(self, datiPrenotazione : dict):
        pass
    
    def assegna(self, datiAssegnamento : dict):
        pass
    
    def _assegnaConPrenotazione(self, prenotazione : NoleggioBici):
        pass

    def _assegnaSenzaPrenotazione(self):
        pass

    def terminaAssegnamento(self):
        pass
    
    def _terminaNoleggioInCorso(self):
        pass

    def isDisponibile(self, orario : datetime):
        pass
