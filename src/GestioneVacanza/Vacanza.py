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
        self._prenotazioniBici = []
        self._noleggiBici = []
        self._colazioniInCamera = {}
        self._sceltePasti = {}

    def aggiungiPrenotazioneBici(self, prenotazioneNoleggio : NoleggioBici):
        i = 0
        while i < len(self._prenotazioniBici) and prenotazioneNoleggio.getOrario() > self._prenotazioniBici[i]:
            i += 1
        self._prenotazioniBici.insert(i, prenotazioneNoleggio)

    def rimuoviPrenotazioneBici(self, prenotazioneNoleggio : NoleggioBici):
        self._prenotazioniBici.remove(prenotazioneNoleggio)

    def aggiungiNoleggioBici(self, noleggio : NoleggioBici):
        self._noleggiBici.append(noleggio)

    def impostaColazioneInCamera(self, data: date, preferenzeDelCliente : dict):
        self._colazioniInCamera[data] = preferenzeDelCliente

    def impostaSceltaPasti(self, data : date, sceltaPasti : dict): # impostaSceltaPasti
        self._sceltePasti[data] = sceltaPasti

    def getClienti(self) -> list:
        return self._clienti

    def getOmbrellone(self) -> Ombrellone:
        return self._ombrellone

    def getPrenotazioniBici(self) -> list:
        return self._prenotazioniBici

    def getNoleggiBici(self) -> list:
        return self._noleggiBici

    def getColazioniInCamera(self) -> dict:
        return self._colazioniInCamera

    def getSceltePasti(self) -> dict:
        return self._sceltePasti

    def isInCorso(self) -> bool:
        return self._inCorso

    def setInCorso(self, inCorso : bool):
        self._inCorso = inCorso

    def setOmbrellone(self, ombrellone : Ombrellone):
        self._ombrellone = ombrellone
