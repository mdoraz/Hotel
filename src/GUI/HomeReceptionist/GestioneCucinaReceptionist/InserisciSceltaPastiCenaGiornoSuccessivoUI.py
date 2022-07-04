import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiCenaUI import ConfermaSceltaPastiCenaUI


class InserisciSceltaPastiCenaGiornoSuccessivoUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi(GestoreFile.absolutePath('InserisciSceltaPastiCenaGiornoSuccessivo.ui', Path.cwd()), self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)


    def _btnAvantiClicked(self):
        self.widgetConfermaSceltaPastiCena = ConfermaSceltaPastiCenaUI()
        self.widgetConfermaSceltaPastiCena.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = InserisciSceltaPastiCenaGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())