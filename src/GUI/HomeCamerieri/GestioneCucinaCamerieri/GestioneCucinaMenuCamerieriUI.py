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
    def __init__(self):
        super().__init__()
        loadUi(GestoreFile.absolutePath('GestioneCucinaMenu.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnPrenotaColazioneInCameraGiornoSuccessivo.clicked.connect(self._btnPrenotaColazioneInCameraGiornoSuccessivoClicked)
        self.btnModificaPrenotazioneColazioneInCamera.clicked.connect(self._btnModificaPrenotazioneColazioneInCameraClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self.close)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self.close)


    def _btnPrenotaColazioneInCameraGiornoSuccessivoClicked(self):
        self.widgetPrenotaColazioneInCameraGiornoSuccessivo= PrenotaColazioneInCameraGiornoSuccessivoUI()
        self.widgetPrenotaColazioneInCameraGiornoSuccessivo.show()
    def _btnModificaPrenotazioneColazioneInCameraClicked(self):
        self.widgetModificaPrenotazioneColazioneInCamera = ModificaPrenotazioneColazioneInCameraUI()
        self.widgetModificaPrenotazioneColazioneInCamera.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = GestioneCucinaMenuCamerieriUI()
    mainWidget.show()
    sys.exit(app.exec_())