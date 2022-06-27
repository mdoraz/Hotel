from pathlib import Path
from datetime import date
import unittest
from Attori.Ruolo import Ruolo
from Gestori.GestoreFile import GestoreFile
from Gestori.GestorePersona import GestorePersona
from Utilities.exeptions import DuplicateError


class TestGestorePersona(unittest.TestCase):

	def setUp(self):
		GestorePersona.aggiungiPersona(Path('files/clienti.pickle'), 'Rodrigo', 'Carlino', date(2001, 1, 1), 
									   'Siviglia', 'rocarl@bu.com', '13342112')
		self.clienti = GestoreFile.leggiPickle(Path('files/clienti.pickle'))
		
		datiAmilcare = {'IBAN' : '3203484020384020', 'turno' : True, 'ruolo' : Ruolo.CAMERIERE,
						'username' : 'amicarl', 'password' : '123456'}
		GestorePersona.aggiungiPersona(Path('files/dipendenti.pickle'), 'Amilcare', 'Carlino', date(2000, 10, 10), 
									   'Siviglia', 'amicarl@bu.com', '2444224150', **datiAmilcare)
		self.dipendenti = GestoreFile.leggiPickle(Path('files/dipendenti.pickle'))


	def tearDown(self):
		cliente1 = None
		for cliente in self.clienti.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				cliente1 = cliente
		try:
			GestorePersona.rimuoviPersona(Path('files/clienti.pickle'), cliente1)
		except KeyError: # per i tearDown effettuati dopo testRimozioneCliente
			pass
		
		dipendente1 = None
		for dipendente in self.dipendenti.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				dipendente1 = dipendente
		try:
			GestorePersona.rimuoviPersona(Path('files/dipendenti.pickle'), dipendente1)
		except KeyError: # per i tearDown effettuati dopo testRimozioneDipendente
			pass


	def testCliente1(self):
		cliente1 = None
		for cliente in self.clienti.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				cliente1 = cliente
		self.assertEqual(str(cliente1), f"ID: {cliente1.getId()} - Rodrigo Carlino, nato il 2001-01-01 a Siviglia")


	def testDipendente1(self):
		dipendente1 = None
		for dipendente in self.dipendenti.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				dipendente1 = dipendente
		self.assertEqual(str(dipendente1), f"ID: {dipendente1.getId()} - Amilcare Carlino, nato il 2000-10-10 a Siviglia --> CAMERIERE")


	def testDuplicati(self):
		self.assertRaises(DuplicateError, GestorePersona.aggiungiPersona, Path('files/clienti.pickle'),
										  'Rodrigo', 'Carlino', date(2001, 1, 1), 'Siviglia', 'rocarl@bu.com', '13342112')
		
		self.assertRaises(DuplicateError, GestorePersona.aggiungiPersona, Path('files/dipendenti.pickle'),
										  'Amilcare', 'Carlino', date(2000, 10, 10), 'Siviglia', 'amicarl@bu.com', '2444224150')


	def testRimozioneCliente(self):
		cliente1 = None
		for cliente in self.clienti.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				cliente1 = cliente
		self.assertNotEqual(cliente1, None) # è stato trovato nel sistema il cliente inserito nel setUp
		
		GestorePersona.rimuoviPersona(Path('files/clienti.pickle'), cliente1) # elimino dal sistema il cliente inserito nel setUp

		flag = False
		clientiAggiornati = GestoreFile.leggiPickle(Path("files/clienti.pickle"))
		for cliente in clientiAggiornati.values():
			if cliente.getNome() == 'Rodrigo' and cliente.getCognome() == 'Carlino' and cliente.getDataNascita() == date(2001, 1, 1):
				flag = True
		self.assertEqual(flag, False) # non è stato trovato nel sistema il cliente inserito nel setUp
	

	def testRimozioneDipendente(self):
		dipendente1 = None
		for dipendente in self.dipendenti.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				dipendente1 = dipendente
		self.assertNotEqual(dipendente1, None) # è stato trovato nel sistema il dipendente inserito nel setUp
		
		GestorePersona.rimuoviPersona(Path('files/dipendenti.pickle'), dipendente1) # elimino dal sistema il dipendente inserito nel setUp

		flag = False
		dipendentiAggiornati = GestoreFile.leggiPickle(Path("files/dipendenti.pickle"))
		for dipendente in dipendentiAggiornati.values():
			if dipendente.getNome() == 'Amilcare' and dipendente.getCognome() == 'Carlino' and dipendente.getDataNascita() == date(2000, 10, 10):
				flag = True
		self.assertEqual(flag, False) # non è stato trovato nel sistema il dipendente inserito nel setUp


if __name__ == '__main__':
	unittest.main()
