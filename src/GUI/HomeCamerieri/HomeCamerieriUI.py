import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi



class HomeCamerieriUI(QTabWidget):
    def __init__(self, previous : QWidget = None):
        super().__init__()
        loadUi('ui/Cameriere/Home/HomeCamerieri.ui', self)
        self.setMinimumSize(600, 300)

        self.btnVisualizzaDatiPersonaliCamerieri.clicked.connect(self.btnVisualizzaDatiPersonaliCamerieriClicked)
        self.btnGestisciCucinaCamerieri.clicked.connect(self.btnTornareHomeHotelHomeCamerieriClicked)
        self.btnTornareHomeHotelHomeCamerieri.clicked.connect(self.btnTornareHomeHotelHomeCamerieriClicked)

    def btnVisualizzaDatiPersonaliCamerieriClicked(self):
        self.HomeCamerieri.show()
        self.close()

    def btnGestisciCucinaCamerieriClicked(self):
        self.HomeCamerieri.show()
        self.close()

    def btnTornareHomeHotelHomeCamerieriClicked(self):
        self.addTab(self.page1,'Home Page')
        self.removeTab(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeCamerieriUI()
    mainWidget.show()
    sys.exit(app.exec_())
