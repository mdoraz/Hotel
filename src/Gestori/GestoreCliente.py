from datetime import date
from pathlib import Path
from Attori.Persona import Persona
from Gestori.GestoreFile import GestoreFile
from Utilities.exeptions import DuplicateError


class GestoreCliente:

    pathFileClienti = Path('files/pickles/clienti.pickle')

    @staticmethod
    def _verficaEsistenzaCliente(nome : str, cognome : str, dataNascita : date, luogoNascita : str) -> bool:
        
        try:
            clienti = GestoreFile.leggiPickle(GestoreCliente.pathFileClienti)
        except FileNotFoundError:
            clienti = {}
        
        if not isinstance(clienti, dict):
            raise TypeError(f"{GestoreCliente.pathFileClienti.name} has been corrupted.")
        
        flag = False
        for cliente in clienti.values():
            if (cliente.getNome() == nome and cliente.getCognome() == cognome and 
                cliente.getDataNascita() == dataNascita and cliente.getLuogoNascita() == luogoNascita):
                flag = True
        
        return flag

    @staticmethod
    def aggiungiCliente(nome : str, cognome : str, dataNascita : date, luogoNascita : str, email : str, cellulare : str):
        
        if GestoreCliente._verficaEsistenzaCliente(nome, cognome, dataNascita, luogoNascita):
            raise DuplicateError('This object is already in the system, try to search it.')
        
        nuovoCliente = Persona(nome, cognome, dataNascita, luogoNascita, email, cellulare)
        
        try:
            clienti = GestoreFile.leggiPickle(GestoreCliente.pathFileClienti)
        except FileNotFoundError:
            clienti = {}
        
        if not isinstance(clienti, dict):
            raise TypeError(f"{GestoreCliente.pathFileClienti.name} has been corrupted.")
        
        clienti[nuovoCliente.getId()] = nuovoCliente
        GestoreFile.salvaPickle(clienti, GestoreCliente.pathFileClienti)

    @staticmethod
    def eliminaCliente(cliente : Persona):
        
        clienti = GestoreFile.leggiPickle(GestoreCliente.pathFileClienti)
        if not isinstance(clienti, dict):
            raise TypeError(f"{GestoreCliente.pathFileClienti.name} has been corrupted.")
        
        del clienti[cliente.getId()]
        GestoreFile.salvaPickle(clienti, GestoreCliente.pathFileClienti)