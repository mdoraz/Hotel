import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.GestioneDipendenti.GestioneDipendentiUI import GestioneDipendentiUI
from src.GUI.HomeTitolare.RicercaEVisualizzaVacanze.VisualizzaRicercaVacanze import VisualizzaRicercaVacanzeUI
from src.GUI.HomeTitolare.VisualizzaDatiPersonali.datiTitolareUI import datiTitolareUI
from src.GUI.HomeTitolare.VisualizzaStatistiche.VisualizzaStatisticheUI import VisualizzaStatisticheUI


class HomeTitolareUI(QTabWidget):
    def __init__(self, previous : QWidget):
        super().__init__()
        self.page1 = QWidget()
        loadUi(GestoreFile.absolutePath('homeTitolare.ui', Path.cwd()), self.page1)
        self.addTab(self.page1, 'Home Titolare')
        self.setMinimumSize(500, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.page1.btnDatiPersonali.clicked.connect(self._btnDatiPersonaliClicked)
        self.page1.btnDipendenti.clicked.connect(self._btnDipendentiClicked)
        self.page1.btnStatistiche.clicked.connect(self._btnStatisticheClicked)
        self.page1.btnCucina.clicked.connect(self._btnCucinaClicked)
        self.page1.btnVacanze.clicked.connect(self._btnVacanzeClicked)
        self.page1.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnDatiPersonaliClicked(self):
        self.widgetdatiTitolare = datiTitolareUI()
        self.widgetdatiTitolare.show()

    def _btnDipendentiClicked(self):
        self.tabwidgetGestioneDipendenti = GestioneDipendentiUI(self)
        self.tabwidgetGestioneDipendenti.show()

    def _btnStatisticheClicked(self):
        self.widgetVisualizzaStatistiche = VisualizzaStatisticheUI(self)
        self.widgetVisualizzaStatistiche.show()
        self.close()  #per chiudere la home titolare

    def _btnCucinaClicked(self):
        pass

    def _btnVacanzeClicked(self):
        self.widgetVisualizzaRicercaVacanze = VisualizzaRicercaVacanzeUI()
        self.widgetVisualizzaRicercaVacanze.show()

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeTitolareUI(QWidget())
    mainWidget.show()
    sys.exit(app.exec_())
