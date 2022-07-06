import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class RicercaDelCliente2UI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('RicercaDelCliente2.ui', Path.cwd()), self)
        self.setMinimumSize(400,200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnRicercaClienteClicked(self):
        pass

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaDelCliente2UI()
    mainWidget.show()
    sys.exit(app.exec_())