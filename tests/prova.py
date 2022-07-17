from datetime import date, datetime
from pathlib import Path

from src.Servizi.Camera import Camera
from src.Servizi.Ombrellone import Ombrellone
from src.Servizi.Bici import Bici
from src.Gestori.GestoreFile import GestoreFile


paths = GestoreFile.leggiJson(Path('paths.json'))

def creaCamere():
	camere = {}

	for i in range(1, 37):
		nPersone = 0
		if i in range(1, 11):
			nPersone = 2
		elif i in range(11, 21):
			nPersone = 3
		elif i in range(21, 31):
			nPersone = 4
		else:
			nPersone = 5

		camere[i] = Camera(i, nPersone)
	
	GestoreFile.salvaPickle(camere, Path(paths['camere']))


def creaOmbrelloni():
	ombrelloni = {}

	for i in range(1, 37):
		ombrelloni[i] = Ombrellone(i)

	GestoreFile.salvaPickle(ombrelloni, Path(paths['ombrelloni']))



def creaBici():
	biciclette = {}

	for i in range(1, 21):
		if i in range(1, 11):
			tipo = True
		else:
			tipo = False
		
		biciclette[i] = Bici(i, tipo)

	GestoreFile.salvaPickle(biciclette, Path(paths['bici']))


def svuotaNoleggi(numeroCamera):
	camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
	camera = camere[numeroCamera]

	camera.getVacanzaAttuale().setNoleggi([])

	GestoreFile.salvaPickle(camere, Path(paths['camere']))


creaBici()


