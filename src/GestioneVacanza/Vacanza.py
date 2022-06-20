from Servizi.Ombrellone import Ombrellone
from Servizi.Camera import Camera
from GestioneVacanza.NoleggioBici import NoleggioBici
from GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from datetime import date

class Vacanza(PrenotazioneVacanza):

    def __init__(self, prenotazione : PrenotazioneVacanza, altriClienti : list, ombrellone : Ombrellone):
        super().__init__(prenotazione.getPeriodo(), prenotazione.getCamera(), prenotazione.getTipoSoggiorno(),
                         prenotazione.getNominativo(), prenotazione.getNumeroCarta())
        self._clienti = altriClienti
        self._clienti.append(prenotazione.getNominativo())
        self._ombrellone = ombrellone
        self._inCorso = True
        self._noleggiBici = []
        self._prenotazioniBici = []
        self._colazioniInCamera = {}
        self._sceltePasti = {}

    def aggiungiColazioneInCamera(self, preferenzeDelCliente : dict):
        pass

    def aggiungiNoleggioBici(self, noleggio : NoleggioBici):
        pass

    def aggiungiPrenotazioneBici(self, prenotazioneNoleggio : NoleggioBici):
        pass

    def aggiungiSceltaPasti(self, data : date, sceltaPasti : dict):
        pass

    def getClienti(self) -> list:
        pass

    def getColazioniInCamera(self) -> dict:
        pass

    def getNoleggiBici(self) -> list:
        pass

    def getOmbrellone(self) -> Ombrellone:
        pass

    def getPrenotazioniBici(self) -> list:
        pass

    def getSceltePasti(self) -> dict:
        pass

    def isInCorso(self) -> bool:
        pass

    def rimuoviPrenotazioneBici(self, prenotazioneNoleggio : NoleggioBici):
        pass

    def setInCorso(self, inCorso : bool):
        pass

    def setOmbrellone(self, ombrellone : Ombrellone):
        pass