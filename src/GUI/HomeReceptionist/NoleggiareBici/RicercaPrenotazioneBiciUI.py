import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile


class RicercaPrenotazioneBiciUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('RicercaPrenotazioneBici.ui', Path.cwd()), self)
        self.setMinimumSize(500,400)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaCamera.clicked.connect(self._btnRicercaCameraClicked)
        self.btnConfermaScelteBici.clicked.connect(self._btnConfermaScelteBiciClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnRicercaCameraClicked(self):
        pass
    def _btnConfermaScelteBiciClicked(self):
        pass
    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaPrenotazioneBiciUI()
    mainWidget.show()
    sys.exit(app.exec_())