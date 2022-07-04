import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile


class HomeNoleggiareUnaBiciUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('HomeNoleggiareUnaBici.ui', Path.cwd()), self)
        self.setMinimumSize(500,300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaOrarioRicercato.clicked.connect(self._btnRicercaOrarioRicercatoClicked)
        self.btnAssociaBiciSelezionataAllaPrenotazione.clicked.connect(self._btnAssociaBiciSelezionataAllaPrenotazioneClicked)
        self.btnAssociaCameraAllaPrenotazione.clicked.connect(self._btnAssociaCameraAllaPrenotazioneClicked)
        self.btnEffettuaPrenotazione.clicked.connect(self._btnEffettuaPrenotazioneClicked)
        self.btnRicercaPrenotazioneBici.clicked.connect(self._btnRicercaPrenotazioneBiciClicked)
        self.btnModificaPrenotazione.clicked.connect(self._btnModificaPrenotazioneClicked)
        self.btnEliminaPrenotazione.clicked.connect(self._btnEliminaPrenotazioneClicked)
        self.btnNo.clicked.connect(self._btnNoClicked)
        self.btnSi.clicked.connect(self._btnSiClicked)
        self.btnRicercaNoleggiAssociati.clicked.connect(self._btnRicercaNoleggiAssociatiClicked)
        self.btnConfermaTerminareNoleggio.clicked.connect(self._btnConfermaTerminareNoleggioClicked)
        self.btnTornareHomeReceptionist.clicked.connect(self._btnTornareHomeReceptionistClicked)

    def _btnRicercaOrarioRicercatoClicked(self):
        pass

    def _btnAssociaBiciSelezionataAllaPrenotazioneClicked(self):
        pass

    def _btnAssociaCameraAllaPrenotazioneClicked(self):
        pass

    def _btnEffettuaPrenotazioneClicked(self):
        pass

    def _btnRicercaPrenotazioneBiciClicked(self):
        pass

    def _btnModificaPrenotazioneClicked(self):
        pass

    def _btnEliminaPrenotazioneClicked(self):
        pass

    def _btnNoClicked(self):
        pass

    def _btnSiClicked(self):
        pass

    def _btnRicercaNoleggiAssociatiClicked(self):
        pass

    def _btnConfermaTerminareNoleggioClicked(self):
        pass

    def _btnTornareHomeReceptionistClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeNoleggiareUnaBiciUI()
    mainWidget.show()
    sys.exit(app.exec_())