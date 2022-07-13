import unittest
from pathlib import Path
from datetime import date

from src.Attori.Persona import Persona
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import ArgumentTypeError, CreationError, NotAvailableError


class TestCamera(unittest.TestCase):

	def setUp(self):
		self.paths = GestoreFile.leggiJson(Path('paths.json'))
		self.camere = GestoreFile.leggiDictPickle(Path(self.paths['camere']))


	def tearDown(self):
		pass


	def testAggiungiRimuoviPrenotazione(self):
		camera1 = self.camere[1]
		if not isinstance(camera1, Camera):
			raise Exception
		nPrenotazioniIniziali = len(camera1.getPrenotazioni())
		
		datiPrenotazione1 = {
			'periodo' : PeriodoConData(date(2000, 7, 1), date(2000, 7, 7)),
			'tipoSoggiorno' : Soggiorno.MEZZA_PENSIONE,
			'nominativo' : Persona('Eustachio', 'Liguori', date(1980, 7, 6), 'Pistoia', 'eustoia@hotmail.com', '393204820'),
			'numeroCarta' : '193028018382001'
		}
		camera1.prenota(datiPrenotazione1)
		
		self.assertEqual(nPrenotazioniIniziali + 1, len(camera1.getPrenotazioni())) # verifica dell'avvenuta aggiunta della prenotazione
		self.assertEqual(str(camera1.getPrenotazioni()[0]), 'camera 1 dal 01/07/2000 al 07/07/2000 - Liguori - Mezza pensione')

		datiPrenotazione1['nominativo'] = 'Eustachio' # nominativo str invece di Persona
		self.assertRaises(ArgumentTypeError, camera1.prenota, datiPrenotazione1) # verifica eccezione in caso di tipo sbagliato
 
		# ricarico le camere dal file pickle per vedere se la prenotazione è stata salvata correttamente
		camere = GestoreFile.leggiDictPickle(Path(self.paths['camere']))
		self.assertEqual(nPrenotazioniIniziali + 1, len(camere[1].getPrenotazioni()))
		self.assertEqual(str(camere[1].getPrenotazioni()[0]), 'camera 1 dal 01/07/2000 al 07/07/2000 - Liguori - Mezza pensione')

		# rimuovo la prenotazione e salvo su file
		prenotazionie1 = camera1.getPrenotazioni()[0] # la prenotazione aggiunta all'inizio del test è la prima della lista, poichè questa
													# è ordinata secondo l'ordine temporale e dalla gui non si può prenotare per un periodo passato
		camera1.eliminaPrenotazione(prenotazionie1)
		camere[1] = camera1
		self.assertEqual(nPrenotazioniIniziali, len(camere[1].getPrenotazioni())) # verifica dell'avvenuta rimozione della prenotazione
		GestoreFile.salvaPickle(camere, Path(self.paths['camere']))


	def testSovrapposizionePrenotazioni(self):
		camera1 = self.camere[1]
		if not isinstance(camera1, Camera):
			raise Exception

		datiPrenotazione1 = {
			'periodo' : PeriodoConData(date(2000, 7, 1), date(2000, 7, 7)),
			'tipoSoggiorno' : Soggiorno.MEZZA_PENSIONE,
			'nominativo' : Persona('Eustachio', 'Liguori', date(1980, 7, 6), 'Pistoia', 'eustoia@hotmail.com', '393204820'),
			'numeroCarta' : '193028018382001'
		}
		camera1.prenota(datiPrenotazione1)

		datiPrenotazione2 = {
			'periodo' : PeriodoConData(date(2000, 7, 6), date(2000, 7, 10)),
			'tipoSoggiorno' : Soggiorno.MEZZA_PENSIONE,
			'nominativo' : Persona('Gaia', 'Derisis', date(1976, 5, 4), 'Avelletri', 'avel@alice.it', '3284920181'),
			'numeroCarta' : '434291041208445'
		}
		self.assertRaises(NotAvailableError, camera1.prenota, datiPrenotazione2) # la prenotazione ha un periodo che si sovrappone a quello di un'altra prenotazione

		datiPrenotazione2['periodo'].setInizio(date(2000, 7, 7))
		camera1.prenota(datiPrenotazione2) # se l'inizio di una prenotazione e la fine di un'altra coincidono, la prenotazione non da errore

		# rimuovo le prenotazioni e salvo su file
		while len(camera1.getPrenotazioni()) > 0:
			camera1.eliminaPrenotazione(camera1.getPrenotazioni()[0])
		self.camere[1] = camera1
		GestoreFile.salvaPickle(self.camere, Path(self.paths['camere']))

	
	def testAssegnamento(self):
		camera = self.camere[1]
		if not isinstance(camera, Camera):
			raise Exception

		datiPrenotazione = {
			'periodo' : PeriodoConData(date(2000, 7, 1), date(2000, 7, 7)),
			'tipoSoggiorno' : Soggiorno.MEZZA_PENSIONE,
			'nominativo' : Persona('Eustachio', 'Liguori', date(1980, 7, 6), 'Pistoia', 'eustoia@hotmail.com', '393204820'),
			'numeroCarta' : '193028018382001'
		}
		camera.prenota(datiPrenotazione)
		ombrelloni = GestoreFile.leggiDictPickle(Path(self.paths['ombrelloni']))

		datiAssegnamento = {
			'prenotazione' : camera.getPrenotazioni()[0], # prenotazione appena aggiunta è in prima posizione (ordine di data)
			'clienti' : [datiPrenotazione['nominativo'], Persona('Rosanna', 'Camuzi', date(1981, 2, 3), 'Pistoia', 'rosacamu@hotmail.com', '3933949056')],
			'ombrellone' : ombrelloni[10]
		}
		camera.assegna(datiAssegnamento)

		# verifica l'assegnamento di camera e ombrellone
		self.assertEqual(True, ombrelloni[10].isAssegnato())
		self.assertEqual(True, camera.isAssegnato())
		self.assertNotEqual(None, camera.getVacanzaAttuale())
		self.assertEqual(False, datiAssegnamento['prenotazione'] in camera.getPrenotazioni()) # verifica la rimozione della prenotazione da quelle che ha la camera

		# verifica che ombrellone e camera non sono più assegnati 
		camera.terminaAssegnamento()
		self.assertEqual(False, ombrelloni[10].isAssegnato())
		self.assertEqual(False, camera.isAssegnato())
		self.assertEqual(None, camera.getVacanzaAttuale())

		# viene aggiunto un terzo elemento alla lista dei clienti
		datiAssegnamento['clienti'].append(Persona('Antonino', 'Liguori', date(1999, 8, 7), 'Pistoia', 'antonino@hotmail.com', '324598284'))
		self.assertRaises(CreationError, camera.assegna, datiAssegnamento) # lanciata eccezione perchè i clienti sono 3 e la camera ha 2 posti



if __name__ == '__main__':
	unittest.main()