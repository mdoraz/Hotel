import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiCenaUI import ConfermaSceltaPastiCenaUI


class InserisciSceltaPastiCenaGiornoSuccessivoUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/InserisciSceltaPastiPranzoCena/InserisciSceltaPastiCenaGiornoSuccessivo.ui', self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnTornarePaginaPrecedenteClicked(self):
        pass

    def _btnAvantiClicked(self):
        self.widgetConfermaSceltaPastiCena = ConfermaSceltaPastiCenaUI()
        self.widgetConfermaSceltaPastiCena.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = InserisciSceltaPastiCenaGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())