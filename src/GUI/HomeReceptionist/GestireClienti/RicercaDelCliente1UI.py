import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.HomeReceptionist.GestireClienti.RicercaDelCliente2UI import RicercaDelCliente2UI
from src.Gestori.GestoreFile import GestoreFile

class RicercaDelCliente1UI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('RicercaDelCliente1.ui', Path.cwd()), self)
        self.setMinimumSize(350,100)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnNo.clicked.connect(self._btnNoClicked)

    def _btnAvantiClicked(self):
        self.close()
        self.widgetRicercaDelCliente2 = RicercaDelCliente2UI(self)
        self.widgetRicercaDelCliente2.show()

    def _btnNoClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaDelCliente1UI()
    mainWidget.show()
    sys.exit(app.exec_())