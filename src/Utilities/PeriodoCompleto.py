from __future__ import annotations
from datetime import date, datetime
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


    def isSovrapposto(self, altroPeriodo : PeriodoCompleto):
        """Returns True if this period and altroPeriodo overlap."""

        sovrapposto = True
        if altroPeriodo.getInizio() >= self._fine: # se l'altro periodo inizia dopo la fine di questo o lo stesso giorno in cui questo finisce
            sovrapposto = False
        if altroPeriodo.getFine() <= self._inizio: # se l'altro periodo finisce prima dell'inizio di questo o lo stesso giorno in cui questo iniza
            sovrapposto = False
        return sovrapposto
    

    def __str__(self):
        return f"da {self._inizio.strftime('%d/%m/%Y')} alle {self._inizio.strftime('%H:%M')} a {self._fine.strftime('%d/%m/%Y')}  alle {self._fine.strftime('%H:%M')}"

