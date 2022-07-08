import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class SelezionaCameraUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('SelezionaCamera.ui', Path.cwd()), self)
        self.setMinimumSize(600,300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaCamerePeriodoSelezionato.clicked.connect(self._btnRicercaCamerePeriodoSelezionatoClicked)
        self.btnScegliereCameraSelezionata.clicked.connect(self._btnScegliereCameraSelezionataClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)

    def _btnRicercaCamerePeriodoSelezionatoClicked(self):
        pass
    def _btnScegliereCameraSelezionataClicked(self):
        pass
    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = SelezionaCameraUI()
    mainWidget.show()
    sys.exit(app.exec_())