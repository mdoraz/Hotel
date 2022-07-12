import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.HomeGestioneClientiUI import HomeGestioneClientiUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaClienteUI import RicercaClienteUI
from src.Gestori.GestoreFile import GestoreFile

class AggiungereClientiCheckInUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('AggiungereClientiCheckIn.ui', Path.cwd()), self)
        self.setMinimumSize(700,200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
        self.btnRegistraCliente.clicked.connect(self._btnRegistraClienteClicked)
        self.btnConfermaAggiungereClienti.clicked.connect(self._btnConfermaAggiungereClientiClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnRicercaClienteClicked(self):
        self.widgetRicercaCliente = RicercaClienteUI(self)
        self.widgetRicercaCliente.show()

    def _btnRegistraClienteClicked(self):
        self.tabwidgetHomeGestioneClienti = HomeGestioneClientiUI(self)
        self.tabwidgetHomeGestioneClienti.show()

    def _btnConfermaAggiungereClientiClicked(self):
        pass

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = AggiungereClientiCheckInUI()
    mainWidget.show()
    sys.exit(app.exec_())