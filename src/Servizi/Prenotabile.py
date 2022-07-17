from abc import ABCMeta, abstractmethod

class Prenotabile(metaclass = ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @abstractmethod
    def prenota(self, datiPrenotazione : dict):
        raise NotImplementedError