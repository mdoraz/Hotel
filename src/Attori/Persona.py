from Attori.Contattabile import Contattabile
from datetime import date


class Persona(Contattabile):

    def __init__(self, nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str, **kwargs):
        super().__init__(email, cellulare, **kwargs)
        self._id = Persona._calcolaUltimoId()
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

    @staticmethod
    def _calcolaUltimoId() -> int:
        pass