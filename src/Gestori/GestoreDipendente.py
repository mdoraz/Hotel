import imp
from Attori.Dipendente import Dipendente
from Attori.Ruolo import Ruolo
from datetime import date


class GestoreDipendente:

    @staticmethod
    def _verificaEsistenzaDipendente(nome : str, congome : str, dataNascita : date, luogoNascita : str) -> bool:
        pass

    @staticmethod
    def aggiungiDipendente(nome : str, cognome : str, dataNascita : date, luogoNascita : str, 
                           email : str, cellulare : str, IBAN : str, turno : bool, ruolo : Ruolo):
        pass

    @staticmethod
    def eliminaDipendente(dipendente : Dipendente):
        pass