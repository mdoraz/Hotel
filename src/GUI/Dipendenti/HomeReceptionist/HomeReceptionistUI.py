import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.HomeGestioneVacanzeUI import HomeGestioneVacanzeUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.HomeGestireUnClienteUI import HomeGestireUnClienteUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.HomeNoleggiareUnaBiciUI import HomeNoleggiareUnaBiciUI
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.GestioneCucinaMenuReceptionistUI import \
    GestioneCucinaMenuReceptionistUI
from src.GUI.Dipendenti.VisualizzaDatiPersonaliDipendente.VisualizzaDatiPersonaliDipendenteUI import \
     VisualizzaDatiPersonaliDipendenteUI


class HomeReceptionistUI(QTabWidget):
    def __init__(self, receptionist, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('HomeReceptionist.ui', Path.cwd()), self)
        self.setMinimumSize(600, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous
        self.receptionist = receptionist

    def _connectButtons(self):
        self.btnDatiPersonali.clicked.connect(self._btnDatiPersonaliClicked)
        self.btnClienti.clicked.connect(self._btnClientiClicked)
        self.btnNoleggiBici.clicked.connect(self._btnNoleggiBiciClicked)
        self.btnVacanza.clicked.connect(self._btnVacanzaClicked)
        self.btnInserisciSceltaPasti.clicked.connect(self._btnInserisciSceltaPastiClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnDatiPersonaliClicked(self):
        self.close()
        self.widgetVisualizzaDatiPersonaliDipendente = VisualizzaDatiPersonaliDipendenteUI(self.receptionist, self)
        self.widgetVisualizzaDatiPersonaliDipendente.show()

    def _btnClientiClicked(self):
        self.close()
        self.tabHomeGestireUnCliente = HomeGestireUnClienteUI(self)
        self.tabHomeGestireUnCliente.show()

    def _btnNoleggiBiciClicked(self):
        self.close()
        self.widgetHomeNoleggiareUnaBici = HomeNoleggiareUnaBiciUI(self)
        self.widgetHomeNoleggiareUnaBici.show()

    def _btnVacanzaClicked(self):
        self.close()
        self.widgetHomegestioneVacanze = HomeGestioneVacanzeUI(self)
        self.widgetHomegestioneVacanze.show()

    def _btnInserisciSceltaPastiClicked(self):
        self.close()
        self.tabGestioneCucinaMenuReceptionist = GestioneCucinaMenuReceptionistUI(self)
        self.tabGestioneCucinaMenuReceptionist.show()
    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())