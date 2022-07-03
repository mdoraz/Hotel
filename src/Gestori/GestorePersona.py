from datetime import date
from pathlib import Path

from src.Attori.Dipendente import Dipendente
from src.Attori.Persona import Persona
from src.Attori.Ruolo import Ruolo
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.exeptions import CreationError, DuplicateError


class GestorePersona():

	@staticmethod
	def _verificaEsistenzaPersona(pathFile : Path, nome : str, cognome : str, dataNascita : date, luogoNascita : str):
		
		try:
			persone = GestoreFile.leggiDictPickle(pathFile)
		except TypeError:
			raise
		
		flag = False
		for persona in persone.values():
			if (persona.getNome() == nome and persona.getCognome() == cognome and 
                persona.getDataNascita() == dataNascita and persona.getLuogoNascita() == luogoNascita):
				flag = True
        
		return flag


	@staticmethod
	def aggiungiPersona(pathFile : Path, nome : str, cognome : str, dataNascita : date, luogoNascita : str,
						email : str, cellulare : str, **kwargs):
		"""Adds in the system a Persona object. If you want to add an object of a Persona subclass, you have to use kwargs
		to pass the extra parameters requested by the subclass constructor."""
		
		if GestorePersona._verificaEsistenzaPersona(pathFile, nome, cognome, dataNascita, luogoNascita):
			raise DuplicateError('this object is already in the system.')
		
		nuovaPersona = Persona(nome, cognome, dataNascita, luogoNascita, email, cellulare)

		if pathFile.name == 'dipendenti.pickle': # se il file è quello dei dipendenti, nuovaPersona deve essere della classe Dipendente
			try:
				if (isinstance(kwargs['IBAN'], str) and isinstance(kwargs['turno'], bool) and isinstance(kwargs['ruolo'], Ruolo) and
					isinstance(kwargs['username'], str) and isinstance(kwargs['password'], str)):
					
					nuovaPersona = Dipendente.initConPersona(nuovaPersona, kwargs['IBAN'], kwargs['turno'], kwargs['ruolo'],
													 		 kwargs['username'], kwargs['password'])
				else:
					raise TypeError("some argument hasn't the right type to create a Dipendente object")
			except KeyError: # se qualche chiave nell'if precedente non è contenuta in kwargs
				raise CreationError('the arguments are not the right ones to create a Dipendente object')
		try:
			persone = GestoreFile.leggiDictPickle(pathFile)
		except TypeError:
			raise
			
		persone[nuovaPersona.getId()] = nuovaPersona
		GestoreFile.salvaPickle(persone, pathFile)


	@staticmethod
	def rimuoviPersona(pathFile : Path, persona : Persona):
		try:
			persone = GestoreFile.leggiDictPickle(pathFile)
		except TypeError:
			raise
		
		del persone[persona.getId()]

		GestoreFile.salvaPickle(persone, pathFile)