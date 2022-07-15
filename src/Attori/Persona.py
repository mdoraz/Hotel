from __future__ import annotations
from datetime import date
from pathlib import Path

from src.Attori.Contattabile import Contattabile
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.exceptions import CreationError


class Persona(Contattabile):

    def __init__(self, nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str, **kwargs):
        super().__init__(email, cellulare, **kwargs)
        try:
            self._id = Persona._calcolaId()
        except TypeError as e:
            raise CreationError(f"{str(e)} Cannot generate a valid id for this Persona object.")
        self._nome = nome
        self._cognome = cognome
        self._dataNascita = dataNascita
        self._luogoNascita = luogoNascita

    def getNome(self) -> str:
        return self._nome

    def getCognome(self) -> str:
        return self._cognome

    def getDataNascita(self) -> date:
        return self._dataNascita

    def getLuogoNascita(self) -> str:
        return self._luogoNascita

    def getId(self) -> int:
        return self._id

    def setNome(self, nome : str):
        self._nome = nome

    def setCognome(self, cognome : str):
        self._cognome = cognome

    def setDataNascita(self, dataNascita : date):
        self._dataNascita = dataNascita

    def setLuogoNascita(self, luogoNascita : str):
        self._luogoNascita = luogoNascita
    

    def setId(self, id : int):
        self._id = id


    @staticmethod
    def _calcolaId() -> int:

        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            clienti = GestoreFile.leggiPickle(Path(paths['clienti']))
        except FileNotFoundError:
            return 1
        
        if not isinstance(clienti, dict):
            raise TypeError(f"{Path(paths['clienti']).name} has been corrupted.")
        
        ultimoId = 0
        for cliente in clienti.values():
            if cliente.getId() > ultimoId:
                ultimoId = cliente.getId()
        
        return ultimoId + 1

    
    def isTheSame(self, other : Persona):
        return (self._nome == other.getNome() and self._cognome == other.getCognome() and 
                self._dataNascita == other.getDataNascita() and self._luogoNascita == other.getLuogoNascita())


    def __str__(self):
        return f"ID: {self._id} - {self._nome} {self._cognome}, nato il {self._dataNascita} a {self._luogoNascita}"