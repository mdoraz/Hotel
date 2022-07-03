import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeTitolare.VisualizzaDatiPersonali.datiTitolareUI import datiTitolareUI
from src.GUI.HomeTitolare.VisualizzaStatistiche.VisualizzaStatisticheUI import VisualizzaStatisticheUI


class HomeTitolareUI(QTabWidget):
    def __init__(self):
        super().__init__()
        self.page1 = QWidget()
        loadUi('ui/Titolare/Home/homeTitolare.ui', self.page1)
        self.addTab(self.page1, 'Home Titolare')
        self.setMinimumSize(500, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.page1.btnDatiPersonali.clicked.connect(self._btnDatiPersonaliClicked)
        self.page1.btnDipendenti.clicked.connect(self._btnDipendentiClicked)
        self.page1.btnStatistiche.clicked.connect(self._btnStatisticheClicked)
        self.page1.btnCucina.clicked.connect(self._btnCucinaClicked)
        self.page1.btnVacanze.clicked.connect(self._btnVacanzeClicked)
        self.page1.btnIndietro.clicked.connect(self.close)

    def _btnDatiPersonaliClicked(self):
        self.widgetdatiTitolare = datiTitolareUI()
        self.widgetdatiTitolare.show()

    def _btnDipendentiClicked(self):
        pass

    def _btnStatisticheClicked(self):
        self.widgetVisualizzaStatistiche = VisualizzaStatisticheUI()
        self.widgetVisualizzaStatistiche.show()

    def _btnCucinaClicked(self):
        pass

    def _btnVacanzeClicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeTitolareUI()
    mainWidget.show()
    sys.exit(app.exec_())
