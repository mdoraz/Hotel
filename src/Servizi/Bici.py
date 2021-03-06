from datetime import datetime, timedelta
from pathlib import Path

from src.GestioneVacanza.NoleggioBici import NoleggioBici
from src.GestioneVacanza.Stato import Stato
from src.Gestori.GestoreFile import GestoreFile
from src.Gestori.GestoreTransazioni import GestoreTransazioni
from src.Servizi.Camera import Camera
from src.Servizi.Prenotabile import Prenotabile
from src.Servizi.Assegnabile import Assegnabile
from src.Utilities.exceptions import ArgumentTypeError, AssignmentError, CorruptedFileError, NotAvailableError

class Bici(Prenotabile, Assegnabile):
    
    def __init__(self, numero : int, tipo : bool):
        super().__init__()
        self._numero = numero
        self._tipo = tipo
        self._orariPrenotati = []

    def getNumero(self) -> int:
        return self._numero

    def getTipo(self) -> bool:
        return self._tipo

    def getOrariPrenotati(self) -> list[datetime]:
        return self._orariPrenotati

    def setNumero(self, numero : int):
        self._numero = numero

    def setTipo(self, tipo : bool):
        self._tipo = tipo
    
    def rimuoviOrarioPrenotazione(self, orario : datetime):
        self._orariPrenotati.remove(orario)
    

    def prenota(self, datiPrenotazione : dict):
        """Creates a reservation for this bike. datiPrenotazione must have this keys: 'orario' and 'camera'.
        The type values are: datetime for 'orario' and Camera for 'camera'."""
        
        if not isinstance(datiPrenotazione['orario'], datetime) or not isinstance(datiPrenotazione['camera'], Camera):
           raise ArgumentTypeError('Some argument has not the correct type.')

        orario = datiPrenotazione['orario']
        camera = datiPrenotazione['camera']

        if not camera.isAssegnato():
            raise AssignmentError('The room associated to this reservation is not currently assigned, cannot reserve a bike for that room.')

        if not self.isDisponibile(orario):
            raise NotAvailableError('This bike is not available at the requested time.')

        # inserimento ordinato dell'orario nella lista di orari prenotati
        i = 0
        while i < len(self._orariPrenotati) and orario > self._orariPrenotati[i]:
            i += 1
        self._orariPrenotati.insert(i, orario)

        # salvo le modifiche apportate a questa bici
        biciclette = self._readDict('bici')
        biciclette[self._numero] = self
        GestoreFile.salvaPickle(biciclette, Path(paths['bici']))
        
        # creo la prenotazione della bici e la aggiungo a quelle associate alla vacanza
        prenotazione = NoleggioBici(self, camera, orario, Stato.PRENOTATO)
        camera.getVacanzaAttuale().aggiungiPrenotazioneBici(prenotazione) # type: ignore

        # salvo le modifiche apportate alla vacanza
        camere = self._readDict('camere')
        camere[camera.getNumero()] = camera
        GestoreFile.salvaPickle(camere, Path(paths['camere']))
    

    def assegna(self, datiAssegnamento : dict):
        """This method assigns this bike. datiAssegnamento must contain the following keys: 'camera', 'prenotazione'.
        The values types must be: Camera for 'camera', NoleggioBici (or None if there isn't a reservation) for 'prenotazione'."""
        
        if self._assegnato:
            raise AssignmentError('This bike is already assigned.')

        camere = self._readDict('camere')
        biciclette = self._readDict('bici')

        if datiAssegnamento['prenotazione'] == None:
            if not isinstance(datiAssegnamento['camera'], Camera):
                raise ArgumentTypeError("The value of 'camera' key of datiAssegnamento is not of the Camera class.")
            self._assegnaSenzaPrenotazione(datiAssegnamento['camera'], camere, biciclette)
        
        elif isinstance(datiAssegnamento['prenotazione'], NoleggioBici):
            self._assegnaConPrenotazione(datiAssegnamento['prenotazione'], camere, biciclette)
        else:
            raise ArgumentTypeError("The value of 'prenotazione' key of datiAssegnamento is not of the NoleggioBici class.")

    
    def _assegnaConPrenotazione(self, prenotazione : NoleggioBici, camere : dict, biciclette : dict):
        
        self._assegnato = True # questa bici diventa assegnata
        biciclette[self._numero] = self
        GestoreFile.salvaPickle(biciclette, Path(GestoreFile.leggiJson(Path('paths.json'))['bici'])) # salvo le modifiche apportate a questa bici

        # dalla vacanza associata alla camera che ha noleggiato questa bici, rimuovo la prenotazione e aggiungo il noleggio
        prenotazione.getCamera().getVacanzaAttuale().rimuoviPrenotazioneBici(prenotazione) # type: ignore
        prenotazione.setStato(Stato.IN_CORSO)
        prenotazione.getCamera().getVacanzaAttuale().aggiungiNoleggioBici(prenotazione) # type: ignore

        camere[prenotazione.getCamera().getNumero()] = prenotazione.getCamera()
        GestoreFile.salvaPickle(camere, Path(GestoreFile.leggiJson(Path('paths.json'))['camere'])) # salvo le modifiche apportate alla vacanza associata alla camera


    def _assegnaSenzaPrenotazione(self, camera : Camera, camere : dict, biciclette : dict):
        
        self._assegnato = True # questa bici diventa assegnata
        biciclette[self._numero] = self
        GestoreFile.salvaPickle(biciclette, Path(GestoreFile.leggiJson(Path('paths.json'))['bici'])) # salvo le modifiche apportate a questa bici

        orario = datetime.now() + timedelta(minutes = 1)
        noleggio = NoleggioBici(self, camera, orario, Stato.IN_CORSO)
        camera.getVacanzaAttuale().aggiungiNoleggioBici(noleggio) # type: ignore

        camere[camera.getNumero()] = camera
        GestoreFile.salvaPickle(camere, Path(GestoreFile.leggiJson(Path('paths.json'))['camere'])) # salvo le modifiche apportate alla vacanza associata alla camera


    def terminaAssegnamento(self):
        self._assegnato = False
        # salvo le modifiche apportate a questa bici
        biciclette = self._readDict('bici')
        biciclette[self._numero] = self
        GestoreFile.salvaPickle(biciclette, Path(paths['bici']))
        
        self._terminaNoleggioInCorso() # cerco il noleggio in corso associato a questa bici e lo imposto come concluso

    
    def _terminaNoleggioInCorso(self):
        camere = self._readDict('camere')

        for camera in camere.values():
            if camera.isAssegnato():
                for noleggio in camera.getVacanzaAttuale().getNoleggiBici():
                    if noleggio.isInCorso() and noleggio.getBici().getNumero() == self._numero:
                        noleggio.setStato(Stato.CONCLUSO)
                        maxDurataNoleggio = timedelta(hours = 2)
                        if datetime.now() - noleggio.getOrario() > maxDurataNoleggio: # se ?? stata riconsegnata la bici in ritardo
                            GestoreTransazioni.prelevaMultaBici(camera.getVacanzaAttuale().getNumeroCarta())
        
        GestoreFile.salvaPickle(camere, Path(paths['camere']))


    def isDisponibile(self, orario : datetime) -> bool:
        disponibile = True
        i = 0
        maxDurataNoleggio = timedelta(hours = 2)
        while i < len(self._orariPrenotati) and disponibile:
            if self._orariPrenotati[i] >= orario and self._orariPrenotati[i] - orario < maxDurataNoleggio: # se la distanza tra l'orario pernotato e l'orario richiesto
                disponibile = False                                                                     # ?? inferiore alla durata massima di un noleggio
            elif self._orariPrenotati[i] < orario and orario - self._orariPrenotati[i] < maxDurataNoleggio:
                disponibile = False
            i += 1
        return disponibile


    def _readDict(self, pathsKey : str) -> dict:
        global paths
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            dictionary = GestoreFile.leggiDictPickle(Path(paths[pathsKey]))
        except CorruptedFileError:
            raise
        return dictionary


    def __str__(self):
        return f"bici {self._numero}: {'donna' if self._tipo == True else 'uomo'}"
