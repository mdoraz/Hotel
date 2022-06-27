from datetime import date
from pathlib import Path
from Attori.Dipendente import Dipendente
from Attori.Ruolo import Ruolo
from Gestori.GestoreFile import GestoreFile
from Utilities.exeptions import DuplicateError


class GestoreDipendente:

    pathFileDipendenti = Path('files/pickles/dipendenti.pickle')
    
    @staticmethod
    def _verificaEsistenzaDipendente(nome : str, cognome : str, dataNascita : date, luogoNascita : str) -> bool:
        
        try:
            dipendenti = GestoreFile.leggiPickle(GestoreDipendente.pathFileDipendenti)
        except FileNotFoundError:
            dipendenti = {}
        
        if not isinstance(dipendenti, dict):
            raise TypeError(f"{GestoreDipendente.pathFileDipendenti.name} has been corrupted.")
        
        flag = False
        for dipendente in dipendenti.values():
            if (dipendente.getNome() == nome and dipendente.getCognome() == cognome and 
                dipendente.getDataNascita() == dataNascita and dipendente.getLuogoNascita() == luogoNascita):
                flag = True
        
        return flag


    @staticmethod
    def aggiungiDipendente(nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str,
                           IBAN : str, turno : bool, ruolo : Ruolo, username : str, password : str):
        
        if GestoreDipendente._verificaEsistenzaDipendente(nome, cognome, dataNascita, luogoNascita):
            raise DuplicateError('This object is already saved in the system, try to search it.')

        nuovoDipendente = Dipendente(nome, cognome, dataNascita, luogoNascita, email, cellulare, IBAN, turno , ruolo, username, password)
        
        try:
            dipendenti = GestoreFile.leggiPickle(GestoreDipendente.pathFileDipendenti)
        except FileNotFoundError:
            dipendenti = {}
        
        if not isinstance(dipendenti, dict):
            raise TypeError(f"{GestoreDipendente.pathFileDipendenti.name} has been corrupted.")
        
        dipendenti[nuovoDipendente.getId()] = nuovoDipendente
        GestoreFile.salvaPickle(dipendenti, GestoreDipendente.pathFileDipendenti)


    @staticmethod
    def eliminaDipendente(dipendente : Dipendente):
        
        dipendenti = GestoreFile.leggiPickle(GestoreDipendente.pathFileDipendenti)
        if not isinstance(dipendenti, dict):
            raise TypeError(f"{GestoreDipendente.pathFileDipendenti.name} has been corrupted.")
        
        del dipendenti[dipendente.getId()]
        GestoreFile.salvaPickle(dipendenti, GestoreDipendente.pathFileDipendenti)
