import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.HomeTitolare.GestioneCucina.AvvisoPiattiModificatiUI import AvvisoPiattiModificatiUI
from src.Gestori.GestoreFile import GestoreFile


class ModificaMenuUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ModificaMenu.ui', Path.cwd()), self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnSiConfermaModifiche.clicked.connect(self._btnSiConfermaModificheClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnSiConfermaModificheClicked(self):
        self.close()
        self.widgetAvvisoPiattiModificati = AvvisoPiattiModificatiUI(self)
        self.widgetAvvisoPiattiModificati.show()
    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ModificaMenuUI()
    mainWidget.show()
    sys.exit(app.exec_())