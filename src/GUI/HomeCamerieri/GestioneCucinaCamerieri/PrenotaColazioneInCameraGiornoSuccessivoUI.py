import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeCamerieri.GestioneCucinaCamerieri.ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI import \
    ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI


class PrenotaColazioneInCameraGiornoSuccessivoUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Cameriere/GestisciCucina/PrenotaColazioneInCameraGiornoSuccessivo.ui', self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()


    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnIndietro.clicked.connect(self.close)

    def _btnAvantiClicked(self):
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo = ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI()
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = PrenotaColazioneInCameraGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())
