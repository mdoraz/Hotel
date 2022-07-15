import sys
from datetime import date
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Dipendente import Dipendente
from src.Attori.Ruolo import Ruolo
from src.GUI.Dipendenti.HomeCamerieri.GestioneCucinaCamerieri.GestioneCucinaMenuCamerieriUI import \
    GestioneCucinaMenuCamerieriUI
from src.GUI.Dipendenti.VisualizzaDatiPersonaliDipendente.VisualizzaDatiPersonaliDipendenteUI import \
    VisualizzaDatiPersonaliDipendenteUI
from src.Gestori.GestoreFile import GestoreFile


class HomeCamerieriUI(QTabWidget):
    
    def __init__(self, cameriere : Dipendente, previous: QWidget):
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('HomeCamerieri.ui', Path.cwd()), self)

        self.previous = previous
        self.cameriere = cameriere
        self._connectButtons()

    
    def _connectButtons(self):
        self.btnVisualizzaDatiPersonaliCamerieri.clicked.connect(self._btnVisualizzaDatiPersonaliCamerieriClicked)
        self.btnGestisciCucinaCamerieri.clicked.connect(self._btnGestisciCucinaCamerieriClicked)
        self.btnTornareHomeHotelHomeCamerieri.clicked.connect(self._btnTornareHomeHotelHomeCamerieriClicked)

    
    def _btnVisualizzaDatiPersonaliCamerieriClicked(self):
        self.close()
        self.widgetVisualizzaDatiPersonaliDipendente = VisualizzaDatiPersonaliDipendenteUI(self.cameriere, self)
        self.widgetVisualizzaDatiPersonaliDipendente.show()

    
    def _btnGestisciCucinaCamerieriClicked(self):
        self.close()
        self.tabGestioneCucinaMenuCamerieri = GestioneCucinaMenuCamerieriUI(self)
        self.tabGestioneCucinaMenuCamerieri.show()

    
    def _btnTornareHomeHotelHomeCamerieriClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeCamerieriUI(Dipendente('Gervasa', 'Liguori', date(1981, 5, 7), 'Pistoia', 'gerva@hotmail.com', '374205234',
                                             '23432482402822523542', False, Ruolo.CAMERIERE, 'user', '12345678'), QWidget())
    mainWidget.show()
    sys.exit(app.exec_())
