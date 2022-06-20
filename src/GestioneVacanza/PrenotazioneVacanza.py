from Utilities.PeriodoConData import PeriodoConData
from Servizi.Camera import Camera
from Attori.Persona import Persona
from GestioneVacanza.Soggiorno import Soggiorno

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