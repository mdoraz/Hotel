from abc import ABCMeta, abstractmethod

class Assegnabile(metaclass = ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._assegnato = False

    @abstractmethod
    def assegna(self, datiAssegnamento : dict):
        raise NotImplementedError

    @abstractmethod
    def terminaAssegnamento(self):
        raise NotImplementedError
    
    def isAssegnato(self):
        return self._assegnato