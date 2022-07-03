import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

class RicercaVacanzaTitolareUI(QTabWidget):
    def __init__(self):
        super().__init__()

        loadUi('ui/Titolare/RicercaEVisualizzaVacanze/RicercaVacanzaTitolare.ui', self)
        self.setMinimumSize(400,200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnCercaVacanza.clicked.connect(self._btnCercaVacanzaClicked)

    def _btnCercaVacanzaClicked(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaVacanzaTitolareUI()
    mainWidget.show()
    sys.exit(app.exec_())
