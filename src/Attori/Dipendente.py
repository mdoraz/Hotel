from __future__ import annotations
from datetime import date
from pathlib import Path

from src.Attori.Utente import Utente
from src.Attori.Persona import Persona
from src.Attori.Ruolo import Ruolo
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.exeptions import CreationError


class Dipendente(Persona, Utente):

    def __init__(self, nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str,
                 IBAN : str, turno : bool, ruolo : Ruolo, username : str, password : str):

        credenziali = {'username': username, 'password': password}
        super().__init__(nome, cognome, dataNascita, luogoNascita, email, cellulare, **credenziali)
        try:
            self._id = Dipendente._calcolaId()
        except TypeError as e:
            raise CreationError(f"{str(e)} Cannot generate a valid id for this Dipendente object.")
        self._IBAN = IBAN
        self._turno = turno
        self._ruolo = ruolo
        self._assenze = []
        
        STIPENDIO_RECEPTIONIST = 1200
        STIPENDIO_CAMERIERE = 1000
        if self._ruolo == Ruolo.RECEPTIONIST:
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
    
    def aggiungiAssenza(self, data : date): # inserimento ordinato di "data" nella lista di date "self._assenze"
        dataInserita = False
        for i in range(0, len(self._assenze)):
            if data < self._assenze[i] and not dataInserita:
                self._assenze.insert(i, data)
                dataInserita = True
        if not dataInserita:
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
    def _calcolaId() -> int:
        
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            dipendenti = GestoreFile.leggiPickle(Path(paths['dipendenti']))
        except FileNotFoundError:
            return 1
        
        if not isinstance(dipendenti, dict):
            raise TypeError(f"{Path(paths['dipendenti']).name} has been corrupted.")
        
        ultimoId = 0
        for dipendente in dipendenti.values():
            if dipendente.getId() > ultimoId:
                ultimoId = dipendente.getId()
        
        return ultimoId + 1
    
    def __str__(self):
        return f"{super().__str__()} --> {self._ruolo.name}"
    