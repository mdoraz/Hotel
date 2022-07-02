import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi




class VisualizzaDatiPersonaliCamerieriUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Cameriere/VisualizzaDatiPersonali/VisualizzaDatiPersonali.ui', self)
        self.setMinimumSize(600, 300)
        self.setFont(QtGui.QFont('Arial', 10))

        self.lineEditLabelPairs = {
            self.lineEditNomeCamerieri: self.labelNomeCamerieri,
            self.lineEditCognomeCamerieri: self.labelCognomeCamerieri,
            self.lineEditLuogoDiNascitaProvinciaCamerieri: self.labelLuogoDiNascitaCamerieri,
            self.lineEditTelefonoCamerieri: self.labelTelefonoCamerieri,
            self.lineEditIndirizzoEmailCamerieri: self.labelIndirizzoEmailCamerieri,
            self.lineEditIBANCamerieri: self.labelIBANCamerieri,
            self.lineEditTurnoDiLavoroCamerieri: self.labelTurnoDiLavoroCamerieri,
            self.lineEditRuoloCamerieri: self.labelRuoloCamerieri
        }

    def _connectButtons(self):
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)

    def _btnTornareIndietroClicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaDatiPersonaliCamerieriUI()
    mainWidget.show()
    sys.exit(app.exec_())



