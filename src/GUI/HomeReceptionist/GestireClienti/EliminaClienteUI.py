import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class EliminaClienteUI(QTabWidget):
    def __init__(self):
        super().__init__()

        loadUi(GestoreFile.absolutePath('EliminaCliente.ui', Path.cwd()), self)
        self.setMinimumSize(600,400)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnEliminaCliente.clicked.connect(self._btnEliminaClienteClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)

    def _btnEliminaClienteClicked(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = EliminaClienteUI()
    mainWidget.show()
    sys.exit(app.exec_())