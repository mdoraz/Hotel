from __future__ import annotations
from Attori.Utente import Utente
from Attori.Persona import Persona
from Attori.Ruolo import Ruolo
from datetime import date

class Dipendente(Persona, Utente):

    def __init__(self, nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str,
                 IBAN : str, turno : bool, ruolo : Ruolo, username : str, password : str):
        
        credenziali = {'username': username, 'password': password}
        super().__init__(nome, cognome, dataNascita, luogoNascita, email, cellulare, **credenziali)
        self._id = Dipendente._calcolaUltimoId()
        self._IBAN = IBAN
        self._turno = turno
        self._ruolo = ruolo
        self._assenze = []
        
        STIPENDIO_RECEPTIONIST = 1200
        STIPENDIO_CAMERIERE = 1000
        if self._ruolo.name == Ruolo.RECEPTIONIST:
            self._stipendio = STIPENDIO_RECEPTIONIST
        else:
            self._stipendio = STIPENDIO_CAMERIERE

   
    @staticmethod
    def initConPersona(persona : Persona, IBAN : str, turno : bool, ruolo : Ruolo, username : str, password : str) -> Dipendente:
        
        return Dipendente(persona.getNome(), persona.getCognome(), persona.getDataNascita(), persona.getLuogoNascita(), 
                         persona.getEmail(), persona.getCellulare(), IBAN, turno, ruolo, username, password)

    def getAssenze(self) -> list:
        return self._assenze

    def getAutorizzazione(self) -> Ruolo:
        return self._ruolo

    def getIBAN(self) -> str:
        return self._IBAN

    def getStipendio(self) -> int:
        return self._stipendio

    def getTurno(self) -> bool:
        return self._turno
    
    def aggiungiAssenza(self, data : date):
        self._assenze.append(data)

    def rimuoviAssenza(self, data : date):
        self._assenze.remove(data)

    def setAutorizzazione(self, ruolo : Ruolo):
        self._ruolo = ruolo

    def setIBAN(self, IBAN : str):
        self._IBAN = IBAN

    def setStipendio(self, stipendio : int):
        self._stipendio = stipendio

    def setTurno(self, turno : bool):
        self._turno = turno

    @staticmethod
    def _calcolaUltimoId() -> int:
        pass