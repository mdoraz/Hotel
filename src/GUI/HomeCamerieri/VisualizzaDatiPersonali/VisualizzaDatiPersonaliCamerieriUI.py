import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile



class VisualizzaDatiPersonaliCamerieriUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('VisualizzaDatiPersonali.ui', Path.cwd()), self)
        self.setMinimumSize(600, 300)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

        self.lineEditLabelPairs = {
            self.lineeditNome: self.labelNome,
            self.lineeditCognome: self.labelCognome,
            self.lineeditLuogoDiNascitaProvincia: self.labelLuogoDiNascitaProvincia,
            self.lineeditTelefono: self.labelTelefono,
            self.lineeditIndirizzoEmail: self.labelIndirizzoEmail,
            self.lineeditIBAN: self.labelIBAN,
            self.lineeditTurnoDiLavoro: self.labelTurnoDiLavoro,
            self.lineeditRuolo: self.labelRuolo
        }

    def _connectButtons(self):
        self.btnOk.clicked.connect(self._btnOkClicked)

    def _btnOkClicked(self):
        self.close()
        self.previous.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaDatiPersonaliCamerieriUI()
    mainWidget.show()
    sys.exit(app.exec_())


