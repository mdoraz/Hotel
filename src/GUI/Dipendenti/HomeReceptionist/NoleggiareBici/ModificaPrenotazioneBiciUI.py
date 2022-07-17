"""import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile


class ModificaPrenotazioneBiciUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ModificaPrenotazioneBici.ui', Path.cwd()), self)
        self.setMinimumSize(600,300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnConfermaModifiche.clicked.connect(self._btnConfermaModificheClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnConfermaModificheClicked(self):
        pass
    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ModificaPrenotazioneBiciUI()
    mainWidget.show()
    sys.exit(app.exec_())"""