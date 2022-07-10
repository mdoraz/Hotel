import sys
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.GUIUtils import GUIUtils


class RicercaDelClienteUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('RicercaDelCliente.ui', Path.cwd()), self)
        
        self.previous = previous
        self._setValidators()
        self._connectButtons()

    
    def _setValidators(self):
        self.lineeditNome.setValidator(GUIUtils.validators['soloLettere'])
        self.lineeditCognome.setValidator(GUIUtils.validators['soloLettere'])
        self.lineeditID.setValidator(GUIUtils.validators['soloNumeri'])
    

    def _connectButtons(self):
        self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)


    def _btnRicercaClienteClicked(self):
        pass


    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaDelClienteUI(QWidget())
    mainWidget.show()
    sys.exit(app.exec_())