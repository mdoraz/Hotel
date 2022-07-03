import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.InserisciSceltaPastiCenaGiornoSuccessivoUI import \
    InserisciSceltaPastiCenaGiornoSuccessivoUI
from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.InserisciSceltaPastiPranzoGiornoSuccessivoUI import \
    InserisciSceltaPastiPranzoGiornoSuccessivoUI


class GestioneCucinaMenuReceptionistUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/InserisciSceltaPastiPranzoCena/GestioneCucina.ui', self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnInserisciSceltaPastiPranzo.clicked.connect(self._btnInserisciSceltaPastiPranzoClicked)
        self.btnInserisciSceltaPastiCena.clicked.connect(self._btnInserisciSceltaPastiCenaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self.close)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self.close)

    def _btnInserisciSceltaPastiPranzoClicked(self):
        self.widgetInserisciSceltaPastiPranzoGiornoSuccessivo = InserisciSceltaPastiPranzoGiornoSuccessivoUI()
        self.widgetInserisciSceltaPastiPranzoGiornoSuccessivo.show()
    def _btnInserisciSceltaPastiCenaClicked(self):
        self.widgetInserisciSceltaPastiCenaGiornoSuccessivo = InserisciSceltaPastiCenaGiornoSuccessivoUI()
        self.widgetInserisciSceltaPastiCenaGiornoSuccessivo.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = GestioneCucinaMenuReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())