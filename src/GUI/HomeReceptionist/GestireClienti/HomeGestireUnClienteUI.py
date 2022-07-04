import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.HomeReceptionist.GestireClienti.EliminaClienteUI import EliminaClienteUI
from src.GUI.HomeReceptionist.GestireClienti.ModificaClienteUI import ModificaClienteUI
from src.GUI.HomeReceptionist.GestireClienti.RicercaDelCliente1UI import RicercaDelCliente1UI
from src.Gestori.GestoreFile import GestoreFile


class HomeGestireUnClienteUI(QTabWidget):
    def __init__(self, previous : QWidget ):
        super().__init__()

        loadUi(GestoreFile.absolutePath('HomeGestireUnCliente.ui', Path.cwd()), self)
        self.setMinimumSize(600,400)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous
        self.msg = QMessageBox()  # per futuri messaggi


    def _connectButtons(self):
        self.btnNo.clicked.connect(self._btnNoClicked)
        self.btnHelpAsterisco.clicked.connect(self._btnHelpAsteriscoClicked)
        self.btnTornareHomeReceptionist.clicked.connect(self._btnTornareHomeReceptionistClicked)
        self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
        self.btnModificaClienteRicercato.clicked.connect(self._btnModificaClienteRicercatoClicked)
        self.btnEliminaClienteRicercato.clicked.connect(self._btnEliminaClienteRicercatoClicked)

    def _btnNoClicked(self):
        pass

    def _btnHelpAsteriscoClicked(self):
        self._showMessage("L'asterisco accanto ad ogni campo vuol dire che la registrazione non può essere effettuata se prima tutti i campi non sono stati inseriti.", QMessageBox.Icon.Warning)

    def _btnRicercaClienteClicked(self):
        self.widgetRicercaDelCliente1 = RicercaDelCliente1UI()
        self.widgetRicercaDelCliente1.show()

    def _btnModificaClienteRicercatoClicked(self):
        self.widgetModificaCliente = ModificaClienteUI()
        self.widgetModificaCliente.show()

    def _btnEliminaClienteRicercatoClicked(self):
        self.widgetEliminaCliente = EliminaClienteUI()
        self.widgetEliminaCliente.show()

    def _btnTornareHomeReceptionistClicked(self):
        self.close()
        self.previous.show()

    def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeGestireUnClienteUI()
    mainWidget.show()
    sys.exit(app.exec_())