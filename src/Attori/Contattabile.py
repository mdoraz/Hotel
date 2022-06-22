class Contattabile:
    
    def __init__(self, email : str, cellulare : str, **kwargs):
        self._email = email
        self._cellulare = cellulare
        super().__init__(**kwargs)

    def getCellulare(self) -> str:
        return self._cellulare

    def getEmail(self) -> str:
        return self._email

    def setCellulare(self, cellulare : str):
        self._cellulare = cellulare

    def setEmail(self, email : str):
        self._email = email
