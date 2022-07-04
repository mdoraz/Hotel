import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.InserisciSceltaPastiCenaGiornoSuccessivoUI import \
    InserisciSceltaPastiCenaGiornoSuccessivoUI
from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.InserisciSceltaPastiPranzoGiornoSuccessivoUI import \
    InserisciSceltaPastiPranzoGiornoSuccessivoUI


class GestioneCucinaMenuReceptionistUI(QTabWidget):
    def __init__(self, previous: QWidget ):
        super().__init__()
        loadUi(GestoreFile.absolutePath('GestioneCucina.ui', Path.cwd()), self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self.previous = previous
        self._connectButtons()

    def _connectButtons(self):
        self.btnInserisciSceltaPastiPranzo.clicked.connect(self._btnInserisciSceltaPastiPranzoClicked)
        self.btnInserisciSceltaPastiCena.clicked.connect(self._btnInserisciSceltaPastiCenaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self._btnTornarePaginaPrecedente_2Clicked)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self._btnTornarePaginaPrecedente_3Clicked)

    def _btnInserisciSceltaPastiPranzoClicked(self):
        self.widgetInserisciSceltaPastiPranzoGiornoSuccessivo = InserisciSceltaPastiPranzoGiornoSuccessivoUI()
        self.widgetInserisciSceltaPastiPranzoGiornoSuccessivo.show()
    def _btnInserisciSceltaPastiCenaClicked(self):
        self.widgetInserisciSceltaPastiCenaGiornoSuccessivo = InserisciSceltaPastiCenaGiornoSuccessivoUI()
        self.widgetInserisciSceltaPastiCenaGiornoSuccessivo.show()

    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()
    def _btnTornarePaginaPrecedente_2Clicked(self):
        self.close()
        self.previous.show()
    def _btnTornarePaginaPrecedente_3Clicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = GestioneCucinaMenuReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())