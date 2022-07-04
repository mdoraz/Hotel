import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.HomeTitolare.RicercaEVisualizzaVacanze.RicercaVacanzaTitolareUI import RicercaVacanzaTitolareUI


class VisualizzaRicercaVacanzeUI(QTabWidget):
    def __init__(self):
        super().__init__()

        loadUi(GestoreFile.absolutePath('VisualizzaRicercaVacanze.ui', Path.cwd()), self)
        self.setMinimumSize(1000,600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnRicercaVacanza.clicked.connect(self._btnRicercaVacanzaClicked)
        self.btnTornareHomeTitolare.clicked.connect(self.close)

    def _btnRicercaVacanzaClicked(self):
        self.widgetRicercaVacanzaTitolare = RicercaVacanzaTitolareUI()
        self.widgetRicercaVacanzaTitolare.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaRicercaVacanzeUI()
    mainWidget.show()
    sys.exit(app.exec_())

