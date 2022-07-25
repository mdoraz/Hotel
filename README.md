# Hotel
Permette la gestione di un hotel nella sua attività caratteristica. 

## Istruzioni per l'uso

- Entry point al programma in src/Main/\_\_main\_\_.py

- Al primo accesso, non ci sono dipendenti salvati nel sistema; sarà compito del titolare aggiungere quanti dipendenti desidera.
  Per accedere come titolare, le credenziali iniziali sono 'username' per lo username e 'password' per la password.
  Una volta eseguito il login, il titolare può modificare le proprie credenziali.

## Risoluzione problemi

Se durante l'esecuzione viene lanciata un'eccezione che riguarda la deserializzazione di un file pickle
(a seguito dell'istruzione pickle.load() presente nel metodo leggiPickle() della classe GestoreFile)
allora bisogna ricreare i file pickle.
Per risolvere il problema, creare un nuovo file python ovunque nella cartella Hotel ed eseguire il seguente snippet:

```
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



creaCamere()
creaOmbrelloni()
creaBici()
```