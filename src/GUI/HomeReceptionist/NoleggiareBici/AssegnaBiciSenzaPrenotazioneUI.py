import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile


class AssegnaBiciSenzaPrenotazioneUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('AssegnaBiciSenzaPrenotazione.ui', Path.cwd()), self)
        self.setMinimumSize(600,300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnAssegnaBiciSenzaPrenotazione.clicked.connect(self._btnAssegnaBiciSenzaPrenotazioneClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnAssegnaBiciSenzaPrenotazioneClicked(self):
        pass
    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = AssegnaBiciSenzaPrenotazioneUI()
    mainWidget.show()
    sys.exit(app.exec_())