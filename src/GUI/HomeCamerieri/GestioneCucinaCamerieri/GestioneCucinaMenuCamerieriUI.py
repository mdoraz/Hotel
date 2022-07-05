import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.HomeCamerieri.GestioneCucinaCamerieri.ModificaPrenotazioneColazioneInCameraUI import \
    ModificaPrenotazioneColazioneInCameraUI
from src.GUI.HomeCamerieri.GestioneCucinaCamerieri.PrenotaColazioneInCameraGiornoSuccessivoUI import \
    PrenotaColazioneInCameraGiornoSuccessivoUI


class GestioneCucinaMenuCamerieriUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('GestioneCucinaMenu.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnPrenotaColazioneInCameraGiornoSuccessivo.clicked.connect(self._btnPrenotaColazioneInCameraGiornoSuccessivoClicked)
        self.btnModificaPrenotazioneColazioneInCamera.clicked.connect(self._btnModificaPrenotazioneColazioneInCameraClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self._btnTornarePaginaPrecedente_2Clicked)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self._btnTornarePaginaPrecedente_3Clicked)


    def _btnPrenotaColazioneInCameraGiornoSuccessivoClicked(self):
        self.close()
        self.widgetPrenotaColazioneInCameraGiornoSuccessivo= PrenotaColazioneInCameraGiornoSuccessivoUI(self)
        self.widgetPrenotaColazioneInCameraGiornoSuccessivo.show()
    def _btnModificaPrenotazioneColazioneInCameraClicked(self):
        self.close()
        self.widgetModificaPrenotazioneColazioneInCamera = ModificaPrenotazioneColazioneInCameraUI(self)
        self.widgetModificaPrenotazioneColazioneInCamera.show()

    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

    def _btnTornarePaginaPrecedente_2Clicked(self):
        self.close()
        self.previous.show()

    def _btnTornarePaginaPrecedente_3Clicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = GestioneCucinaMenuCamerieriUI()
    mainWidget.show()
    sys.exit(app.exec_())