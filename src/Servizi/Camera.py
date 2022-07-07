from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, Union

from src.Attori.Persona import Persona
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.Gestori.GestoreFile import GestoreFile
from src.Gestori.GestoreTransazioni import GestoreTransazioni
from src.GestioneVacanza.Vacanza import Vacanza
from src.Servizi.Ombrellone import Ombrellone
from src.Servizi.Prenotabile import Prenotabile
from src.Servizi.Assegnabile import Assegnabile
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import ArgumentTypeError, CorruptedFileError
if TYPE_CHECKING:  # TYPE_CHECKING == True solo durante il type checking. Si evita un circular import error dovuto all'import di una classe utilizzata solo per un type hint
    from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza


class Camera(Prenotabile, Assegnabile):

    def __init__(self, numero : int, numeroPersone : int):
        super().__init__()
        self._numero  = numero
        self._numeroPersone = numeroPersone
        self._prenotazioni = []
        self._vacanzaAttuale = None
        

    def getNumero(self) -> int:
        return self._numero

    def getNumeroPersone(self) -> int:
        return self._numeroPersone

    def getPrenotazioni(self) -> list:
        return self._prenotazioni

    def getVacanzaAttuale(self) -> Union[Vacanza, None]:
        return self._vacanzaAttuale

    def setNumero(self, numero : int):
        self._numero = numero

    def setNumeroPersone(self, numeroPersone : int):
        self._numeroPersone = numeroPersone
    
    def eliminaPrenotazione(self, prenotazione : PrenotazioneVacanza):
        self._prenotazioni.remove(prenotazione)
    

    def prenota(self, datiPrenotazione : dict):
        """Creates a new reservation. datiPrenotazione must have this keys: 'periodo', 'tiposSoggiorno', 'nominativo', 'numeroCarta'.
        The values types must be: PeriodoConData for 'periodo', Soggiorno for 'tipoSoggiorno, Persona for 'nominativo', 
        str for numeroCarta"""
        
        if (not isinstance(datiPrenotazione['periodo'], PeriodoConData) or not isinstance(datiPrenotazione['tipoSoggiorno'], Soggiorno) or
           not isinstance(datiPrenotazione['nominativo'], Persona) or not isinstance(datiPrenotazione['numeroCarta'], str)):
           raise ArgumentTypeError('Some argument has not the correct type.')
        
        prenotazione = PrenotazioneVacanza(datiPrenotazione['periodo'], self, datiPrenotazione['tipoSoggiorno'],
                                           datiPrenotazione['nominativo'], datiPrenotazione['numeroCarta'])
        # inserimento ordinato di prenotazione nella lista di prenotazioni di questa camera
        i = 0
        while prenotazione.getPeriodo().getInizio() > self._prenotazioni[i].getPeriodo().getInizio():
            i += 1
        self._prenotazioni.insert(i, prenotazione)

        GestoreTransazioni.prelevaCaparra(prenotazione)

        self._salvaCameraSuFile()

    
    def assegna(self, datiAssegnamento : dict):
        """Assigns this room, at check-in time. datiAssegnamenti must have this keys: 'prenotazione', 'clienti', 'ombrellone'.
        The values types must be: PrenotazioneVacanza for 'prenotazione', list[Persona] for 'clienti', Ombrellone for 'ombrellone'."""

        if (not isinstance(datiAssegnamento['prenotazione'], PrenotazioneVacanza) or not isinstance(datiAssegnamento['clienti'], list) or 
           not isinstance(datiAssegnamento['ombrellone'], Ombrellone)):
           raise ArgumentTypeError('Some argument has not the correct type.')

        vacanza = Vacanza(datiAssegnamento['prenotazione'], datiAssegnamento['clienti'], datiAssegnamento['ombrellone'])
        
        # questa camera diventa occupata
        self._vacanzaAttuale = vacanza        
        self._assegnato = True

        vacanza.getOmbrellone().assegna({}) # l'ombrellone diventa occupato

        self._prenotazioni.remove(datiAssegnamento['prenotazione']) # rimossa la prenotazione

        self._salvaCameraSuFile()


    def terminaAssegnamento(self):
        if not self._assegnato or not isinstance(self._vacanzaAttuale, Vacanza):
            raise Exception("Cannot terminate this room's assignment: room not assigned")
        
        GestoreTransazioni.prelevaCostoVacanza(self._vacanzaAttuale)
        self._vacanzaAttuale.getOmbrellone().terminaAssegnamento() # ombrellone nuovamente disponibile
        self._vacanzaAttuale.setInCorso(False) # vacanza conclusa

        # aggiungo la vacanza a quelle concluse rimuovo la sua associazione con questa camera
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            vacanzeConcluse = GestoreFile.leggiPickle(Path(paths['vacanzeConcluse']))
            if not isinstance(vacanzeConcluse, list):
                raise CorruptedFileError(f'{Path(paths["vacanzeConcluse"]).name} has been corrupted. To fix this issue, delete it.')
        except FileNotFoundError:
            vacanzeConcluse = []
        vacanzeConcluse.append(self._vacanzaAttuale)
        GestoreFile.salvaPickle(vacanzeConcluse, Path(paths['vacanzeConcluse']))

        # questa camera diventa libera
        self._vacanzaAttuale = None
        self._assegnato = False

        self._salvaCameraSuFile()

    
    def isDisponibile(self, periodo : PeriodoConData) -> bool:
        disponibile = True
        i = 0
        while i < len(self._prenotazioni) and disponibile:
            if periodo.isSovrapposto(self._prenotazioni[i].getPeriodo()):
                disponibile = False
            i += 1
        return disponibile


    def _salvaCameraSuFile(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
        if not isinstance(camere, dict): # se il file ha cambiato contenuto dal momento in cui è stato letto questo ombrellone ad ora
            raise CorruptedFileError(f'{Path(paths["camere"]).name} has been corrupted. To fix the issue, delete it.')
        camere[self._numero] = self
        GestoreFile.salvaPickle(camere, Path(paths['camere']))

    
    def __str__(self):
        return f'camera {self._numero} --> persone: {self._numeroPersone}'
