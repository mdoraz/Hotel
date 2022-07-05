import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
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
        pass
    def _btnRicercaClienteClicked(self):
        pass
    def _btnRegistraClienteClicked(self):
        pass
    def _btnPrelevaCaparraPrenotazioneClicked(self):
        pass
    def _btnConfermaPrenotazioneVacanzaClicked(self):
        pass
    def _btnRicercaPrenotazioneVacanzaClicked(self):
        pass
    def _btnModificaPrenotazioneVacanzaClicked(self):
        pass
    def _btnEliminaPrenotazioneVacanzaClicked(self):
        pass
    def _btnAggiungiClientiVacanzaClicked(self):
        pass
    def _btnEseguiCheckInClicked(self):
        pass
    def _btnRicercaVacanzaClicked(self):
        pass
    def _btnModificatermineVacanzaOmbrelloneClicked(self):
        pass
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

