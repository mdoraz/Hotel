import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.SelezionaCameraUI import SelezionaCameraUI
from src.Gestori.GestoreFile import GestoreFile

class ModificaPrenotazioneVacanzaUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ModificaPrenotazioneVacanza.ui', Path.cwd()), self)
        self.setMinimumSize(700,250)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnConfermaModifiche.clicked.connect(self._btnConfermaModificheClicked)
        self.btnModificaCameraPeriodoSoggiorno.clicked.connect(self._btnModificaCameraPeriodoSoggiornoClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)

    def _btnConfermaModificheClicked(self):
        pass

    def _btnModificaCameraPeriodoSoggiornoClicked(self):
        self.widgetSelezionaCamera = SelezionaCameraUI(self)
        self.widgetSelezionaCamera.show()

    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ModificaPrenotazioneVacanzaUI()
    mainWidget.show()
    sys.exit(app.exec_())