import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile



class VisualizzaStatisticheUI(QTabWidget):
    def __init__(self, previous : QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('VisualizzaStatistiche.ui', Path.cwd()), self)
        self.setMinimumSize(700,200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous


    def _connectButtons(self):
        self.btnStatisticheColazioneInCamera.clicked.connect(self._btnStatisticheColazioneInCameraClicked)
        self.btnStatisticheNoleggioBici.clicked.connect(self._btnStatisticheNoleggioBiciClicked)
        self.btnStatisticheAssenzeDipendenti.clicked.connect(self._btnStatisticheAssenzeDipendentiClicked)
        self.btnStatisticheTipologiaSoggiorno.clicked.connect(self._btnStatisticheTipologiaSoggiornoClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)


    def _btnStatisticheColazioneInCameraClicked(self):
        pass
    def _btnStatisticheNoleggioBiciClicked(self):
        pass
    def _btnStatisticheAssenzeDipendentiClicked(self):
        pass
    def _btnStatisticheTipologiaSoggiornoClicked(self):
        pass
    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaStatisticheUI()
    mainWidget.show()
    sys.exit(app.exec_())




