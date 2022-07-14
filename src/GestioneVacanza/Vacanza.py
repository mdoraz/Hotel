from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date

from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
if TYPE_CHECKING: # true solo durante il tipe checking, legato ai type hints
    from src.Attori.Persona import Persona
    from src.Servizi.Ombrellone import Ombrellone
    from src.GestioneVacanza.NoleggioBici import NoleggioBici

class Vacanza(PrenotazioneVacanza):

    def __init__(self, prenotazione : PrenotazioneVacanza, clienti : list[Persona], ombrellone : Ombrellone):
        super().__init__(prenotazione.getPeriodo(), prenotazione.getCamera(), prenotazione.getTipoSoggiorno(),
                         prenotazione.getNominativo(), prenotazione.getNumeroCarta())
        self._clienti = clienti
        self._ombrellone = ombrellone
        self._prenotazioniBici = []
        self._noleggiBici = []
        self._colazioniInCamera = {}
        self._sceltePastiPranzo = {}
        self._sceltePastiCena = {}
        self._inCorso = True

    def aggiungiPrenotazioneBici(self, prenotazioneNoleggio : NoleggioBici):# inserimento ordinato ella prenotazione
        i = 0
        while i < len(self._prenotazioniBici) and prenotazioneNoleggio.getOrario() > self._prenotazioniBici[i].getOrario():
            i += 1
        self._prenotazioniBici.insert(i, prenotazioneNoleggio)

    def rimuoviPrenotazioneBici(self, prenotazioneNoleggio : NoleggioBici):
        self._prenotazioniBici.remove(prenotazioneNoleggio)

    def aggiungiNoleggioBici(self, noleggio : NoleggioBici):
        self._noleggiBici.append(noleggio)

    def setColazioniInCamera(self,preferenzeDelCliente : dict):
        self._colazioniInCamera = preferenzeDelCliente

    def setSceltePastiPranzo(self, sceltePasti : dict):
        self._sceltePasti = sceltePasti

    def setSceltePastiCena(self, sceltePasti: dict):
        self._sceltePasti = sceltePasti

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

    def getSceltePastiPranzo(self) -> dict:
        return self._sceltePastiPranzo

    def getSceltePastiCena(self) -> dict:
        return self._sceltePastiCena

    def isInCorso(self) -> bool:
        return self._inCorso

    def setInCorso(self, inCorso : bool):
        self._inCorso = inCorso

    def setOmbrellone(self, ombrellone : Ombrellone):
        self._ombrellone = ombrellone
