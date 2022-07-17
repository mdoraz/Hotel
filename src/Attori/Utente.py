class Utente:
    
    def __init__(self, username : str, password : str, **kwargs):
        super().__init__(**kwargs)
        self._username = username
        self._password = password

    def getPassword(self) -> str:
        return self._password

    def getUsername(self) -> str:
        return self._username

    def setPassword(self, password : str):
        self._password = password

    def setUsername(self, username : str):
        self._username = username