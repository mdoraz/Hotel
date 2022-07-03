import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class datiTitolareUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Titolare/VisualizzaDatiPersonali/datiTitolare.ui',self)
        self.setMinimumSize(500, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnIndietro.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = datiTitolareUI()
    mainWidget.show()
    sys.exit(app.exec_())