import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class VisualizzaDatiPersonaliDipendenteUI(QTabWidget):
    def __init__(self, dipendente, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('VisualizzaDatiPersonaliDipendente.ui',Path.cwd()), self)
        self.setMinimumSize(600, 400)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous
        self.dipendente = dipendente


    def _connectButtons(self):
        self.btnOk.clicked.connect(self._btnOkClicked)

    def _btnOkClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaDatiPersonaliDipendenteUI()
    mainWidget.show()
    sys.exit(app.exec_())