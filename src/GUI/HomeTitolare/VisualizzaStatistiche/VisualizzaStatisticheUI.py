import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi



class VisualizzaStatisticheUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Titolare/GestioneStatistiche/VisualizzaStatistiche.ui', self)
        self.setMinimumSize(700,200)
        self.setFont(QtGui.QFont('Arial', 10))


    def _connectButtons(self):
        self.btnStatisticheColazioneInCamera.clicked.connect(self._btnStatisticheColazioneInCameraClicked)
        self.btnStatisticheNoleggioBici.clicked.connect(self._btnStatisticheNoleggioBiciClicked)
        self.btnStatisticheAssenzeDipendenti.clicked.connect(self._btnStatisticheAssenzeDipendentiClicked)
        self.btnStatisticheTipologiaSoggiorno.clicked.connect(self._btnStatisticheTipologiaSoggiornoClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)


    def btnStatisticheColazioneInCameraClicked(self):
        self.VisualizzaStatistiche.show()
        self.close()
    def btnStatisticheNoleggioBiciClicked(self):
        self.VisualizzaStatistiche.show()
        self.close()
    def btnStatisticheAssenzeDipendentiClicked(self):
        self.VisualizzaStatistiche.show()
        self.close()
    def btnStatisticheTipologiaSoggiornoClicked(self):
        self.VisualizzaStatistiche.show()
        self.close()
    def btnTornareIndietroClicked(self):
        self.VisualizzaStatistiche.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaStatisticheUI()
    mainWidget.show()
    sys.exit(app.exec_())




