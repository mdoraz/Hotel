import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile


class AvvisoPiattiModificatiUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('AvvisoPiattiModificati.ui', Path.cwd()), self)
        self.setMinimumSize(600, 200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnOk.clicked.connect(self._btnOkClicked)

    def _btnOkClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = AvvisoPiattiModificatiUI()
    mainWidget.show()
    sys.exit(app.exec_())