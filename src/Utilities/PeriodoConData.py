from datetime import date
from Utilities.exeptions import ArgumentTypeError, InvalidPeriodError

class PeriodoConData:
    
    def __init__(self, dataInizio : date, dataFine : date):
        self._verificaParametri(dataInizio, dataFine)
        self._inizio = dataInizio
        self._fine = dataFine

    def getInizio(self) -> date:
        return self._inizio
    
    def getFine(self) -> date:
        return self._fine

    def setInizio(self, dataInizio : date):
        self._verificaParametri(dataInizio, self._fine)
        self._inizio = dataInizio
    
    def setFine(self, dataFine : date):
        self._verificaParametri(self._inizio, dataFine)
        self._fine = dataFine

    def _verificaParametri(self, inizio, fine):
        if not (isinstance(inizio, date) and isinstance(fine, date)):
            raise ArgumentTypeError("dataInizio e dataFine di PeriodoConData devono essere date")
        elif fine < inizio:
            raise InvalidPeriodError("dataInizio deve precedere temporalmente dataFine di PeriodoConData") 
