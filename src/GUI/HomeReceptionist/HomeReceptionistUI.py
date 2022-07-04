import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeReceptionist.GestioneCucinaReceptionist.GestioneCucinaMenuReceptionistUI import \
    GestioneCucinaMenuReceptionistUI
from src.GUI.HomeReceptionist.VisualizzaDatiPersonali.VisualizzaDatiPersonaliReceptionistUI import \
    VisualizzaDatiPersonaliReceptionistUI


class HomeReceptionistUI(QTabWidget):
    def __init__(self,previous : QWidget):
        super().__init__()
        loadUi('ui/Receptionist/Home/HomeReceptionist.ui', self)
        self.setMinimumSize(600, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnVisualizzaDatiPersonali.clicked.connect(self._btnVisualizzaDatiPersonaliClicked)
        self.btnGestireClienti.clicked.connect(self._btnGestireClientiClicked)
        self.btnGestireNoleggioBici.clicked.connect(self._btnGestireNoleggioBiciClicked)
        self.btnGestireLaVacanza.clicked.connect(self._btnGestireLaVacanzaClicked)
        self.btnInserisciSceltaPastiPranzoCena.clicked.connect(self._btnInserisciSceltaPastiPranzoCenaClicked)
        self.btnTornareHomeHotel.clicked.connect(self._TornareHomeHotelClicked)

    def _btnVisualizzaDatiPersonaliClicked(self):
        self.widgetVisualizzaDatiPersonali = VisualizzaDatiPersonaliReceptionistUI()
        self.widgetVisualizzaDatiPersonali.show()

    def _btnGestireClientiClicked(self):
        pass

    def _btnGestireNoleggioBiciClicked(self):
        pass

    def _btnGestireLaVacanzaClicked(self):
        pass

    def _btnInserisciSceltaPastiPranzoCenaClicked(self):
        self.tabGestioneCucinaMenuReceptionist = GestioneCucinaMenuReceptionistUI()
        self.tabGestioneCucinaMenuReceptionist.show()
    def _TornareHomeHotelClicked(self):
        self.close()
        self.previous.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())