import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class HomeReceptionistUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/Home/HomeReceptionist.ui', self)
        self.setMinimumSize(600, 300)
        self.setFont(QtGui.QFont('Arial', 10))

    def connectButtons(self):
        self.btnVisualizzaDatiPersonali.clicked.connect(self._btnVisualizzaDatiPersonaliClicked)
        self.btnGestireClienti.clicked.connect(self._btnGestireClientiClicked)
        self.btnGestireNoleggioBici.clicked.connect(self._btnGestireNoleggioBiciClicked)
        self.btnGestireLaVacanza.clicked.connect(self._btnGestireLaVacanzaClicked)
        self.btnInserisciSceltaPastiPranzoCena.clicked.connect(self._btnInserisciSceltaPastiPranzoCenaClicked)
        self.btnTornareHomeHotel.clicked.connect(self._btnTornareHomeHotelClicked)

    def btnVisualizzaDatiPersonaliClicked(self):
        self.HomeReceptionist.show()
        self.close()

    def btnGestireClientiClicked(self):
        self.HomeReceptionist.show()
        self.close()

    def btnGestireNoleggioBiciClicked(self):
        self.HomeReceptionist.show()
        self.close()

    def btnGestireLaVacanzaClicked(self):
        self.HomeReceptionist.show()
        self.close()

    def btnInserisciSceltaPastiPranzoCenaClicked(self):
        self.HomeReceptionist.show()
        self.close()

    def btnTornareHomeHotelClicked(self):
        self.HomeReceptionist.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())