from __future__ import annotations
from datetime import date
from src.Utilities.exceptions import ArgumentTypeError, InvalidPeriodError

class PeriodoConData:
    
    def __init__(self, dataInizio : date, dataFine : date):
        try:
            self._verificaParametri(dataInizio, dataFine)
            self._inizio = dataInizio
            self._fine = dataFine
        except:
            raise

    def getInizio(self) -> date:
        return self._inizio
    
    def getFine(self) -> date:
        return self._fine

    def setInizio(self, dataInizio : date):
        try:
            self._verificaParametri(dataInizio, self._fine)
            self._inizio = dataInizio
        except:
            raise
    
    def setFine(self, dataFine : date):
        try:
            self._verificaParametri(self._inizio, dataFine)
            self._fine = dataFine
        except:
            raise

    def _verificaParametri(self, inizio, fine):
        if not (isinstance(inizio, date) and isinstance(fine, date)):
            raise ArgumentTypeError("dataInizio e dataFine di PeriodoConData devono essere date")
        elif fine < inizio:
            raise InvalidPeriodError("dataInizio deve precedere temporalmente dataFine di PeriodoConData") 

    def isSovrapposto(self, other : PeriodoConData):
        """Returns True if this period and other overlap, even by one day."""
        return self._fine < other.getInizio() or self._inizio > other.getFine() 
