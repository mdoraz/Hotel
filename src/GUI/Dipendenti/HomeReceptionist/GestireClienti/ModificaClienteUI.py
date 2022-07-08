import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile


class ModificaClienteUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('ModificaCliente.ui', Path.cwd()), self)
        self.setMinimumSize(600,400)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnSalvaModifiche.clicked.connect(self._btnSalvaModificheClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)

    def _btnSalvaModificheClicked(self):
        pass

    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ModificaClienteUI()
    mainWidget.show()
    sys.exit(app.exec_())