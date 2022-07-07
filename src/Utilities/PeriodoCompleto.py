from __future__ import annotations
from datetime import datetime
from src.Utilities.exceptions import ArgumentTypeError, InvalidPeriodError

class PeriodoCompleto:
    
    def __init__(self, inizio : datetime, fine : datetime):
        self._verificaParametri(inizio, fine)
        self._inizio = inizio
        self._fine = fine

    def getInizio(self) -> datetime:
        return self._inizio
    
    def getFine(self) -> datetime:
        return self._fine

    def setInizio(self, inizio : datetime):
        self._verificaParametri(inizio, self._fine)
        self._inizio = inizio
    
    def setFine(self, fine : datetime):
        self._verificaParametri(self._inizio, fine)
        self._fine = fine

    def _verificaParametri(self, inizio, fine):
        if not (isinstance(inizio, datetime) and isinstance(fine, datetime)):
            raise ArgumentTypeError("inizio e fine di PeriodoComleto devono essere datetime")
        elif fine < inizio:
            raise InvalidPeriodError("inizio deve precedere temporalmente la fine di PeriodoCompleto")

    def isSovrapposto(self, other : PeriodoCompleto):
        """Returns True if this period and other overlap, even by one day."""
        return self._fine < other.getInizio() or self._inizio > other.getFine() 
