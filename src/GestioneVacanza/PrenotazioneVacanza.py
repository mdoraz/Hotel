from __future__ import annotations # permette la post evaluation delle annotazioni: evita errori dovuti a classi utilizzate per i type hints ancora irrisolte quando compaiono nel codice
from typing import TYPE_CHECKING

from src.Attori.Persona import Persona
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.Utilities.PeriodoConData import PeriodoConData
if TYPE_CHECKING: # true solo durante il type checking: evita import error dovuti a circular import di classi coinvolte solo nei type hints
    from src.Servizi.Camera import Camera


class PrenotazioneVacanza:
    def __init__(self, periodo : PeriodoConData, camera : Camera, tipoSoggiorno : Soggiorno, nominativo : Persona, numeroCarta : str):
        self._periodo = periodo
        self._camera = camera
        self._tipoSoggiorno = tipoSoggiorno
        self._nominativo = nominativo
        self._numeroCarta = numeroCarta

    def getCamera(self) -> Camera:
        return self._camera

    def getNominativo(self) -> Persona:
        return self._nominativo

    def getNumeroCarta(self) -> str:
        return self._numeroCarta

    def getPeriodo(self) -> PeriodoConData:
        return self._periodo

    def getTipoSoggiorno(self) -> Soggiorno:
        return self._tipoSoggiorno

    def setCamera(self, camera : Camera):
        self._camera = camera

    def setNominativo(self, nominativo : Persona):
        self._nominativo = nominativo

    def setNumeroCarta(self, numeroCarta : str):
        self._numeroCarta = numeroCarta

    def setPeriodo(self, periodo : PeriodoConData):
        self._periodo = periodo

    def setTipoSoggiorno(self, tipoSoggiorno : Soggiorno):
        self._tipoSoggiorno = tipoSoggiorno
    
    def __str__(self):
        return (f"camera {self._camera.getNumero()} dal {self._periodo.getInizio().strftime('%d/%m/%Y')} al "
                f"{self._periodo.getFine().strftime('%d/%m/%Y')} - {self._nominativo.getCognome()}"
                f" - {str(self._tipoSoggiorno)}")
                

    def __eq__(self, other: PrenotazioneVacanza) -> bool:
        if not isinstance(other, PrenotazioneVacanza):
            return False
        return (self._camera.getNumero() == other.getCamera().getNumero() and
                self._nominativo.getId() == other.getNominativo().getId() and
                self._periodo == other.getPeriodo())