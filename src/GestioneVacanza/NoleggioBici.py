from __future__ import annotations # per la post evaluation delle annotazioni
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GestioneVacanza.Stato import Stato
    from src.Servizi.Camera import Camera
    from src.Servizi.Bici import Bici

class NoleggioBici:

    def __init__(self, bici : Bici, camera : Camera, orario : datetime, stato : Stato):
        self._bici = bici
        self._camera = camera
        self._orario = orario
        self._stato = stato

    def getBici(self) -> Bici:
        return self._bici

    def getCamera(self) -> Camera:
        return self._camera

    def getOrario(self) -> datetime:
        return self._orario

    def isPrenotato(self) -> bool:
        return self._stato.value == 1

    def isInCorso(self) -> bool:
        return self._stato.value == 2

    def isConcluso(self) -> bool:
        return self._stato.value == 3

    def setBici(self, bici : Bici):
        self._bici = bici

    def setCamera(self, camera : Camera):
        self._camera = camera

    def setOrario(self, orario : datetime):
        self._orario = orario

    def setStato(self, stato : Stato):
        self._stato = stato
  