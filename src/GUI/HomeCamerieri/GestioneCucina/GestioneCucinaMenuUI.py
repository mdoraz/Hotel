import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeCamerieri.GestioneCucina.ModificaPrenotazioneColazioneInCameraUI import \
    ModificaPrenotazioneColazioneInCameraUI
from src.GUI.HomeCamerieri.GestioneCucina.PrenotaColazioneInCameraGiornoSuccessivoUI import \
    PrenotaColazioneInCameraGiornoSuccessivoUI


class GestioneCucinaMenuUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Cameriere/GestisciCucina/GestioneCucinaMenu.ui', self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnPrenotaColazioneInCameraGiornoSuccessivo.clicked.connect(self._btnPrenotaColazioneInCameraGiornoSuccessivoClicked)
        self.btnModificaPrenotazioneColazioneInCamera.clicked.connect(self._btnModificaPrenotazioneColazioneInCameraClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnPrenotaColazioneInCameraGiornoSuccessivoClicked(self):
        self.widgetPrenotaColazioneInCameraGiornoSuccessivo= PrenotaColazioneInCameraGiornoSuccessivoUI()
        self.widgetPrenotaColazioneInCameraGiornoSuccessivo.show()
    def _btnModificaPrenotazioneColazioneInCameraClicked(self):
        self.widgetModificaPrenotazioneColazioneInCamera = ModificaPrenotazioneColazioneInCameraUI()
        self.widgetModificaPrenotazioneColazioneInCamera.show()

    def _btnTornarePaginaPrecedenteClicked(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = GestioneCucinaMenuUI()
    mainWidget.show()
    sys.exit(app.exec_())