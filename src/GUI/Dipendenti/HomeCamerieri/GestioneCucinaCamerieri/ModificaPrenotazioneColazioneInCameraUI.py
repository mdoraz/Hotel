import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class ModificaPrenotazioneColazioneInCameraUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ModificaPrenotazioneColazioneInCamera.ui',Path.cwd()), self)
        self.setMinimumSize(400, 200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

        self._hideWidget()

    def _hideWidget(self):
        self.widgetMenuModificare.hide()
        self.btnAnnulla.hide()

    def _connectButtons(self):
        self.btnConfermaModifiche.clicked.connect(self._btnConfermaModificheClicked)
        self.btnCerca.clicked.connect(self._btnCercaClicked)
        self.btnAnnulla.clicked.connect(self._btnAnnullaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnCercaClicked(self):
        self.widgetMenuModificare.show()
        self.btnAnnulla.show()
        self.setMinimumSize(600, 600)

    def _btnAnnullaClicked(self):
        self._hideWidget()
        self.setMinimumSize(400, 200)

    def _btnConfermaModificheClicked(self):
        pass


    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ModificaPrenotazioneColazioneInCameraUI()
    mainWidget.show()
    sys.exit(app.exec_())