import unittest
from pathlib import Path
from datetime import date, datetime
from src.Attori.Persona import Persona
from src.GestioneVacanza.Soggiorno import Soggiorno

from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Bici import Bici
from src.Servizi.Camera import Camera
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import AssignmentError, NotAvailableError

class TestBici(unittest.TestCase):

	def setUp(self):
		self.paths = GestoreFile.leggiJson(Path('paths.json'))
		self.biciclette = GestoreFile.leggiDictPickle(Path(self.paths['bici']))
		ombrelloni = GestoreFile.leggiDictPickle(Path(self.paths['ombrelloni']))
		
		self.camere = GestoreFile.leggiDictPickle(Path(self.paths['camere']))	
		self.camera = self.camere[1]
		if not isinstance(self.camera, Camera):
			raise Exception
		
		# viene prenotata la camera
		datiPrenotazione = {
			'periodo' : PeriodoConData(date(2000, 7, 1), date(2000, 7, 7)),
			'tipoSoggiorno' : Soggiorno.MEZZA_PENSIONE,
			'nominativo' : Persona('Eustachio', 'Liguori', date(1980, 7, 6), 'Pistoia', 'eustoia@hotmail.com', '393204820'),
			'numeroCarta' : '193028018382001'
		}
		self.camera.prenota(datiPrenotazione)
		
		# viene assegnata la camera
		datiAssegnamento = {
			'prenotazione' : self.camera.getPrenotazioni()[0], # prenotazione appena aggiunta è in prima posizione (ordine di data)
			'clienti' : [datiPrenotazione['nominativo'], Persona('Rosanna', 'Camuzi', date(1981, 2, 3), 'Pistoia', 'rosacamu@hotmail.com', '3933949056')],
			'ombrellone' : ombrelloni[10]
		}
		self.camera.assegna(datiAssegnamento)


	def tearDown(self):
		if self.camere[1].isAssegnato():
			self.camere[1].terminaAssegnamento()


	def testAggiungiRimuoviPrenotazione(self):
		camera = self.camere[1]
		bici = self.biciclette[5]
		if not isinstance(bici, Bici) or not isinstance(camera, Camera):
			raise Exception

		nPrenotazioniIniziali = len(bici.getOrariPrenotati())
		nPrenotazioniNoleggi = len(camera.getVacanzaAttuale().getPrenotazioniBici()) # type: ignore

		datiPrenotazioneBici = {
			'camera' : camera,
			'orario' : datetime(1970, 1, 1, 10, 00)
		}
		bici.prenota(datiPrenotazioneBici)

		# verifica dell'avvenuta aggiunta dell'orario agli orari in cui la bici è prenotata e della prenotazione alla vacanza associata alla camera 
		self.assertEqual(nPrenotazioniIniziali + 1, len(bici.getOrariPrenotati()))
		self.assertEqual(nPrenotazioniNoleggi + 1, len(camera.getVacanzaAttuale().getPrenotazioniBici()))  # type: ignore

		# leggo da file e ricontrollo, per verificare il corretto salvataggio
		camere = GestoreFile.leggiDictPickle(Path(self.paths['camere']))
		biciclette = GestoreFile.leggiDictPickle(Path(self.paths['bici']))

		self.assertEqual(nPrenotazioniIniziali + 1, len(biciclette[5].getOrariPrenotati()))
		self.assertEqual(nPrenotazioniNoleggi + 1, len(camere[1].getVacanzaAttuale().getPrenotazioniBici()))  # type: ignore

		# disdico la prenotazione
		bici.rimuoviOrarioPrenotazione(datiPrenotazioneBici['orario'])
		camera.getVacanzaAttuale().rimuoviPrenotazioneBici(camera.getVacanzaAttuale().getPrenotazioniBici()[0]) # type: ignore
		
		self.assertEqual(nPrenotazioniIniziali, len(bici.getOrariPrenotati()))
		self.assertEqual(nPrenotazioniNoleggi, len(camera.getVacanzaAttuale().getPrenotazioniBici())) # type: ignore

		# salvo la disdetta
		biciclette[5] = bici
		camere[1] = camera
		GestoreFile.salvaPickle(biciclette, Path(self.paths['bici']))
		GestoreFile.salvaPickle(camere, Path(self.paths['camere']))

		# termino la vacanza per la camera
		camera.terminaAssegnamento()
		self.assertRaises(AssignmentError, bici.prenota, datiPrenotazioneBici) # la camera non è più assegnata dunque non può prenotare una bici


	def testDisponibilita(self):
		camera = self.camere[1]
		bici = self.biciclette[5]
		if not isinstance(bici, Bici) or not isinstance(camera, Camera):
			raise Exception
		
		datiPrenotazioneBici = {
			'camera' : camera,
			'orario' : datetime(1970, 1, 1, 10, 0) # prenoto alle 10:00
		}
		bici.prenota(datiPrenotazioneBici)

		datiPrenotazioneBici['orario'] = datetime(1970, 1, 1, 11, 59)
		self.assertRaises(NotAvailableError, bici.prenota, datiPrenotazioneBici) # fino a 2 ore dopo l'orario di una prenotazione, la bici non è prenotabile

		datiPrenotazioneBici['orario'] = datetime(1970, 1, 1, 12, 0)
		bici.prenota(datiPrenotazioneBici) # dalle 12:00 la bici è nuovamente prenotabile
		
		datiPrenotazioneBici['orario'] = datetime(1970, 1, 1, 8, 1)
		self.assertRaises(NotAvailableError, bici.prenota, datiPrenotazioneBici) # fino a 2 ore prima l'orario di una prenotazione, la bici non è prenotabile
		
		datiPrenotazioneBici['orario'] = datetime(1970, 1, 1, 8, 0)
		bici.prenota(datiPrenotazioneBici) # la bici è prenotabile fino alle 8:00

		# disdico le prenotazioni
		while len(bici.getOrariPrenotati()) > 0:
			bici.rimuoviOrarioPrenotazione(bici.getOrariPrenotati()[0])
		while len(camera.getVacanzaAttuale().getPrenotazioniBici()) > 0: # type: ignore
			camera.getVacanzaAttuale().rimuoviPrenotazioneBici(camera.getVacanzaAttuale().getPrenotazioniBici()[0]) # type: ignore

		# salvo la disdetta su file
		self.biciclette[5] = bici
		self.camere[1] = camera
		GestoreFile.salvaPickle(self.biciclette, Path(self.paths['bici']))
		GestoreFile.salvaPickle(self.camere, Path(self.paths['camere']))

		# termino la vacanza per la camera
		camera.terminaAssegnamento()
	

	def testAssegnamentoSenzaPrenotazione(self):
		camera : Camera = self.camere[1]

		bici : list[Bici] = [self.biciclette[2], self.biciclette[5], self.biciclette[11]]

		for bicicletta in bici:
			if bicicletta.isAssegnato():
				print('!!!!!!!!!!!!!!!!!!!!!!!'
					  'testAssegnamentoSenzaPrenotazione non eseguito: '
					  'almeno una tra le bici numero 2, 5 e 11 è assegnata al momento.\n'
					  'Terminare il loro assegnamento e runnare di nuovo il test.'
					  '!!!!!!!!!!!!!!!!!!!!!!!')
				return
			
		self.assertEqual(0, len(camera.getVacanzaAttuale().getNoleggiBici())) # type: ignore
		
		datiAssegnamento = {
			'camera' : camera,
			'prenotazione' : None,
			'biciclette' : self.biciclette,
			'camere' : self.camere
		}
		for bicicletta in bici:
			bicicletta.assegna(datiAssegnamento)

		# dopo l'assegnamento le bici sono assegnate
		for bicicletta in bici:
			self.assertEqual(True, bicicletta.isAssegnato())

		# verificare che la modifica sia stata salvata su file
		bicicletteBis = GestoreFile.leggiDictPickle(Path(self.paths['bici']))
		self.assertEqual(True, bicicletteBis[2].isAssegnato())
		self.assertEqual(True, bicicletteBis[5].isAssegnato())
		self.assertEqual(True, bicicletteBis[11].isAssegnato())

		# verificare che nel file i noleggi siano stati aggiunti alla vacanza e che siano in corso
		camereBis = GestoreFile.leggiDictPickle(Path(self.paths['camere']))
		self.assertEqual(3, len(camereBis[1].getVacanzaAttuale().getNoleggiBici()))
		for noleggio in camereBis[1].getVacanzaAttuale().getNoleggiBici(): # type: ignore
			self.assertEqual(True, noleggio.isInCorso())


		for bicicletta in bici:
			bicicletta.terminaAssegnamento()
		
		# dopo il termine dell'assegnamento le bici sono nuovamente disponibili
		for bicicletta in bici:
			self.assertEqual(False, bicicletta.isAssegnato())

		# verificare che la modifica sia stata salvata su file
		bicicletteBis = GestoreFile.leggiDictPickle(Path(self.paths['bici']))
		self.assertEqual(False, bicicletteBis[2].isAssegnato())
		self.assertEqual(False, bicicletteBis[5].isAssegnato())
		self.assertEqual(False, bicicletteBis[11].isAssegnato())

		# verificare che nel file i noleggi siano conclusi
		camereBis = GestoreFile.leggiDictPickle(Path(self.paths['camere']))
		self.assertEqual(3, len(camereBis[1].getVacanzaAttuale().getNoleggiBici()))	
		for noleggio in camereBis[1].getVacanzaAttuale().getNoleggiBici(): # type: ignore
			self.assertEqual(True, noleggio.isConcluso())



if __name__ == '__main__':
	unittest.main()
