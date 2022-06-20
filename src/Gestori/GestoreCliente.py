from Attori.Persona import Persona
from datetime import date


class GestoreCliente:

    @staticmethod
    def _verficaEsistenzaCliente(nome : str, cognome : str, dataNascita : date, luogoNascita : str) -> bool:
        pass

    @staticmethod
    def aggiungiCliente(nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str):
        pass

    @staticmethod
    def eliminaCliente(cliente : Persona):
        pass