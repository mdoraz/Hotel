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


    def isSovrapposto(self, altroPeriodo : PeriodoConData):
        """Returns True if this period and altroPeriodo overlap."""
        sovrapposto = True
        if altroPeriodo.getInizio() >= self._fine: # se l'altro periodo inizia dopo la fine di questo o lo stesso giorno in cui questo finisce
            sovrapposto = False
        if altroPeriodo.getFine() <= self._inizio: # se l'altro periodo finisce prima dell'inizio di questo o lo stesso giorno in cui questo iniza
            sovrapposto = False
        return sovrapposto
    

    def __str__(self):
        return f"da {self._inizio.strftime('%d/%m/%Y')} a {self._fine.strftime('%d/%m/%Y')}"

    def __eq__(self, other : PeriodoConData) -> bool:
        if not isinstance(other, PeriodoConData):
            return False
        return self._inizio == other.getInizio() and self._fine == other.getFine()
