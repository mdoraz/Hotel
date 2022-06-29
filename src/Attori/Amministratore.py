from src.Attori.Contattabile import Contattabile
from src.Attori.Utente import Utente

class Amministratore(Contattabile, Utente):
    
    def __init__(self, email : str, cellulare : str, username : str, password : str):
        credenziali = {'username': username, 'password': password}
        super().__init__(email, cellulare, **credenziali)