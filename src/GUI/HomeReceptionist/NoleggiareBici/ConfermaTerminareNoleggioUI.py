import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class ConfermaTerminareNoleggioUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ConfermaTerminareNoleggio.ui', Path.cwd()), self)
        self.setMinimumSize(600,300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnPrelevaMulta.clicked.connect(self._btnPrelevaMultaClicked)
        self.btnTerminareNoleggio.clicked.connect(self._btnTerminareNoleggioClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)

    def _btnPrelevaMultaClicked(self):
        pass
    def _btnTerminareNoleggioClicked(self):
        #non funziona fino a quando non abbiamo prelevato la multa se la bici ha fatto ritardo
        pass
    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ConfermaTerminareNoleggioUI()
    mainWidget.show()
    sys.exit(app.exec_())
