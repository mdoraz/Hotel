import sys
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RegistraClienteUI import RegistraClienteUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.VisualizzaClienteUI import VisualizzaClienteUI
from src.Gestori.GestoreFile import GestoreFile


class HomeGestioneClientiUI(QTabWidget):
    
    def __init__(self, previous : QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('HomeGestireUnCliente.ui', Path.cwd()), self)
        
        self.previous = previous

        self.tab1 = RegistraClienteUI()
        self.tab2 = VisualizzaClienteUI()
        self.tabwidgetInternal.addTab(self.tab1, 'Registra Cliente')
        self.tabwidgetInternal.addTab(self.tab2, 'Visualizza Cliente')
        self.tab1.btnIndietro.hide()
        
        self._connectButtons()
        self.msg = QMessageBox()  # per futuri messaggi


    def _connectButtons(self):
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)
        self.tab1.btnRegistraCliente.clicked.connect(self._btnRegistraClienteClicked)


    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

    
    def _btnRegistraClienteClicked(self):
        if self.tab1.fieldsFilled(self.tab1.lineeditLabelPairs) and not self.tab1.isClienteInSystem() and self.tab1.fieldsValid():
            self.tab1.salvaCliente()
            self._showMessage('Cliente registrato con successo!')
            self.tab1.clear()

    
    def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeGestioneClientiUI(QWidget())
    mainWidget.show()
    sys.exit(app.exec_())