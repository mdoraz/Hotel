from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: # true solo durante il type checking
    from src.Attori.Dipendente import Dipendente
    from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
    from src.GestioneVacanza.Vacanza import Vacanza

class GestoreTransazioni:

    @staticmethod    
    def assegnaStipendio(dipendente : Dipendente):
        pass
    
    @staticmethod
    def prelevaCaparra(prenotazione : PrenotazioneVacanza):
        pass
    
    @staticmethod
    def prelevaCostoVacanza(vacanza : Vacanza):
        pass
    
    @staticmethod
    def prelevaMultaBici(numeroCarta : str):
        # tramite numeroCarta vengono prelevati 2 euro
        pass