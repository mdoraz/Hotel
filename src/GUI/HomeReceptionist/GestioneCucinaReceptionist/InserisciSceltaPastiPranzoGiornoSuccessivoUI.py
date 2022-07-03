import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiPranzoUI import ConfermaSceltaPastiPranzoUI


class InserisciSceltaPastiPranzoGiornoSuccessivoUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/InserisciSceltaPastiPranzoCena/InserisciSceltaPastiPranzoGiornoSuccessivo.ui', self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnTornarePaginaPrecedenteClicked(self):
        pass
    def _btnAvantiClicked(self):
        self.widgetConfermaSceltaPastiPranzo = ConfermaSceltaPastiPranzoUI()
        self.widgetConfermaSceltaPastiPranzo.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = InserisciSceltaPastiPranzoGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())