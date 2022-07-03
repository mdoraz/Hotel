import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class ConfermaSceltaPastiCenaUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/InserisciSceltaPastiPranzoCena/ConfermaSceltaPastiCena.ui', self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnConfermaPrenotazione.clicked.connect(self._btnConfermaPrenotazioneClicked)
        self.btnIndietro.clicked.connect(self.close)

    def _btnConfermaPrenotazioneClicked(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ConfermaSceltaPastiCenaUI()
    mainWidget.show()
    sys.exit(app.exec_())