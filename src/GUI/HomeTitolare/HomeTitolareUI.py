import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.Attori.Amministratore import Amministratore
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.HomeTitolare.GestioneCucina.GestioneCucinaInterfacciaUI import GestioneCucinaInterfacciaUI
from src.GUI.HomeTitolare.GestioneDipendenti.GestioneDipendentiUI import GestioneDipendentiUI
from src.GUI.HomeTitolare.RicercaEVisualizzaVacanze.VisualizzaRicercaVacanze import VisualizzaRicercaVacanzeUI
from src.GUI.HomeTitolare.VisualizzaDatiPersonali.DatiTitolareUI import DatiTitolareUI
from src.GUI.HomeTitolare.VisualizzaStatistiche.VisualizzaStatisticheUI import VisualizzaStatisticheUI


class HomeTitolareUI(QTabWidget):
    def __init__(self, titolare : Amministratore, previous : QWidget):
        super().__init__()
        self.page1 = QWidget()
        loadUi(GestoreFile.absolutePath('homeTitolare.ui', Path.cwd()), self.page1)
        self.previous = previous
        self.titolare = titolare
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
        self.page1.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnDatiPersonaliClicked(self):
        self.close()
        self.widgetDatiTitolare = DatiTitolareUI(self.titolare, self)
        self.widgetDatiTitolare.show()

    def _btnDipendentiClicked(self):
        self.close()
        self.tabwidgetGestioneDipendenti = GestioneDipendentiUI(self)
        self.tabwidgetGestioneDipendenti.show()

    def _btnStatisticheClicked(self):
        self.close()
        self.widgetVisualizzaStatistiche = VisualizzaStatisticheUI(self)
        self.widgetVisualizzaStatistiche.show()


    def _btnCucinaClicked(self):
        self.close()
        self.widgetGestioneCucinaInterfaccia = GestioneCucinaInterfacciaUI(self)
        self.widgetGestioneCucinaInterfaccia.show()

    def _btnVacanzeClicked(self):
        self.close()
        self.widgetVisualizzaRicercaVacanze = VisualizzaRicercaVacanzeUI(self)
        self.widgetVisualizzaRicercaVacanze.show()

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    paths = GestoreFile.leggiJson(Path('paths.json'))
    titolare = GestoreFile.leggiPickle(Path(paths['titolare']))
    if isinstance(titolare, Amministratore):
        mainWidget = HomeTitolareUI(titolare, QWidget())
        mainWidget.show()
        sys.exit(app.exec_())
