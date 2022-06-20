from abc import ABCMeta, abstractmethod

class Prenotabile(metaclass = ABCMeta):
    
    @abstractmethod
    def prenota(self, datiPrenotazione : dict):
        raise NotImplementedError