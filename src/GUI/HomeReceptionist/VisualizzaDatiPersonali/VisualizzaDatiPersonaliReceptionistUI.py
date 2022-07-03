import sys
from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class VisualizzaDatiPersonaliReceptionistUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Receptionist/VisualizzaDatiPersonali/VisualizzaDatiPersonali.ui', self)
        self.setMinimumSize(600, 400)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

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
        self.btnOk.clicked.connect(self.close)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaDatiPersonaliReceptionistUI()
    mainWidget.show()
    sys.exit(app.exec_())