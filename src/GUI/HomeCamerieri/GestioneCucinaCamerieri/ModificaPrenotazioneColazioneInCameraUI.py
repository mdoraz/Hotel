import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class ModificaPrenotazioneColazioneInCameraUI(QTabWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/Cameriere/GestisciCucina/ModificaPrenotazioneColazioneInCamera.ui', self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()

    def _connectButtons(self):
        self.btnConfermaModifiche.clicked.connect(self._btnConfermaModificheClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)

    def _btnConfermaModificheClicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ModificaPrenotazioneColazioneInCameraUI()
    mainWidget.show()
    sys.exit(app.exec_())