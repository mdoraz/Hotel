import unittest
from pathlib import Path
from datetime import date
from src.Attori.Dipendente import Dipendente
from src.Attori.Persona import Persona

from src.Attori.Ruolo import Ruolo
from src.Gestori.GestoreFile import GestoreFile
from src.Gestori.GestorePersona import GestorePersona
from src.Utilities.exceptions import DuplicateError


class TestGestorePersona(unittest.TestCase):

	def setUp(self):
		global paths
		paths = GestoreFile.leggiJson(Path('paths.json'))

		GestorePersona.aggiungiPersona(Path(paths['clienti']),   # aggiunto un cliente nel file di clienti
									   'Rodrigo', 'Carlino', date(2001, 1, 1), 'Siviglia', 'rocarl@bu.com', '13342112')
		self.clienti : dict[int, Persona] = GestoreFile.leggiDictPickle(Path(paths['clienti']))

		datiDipendente = {
			'IBAN' : '3203484020384020',
			'turno' : True,
			'ruolo' : Ruolo.CAMERIERE,
			'username' : 'amicarl',
			'password' : '123456'
		}
		GestorePersona.aggiungiPersona(Path(paths['dipendenti']),   # aggiunto un dipendente nel file di dipendenti
									   'Amilcare', 'Carlino', date(2000, 10, 10), 'Siviglia', 'amicarl@bu.com', '2444224150', **datiDipendente)
		self.dipendenti : dict[int, Dipendente] = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))


	def tearDown(self):
		cliente1 = None
		for cliente in self.clienti.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				cliente1 = cliente
		try:
			GestorePersona.rimuoviPersona(Path(paths['clienti']), cliente1) # type: ignore
		except KeyError: # per i tearDown effettuati dopo testRimozioneCliente
			pass
		
		dipendente1 = None
		for dipendente in self.dipendenti.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				dipendente1 = dipendente
		try:
			GestorePersona.rimuoviPersona(Path(paths['dipendenti']), dipendente1) # type: ignore
		except KeyError: # per i tearDown effettuati dopo testRimozioneDipendente
			pass


	def testDuplicati(self):
		self.assertRaises(DuplicateError, GestorePersona.aggiungiPersona, 
										Path(paths['clienti']), 'Rodrigo', 'Carlino', date(2001, 1, 1), 'Siviglia', 'rocarl@bu.com', '13342112')
		
		self.assertRaises(DuplicateError, GestorePersona.aggiungiPersona, 
										Path(paths['dipendenti']), 'Amilcare', 'Carlino', date(2000, 10, 10), 'Siviglia', 'amicarl@bu.com', '2444224150')


	def testRimozioneCliente(self):
		cliente1 = None
		for cliente in self.clienti.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				cliente1 = cliente
		self.assertIsNotNone(cliente1) # è stato trovato nel sistema il cliente inserito nel setUp
		
		# elimino dal sistema il cliente inserito nel setUp
		GestorePersona.rimuoviPersona(Path(paths['clienti']), cliente1) # type: ignore

		trovato = False
		clientiAggiornati = GestoreFile.leggiDictPickle(Path(paths['clienti']))
		for cliente in clientiAggiornati.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				trovato = True
		self.assertFalse(trovato) # non è stato trovato nel sistema il cliente inserito nel setUp
	

	def testRimozioneDipendente(self):
		dipendente1 = None
		for dipendente in self.dipendenti.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				dipendente1 = dipendente
		self.assertIsNotNone(dipendente1) # è stato trovato nel sistema il dipendente inserito nel setUp
		
		# elimino dal sistema il dipendente inserito nel setUp
		GestorePersona.rimuoviPersona(Path(paths['dipendenti']), dipendente1) # type: ignore

		trovato = False
		dipendentiAggiornati = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		for dipendente in dipendentiAggiornati.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				trovato = True
		self.assertFalse(trovato) # non è stato trovato nel sistema il dipendente inserito nel setUp



if __name__ == '__main__':
	unittest.main()
