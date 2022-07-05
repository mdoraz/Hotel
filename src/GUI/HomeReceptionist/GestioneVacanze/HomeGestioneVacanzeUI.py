import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.HomeReceptionist.GestioneVacanze.AggiungereClientiCheckInUI import AggiungereClientiCheckInUI
from src.GUI.HomeReceptionist.GestioneVacanze.EliminaPrenotazioneVacanzaUI import EliminaPrenotazioneVacanzaUI
from src.GUI.HomeReceptionist.GestioneVacanze.ModificaPrenotazioneVacanzaUI import ModificaPrenotazioneVacanzaUI
from src.GUI.HomeReceptionist.GestioneVacanze.ModificaTermineVacanzaOmbrelloneUI import \
    ModificaTermineVacanzaOmbrelloneUI
from src.GUI.HomeReceptionist.GestioneVacanze.RicercaPrenotazioneVacanzaUI import RicercaPrenotazioneVacanzaUI
from src.GUI.HomeReceptionist.GestioneVacanze.RicercaVacanzaUI import RicercaVacanzaUI
from src.GUI.HomeReceptionist.GestioneVacanze.SelezionaCameraUI import SelezionaCameraUI
from src.GUI.HomeReceptionist.GestireClienti.HomeGestireUnClienteUI import HomeGestireUnClienteUI
from src.GUI.HomeReceptionist.GestireClienti.RicercaDelCliente1UI import RicercaDelCliente1UI
from src.Gestori.GestoreFile import GestoreFile

class HomeGestioneVacanzeUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('HomeGestioneVacanze.ui', Path.cwd()), self)
        self.setMinimumSize(1000,600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnSelezionaCamera.clicked.connect(self._btnSelezionaCameraClicked)
        self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
        self.btnRegistraCliente.clicked.connect(self._btnRegistraClienteClicked)
        self.btnPrelevaCaparraPrenotazione.clicked.connect(self._btnPrelevaCaparraPrenotazioneClicked)
        self.btnConfermaPrenotazioneVacanza.clicked.connect(self._btnConfermaPrenotazioneVacanzaClicked)
        self.btnRicercaPrenotazioneVacanza.clicked.connect(self._btnRicercaPrenotazioneVacanzaClicked)
        self.btnModificaPrenotazioneVacanza.clicked.connect(self._btnModificaPrenotazioneVacanzaClicked)
        self.btnEliminaPrenotazioneVacanza.clicked.connect(self._btnEliminaPrenotazioneVacanzaClicked)
        self.btnAggiungiClientiVacanza.clicked.connect(self._btnAggiungiClientiVacanzaClicked)
        self.btnEseguiCheckIn.clicked.connect(self._btnEseguiCheckInClicked)
        self.btnRicercaVacanza.clicked.connect(self._btnRicercaVacanzaClicked)
        self.btnModificatermineVacanzaOmbrellone.clicked.connect(self._btnModificatermineVacanzaOmbrelloneClicked)
        self.btnEseguireCheckOut.clicked.connect(self._btnEseguireCheckOutClicked)
        self.btnTornareHomeReceptionist.clicked.connect(self._btnTornareHomeReceptionistClicked)

    def _btnSelezionaCameraClicked(self):
        self.widgetSelezionaCamera = SelezionaCameraUI(self)
        self.widgetSelezionaCamera.show()

    def _btnRicercaClienteClicked(self):
        self.close()
        self.widgetRicercaDelCliente1 = RicercaDelCliente1UI(self)
        self.widgetRicercaDelCliente1.show()
    def _btnRegistraClienteClicked(self):
        self.close()
        self.tabHomeGestireUnCliente = HomeGestireUnClienteUI(self)
        self.tabHomeGestireUnCliente.show()

    def _btnPrelevaCaparraPrenotazioneClicked(self):
        pass

    def _btnConfermaPrenotazioneVacanzaClicked(self):
        pass

    def _btnRicercaPrenotazioneVacanzaClicked(self):
        self.close()
        self.widgetRicercaPrenotazioneVacanza = RicercaPrenotazioneVacanzaUI(self)
        self.widgetRicercaPrenotazioneVacanza.show()

    def _btnModificaPrenotazioneVacanzaClicked(self):
        self.widgetModificaPrenotazioneVacanza = ModificaPrenotazioneVacanzaUI(self)
        self.widgetModificaPrenotazioneVacanza.show()

    def _btnEliminaPrenotazioneVacanzaClicked(self):
        self.widgetEliminaPrenotazioneVacanza = EliminaPrenotazioneVacanzaUI(self)
        self.widgetEliminaPrenotazioneVacanza.show()

    def _btnAggiungiClientiVacanzaClicked(self):
        self.widgetAggiungereClientiCheckIn = AggiungereClientiCheckInUI(self)
        self.widgetAggiungereClientiCheckIn.show()

    def _btnEseguiCheckInClicked(self):
        pass

    def _btnRicercaVacanzaClicked(self):
        self.widgetRicercaVacanza = RicercaVacanzaUI(self)
        self.widgetRicercaVacanza.show()

    def _btnModificatermineVacanzaOmbrelloneClicked(self):
        self.widgetModificaTermineVacanzaOmbrellone = ModificaTermineVacanzaOmbrelloneUI(self)
        self.widgetModificaTermineVacanzaOmbrellone.show()

    def _btnEseguireCheckOutClicked(self):
        pass

    def _btnTornareHomeReceptionistClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeGestioneVacanzeUI()
    mainWidget.show()
    sys.exit(app.exec_())

