from enum import Enum

class Soggiorno(Enum):
    
    BED_AND_BREAKFAST = 1
    MEZZA_PENSIONE = 2
    PENSIONE_COMPLETA = 3

    @classmethod
    def enumFromStr(cls, string : str):
        if string.lower() == 'b&b' or string == 'bed and breakfast':
            return cls.BED_AND_BREAKFAST
        if string.lower() == 'mezza pensione':
            return cls.MEZZA_PENSIONE
        if string.lower() == 'pensione completa':
            return cls.PENSIONE_COMPLETA
        raise Exception("string argument doesn't correspond to any vacation types")


    def __str__(self):
        if self.value == 1:
            string = 'B&B'
        elif self.value == 2:
            string = 'Mezza pensione'
        else:
            string = 'Pensione completa'

        return string
    