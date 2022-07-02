import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.HomeCamerieri.VisualizzaDatiPersonali.VisualizzaDatiPersonaliCamerieriUI import \
    VisualizzaDatiPersonaliCamerieriUI


class HomeCamerieriUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Cameriere/Home/HomeCamerieri.ui', self)
        self.setMinimumSize(600, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnVisualizzaDatiPersonaliCamerieri.clicked.connect(self._btnVisualizzaDatiPersonaliCamerieriClicked)
        self.btnGestisciCucinaCamerieri.clicked.connect(self._btnTornareHomeHotelHomeCamerieriClicked)
        self.btnTornareHomeHotelHomeCamerieri.clicked.connect(self._btnTornareHomeHotelHomeCamerieriClicked)

    def _btnVisualizzaDatiPersonaliCamerieriClicked(self):
        self.widgetVisualizzaDatiPersonali = VisualizzaDatiPersonaliCamerieriUI()
        self.widgetVisualizzaDatiPersonali.show()

    def _btnGestisciCucinaCamerieriClicked(self):
        pass

    def _btnTornareHomeHotelHomeCamerieriClicked(self):
       pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeCamerieriUI()
    mainWidget.show()
    sys.exit(app.exec_())
