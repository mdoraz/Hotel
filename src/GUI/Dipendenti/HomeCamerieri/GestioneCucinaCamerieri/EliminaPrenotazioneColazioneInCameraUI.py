import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class EliminaPrenotazioneColazioneInCameraUI(QTabWidget):
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
        self.widgetConfermaModifiche.hide()
        self.btnAnnulla.hide()

    def _connectButtons(self):
        self.btnConferma.clicked.connect(self._btnConfermaClicked)
        self.btnCerca.clicked.connect(self._btnCercaClicked)
        self.btnAnnulla.clicked.connect(self._btnAnnullaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnCercaClicked(self):
        self.widgetMenuModificare.show()
        self.widgetConfermaModifiche.show()
        self.btnAnnulla.show()
        self.setMinimumSize(600, 600)

    def _btnAnnullaClicked(self):
        self._hideWidget()
        self.setMinimumSize(400, 200)

    def _btnConfermaClicked(self):
        pass


    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = EliminaPrenotazioneColazioneInCameraUI()
    mainWidget.show()
    sys.exit(app.exec_())