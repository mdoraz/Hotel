import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.Dipendenti.HomeCamerieri.GestioneCucinaCamerieri.ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI import \
    ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI


class PrenotaColazioneInCameraGiornoSuccessivoUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('PrenotaColazioneInCameraGiornoSuccessivo.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous


    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnAvantiClicked(self):
        self.close()
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo = ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI(self)
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo.show()

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = PrenotaColazioneInCameraGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())
