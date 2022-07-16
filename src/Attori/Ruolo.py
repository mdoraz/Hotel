from enum import Enum

class Ruolo(Enum):
    
    RECEPTIONIST = 1
    CAMERIERE = 2

    @classmethod
    def enumFromStr(cls, string : str):
        return cls.RECEPTIONIST if string.strip().lower() == 'receptionist' else cls.CAMERIERE

    def __str__(self):
        return 'Receptionist' if self.value == 1 else 'Cameriere'