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
        self.btnVisualizzaDatiPersonali.clicked.connect(self._btnVisualizzaDatiPersonaliClicked)
        self.btnGestireClienti.clicked.connect(self._btnGestireClientiClicked)
        self.btnGestireNoleggioBici.clicked.connect(self._btnGestireNoleggioBiciClicked)
        self.btnGestireLaVacanza.clicked.connect(self._btnGestireLaVacanzaClicked)
        self.btnInserisciSceltaPastiPranzoCena.clicked.connect(self._btnInserisciSceltaPastiPranzoCenaClicked)
        self.btnTornareHomeHotel.clicked.connect(self._TornareHomeHotelClicked)

    def _btnVisualizzaDatiPersonaliClicked(self):
        self.close()
        self.widgetVisualizzaDatiPersonaliDipendente = VisualizzaDatiPersonaliDipendenteUI(self.receptionist, self)
        self.widgetVisualizzaDatiPersonaliDipendente.show()

    def _btnGestireClientiClicked(self):
        self.close()
        self.tabHomeGestireUnCliente = HomeGestireUnClienteUI(self)
        self.tabHomeGestireUnCliente.show()

    def _btnGestireNoleggioBiciClicked(self):
        self.close()
        self.widgetHomeNoleggiareUnaBici = HomeNoleggiareUnaBiciUI(self)
        self.widgetHomeNoleggiareUnaBici.show()

    def _btnGestireLaVacanzaClicked(self):
        self.close()
        self.widgetHomegestioneVacanze = HomeGestioneVacanzeUI(self)
        self.widgetHomegestioneVacanze.show()

    def _btnInserisciSceltaPastiPranzoCenaClicked(self):
        self.close()
        self.tabGestioneCucinaMenuReceptionist = GestioneCucinaMenuReceptionistUI(self)
        self.tabGestioneCucinaMenuReceptionist.show()
    def _TornareHomeHotelClicked(self):
        self.close()
        self.previous.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())