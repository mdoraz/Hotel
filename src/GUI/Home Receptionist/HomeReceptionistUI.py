import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class HomeReceptionistUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/Home/HomeReceptionist.ui', self)
        self.setMinimumSize(600, 300)
        self.btnVisualizzaDatiPersonali.clicked.connect(self.btnVisualizzaDatiPersonaliClicked)
        self.btnGestireClienti.clicked.connect(self.btnGestireClientiClicked)
        self.btnGestireNoleggioBici.clicked.connect(self.btnGestireNoleggioBiciClicked)
        self.btnGestireLaVacanza.clicked.connect(self.btnGestireLaVacanzaClicked)
        self.btnInserisciSceltaPastiPranzoCena.clicked.connect(self.btnInserisciSceltaPastiPranzoCenaClicked)
        self.btnTornareHomeHotel.clicked.connect(self.btnTornareHomeHotelClicked)

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