from Servizi.Prenotabile import Prenotabile
from Servizi.Assegnabile import Assegnabile
from GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from Utilities.PeriodoConData import PeriodoConData

class Camera(Prenotabile, Assegnabile):

    def __init__(self, numero : int, numeroPersone : int):
        self._numero  = numero
        self._numeroPersone = numeroPersone
        self._prenotazioni = []
        self._vacanzaAttuale = None

    def getNumero(self) -> int:
        return self._numero

    def getNumeroPersone(self) -> int:
        return self._numeroPersone

    def setNumero(self, numero : int):
        self._numero = numero

    def setNumeroPersone(self, numeroPersone : int):
        self._numeroPersone = numeroPersone
    
    def eliminaPrenotazione(self, prenotazione : PrenotazioneVacanza):
        self._prenotazioni.remove(prenotazione)
    
    def prenota(self, datiPrenotazione : dict):
        pass
    
    def assegna(self, datiAssegnamento : dict):
        pass

    def terminaAssegnamento(self):
        pass
    
    def isDisponibile(self, periodo : PeriodoConData):
        pass
