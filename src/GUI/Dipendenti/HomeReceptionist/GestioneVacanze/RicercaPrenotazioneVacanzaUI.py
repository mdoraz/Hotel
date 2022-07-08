import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaDelCliente1UI import RicercaDelCliente1UI
from src.Gestori.GestoreFile import GestoreFile

class RicercaPrenotazioneVacanzaUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('RicercaPrenotazioneVacanza.ui', Path.cwd()), self)
        self.setMinimumSize(600,300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
        self.btnOk.clicked.connect(self._btnOkClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)

    def _btnRicercaClienteClicked(self):
        self.close()
        self.widgetRicercaDelCliente1 = RicercaDelCliente1UI(self)
        self.widgetRicercaDelCliente1.show()

    def _btnOkClicked(self):
        pass

    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaPrenotazioneVacanzaUI()
    mainWidget.show()
    sys.exit(app.exec_())