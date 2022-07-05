import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiPranzoUI import ConfermaSceltaPastiPranzoUI


class InserisciSceltaPastiPranzoGiornoSuccessivoUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('InserisciSceltaPastiPranzoGiornoSuccessivo.ui',Path.cwd()), self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)

    def _btnAvantiClicked(self):
        self.widgetConfermaSceltaPastiPranzo = ConfermaSceltaPastiPranzoUI(self)
        self.widgetConfermaSceltaPastiPranzo.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = InserisciSceltaPastiPranzoGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())