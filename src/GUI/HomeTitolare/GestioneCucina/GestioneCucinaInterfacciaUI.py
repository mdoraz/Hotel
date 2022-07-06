import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.HomeTitolare.GestioneCucina.ModificaMenuColazioneInCameraUI import ModificaMenuColazioneInCameraUI
from src.GUI.HomeTitolare.GestioneCucina.ModificaMenuUI import ModificaMenuUI
from src.Gestori.GestoreFile import GestoreFile


class GestioneCucinaInterfacciaUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('GestioneCucinaInterfaccia.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnModificaMenuColazioneInCamera.clicked.connect(self._btnModificaMenuColazioneInCameraClicked)
        self.btnModificaMenuPranzo.clicked.connect(self._btnModificaMenuPranzoClicked)
        self.btnModificaMenuCena.clicked.connect(self._btnModificaMenuCenaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self._btnTornarePaginaPrecedente_2Clicked)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self._btnTornarePaginaPrecedente_3Clicked)

    def _btnModificaMenuColazioneInCameraClicked(self):
        self.close()
        self.widgetModificaMenuColazioneInCamera = ModificaMenuColazioneInCameraUI(self)
        self.widgetModificaMenuColazioneInCamera.show()

    def _btnModificaMenuPranzoClicked(self):
        self.close()
        self.widgetModificaMenu = ModificaMenuUI(self)
        self.widgetModificaMenu.show()

    def _btnModificaMenuCenaClicked(self):
        self.close()
        self.widgetModificaMenu = ModificaMenuUI(self)
        self.widgetModificaMenu.show()

    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

    def _btnTornarePaginaPrecedente_2Clicked(self):
        self.close()
        self.previous.show()

    def _btnTornarePaginaPrecedente_3Clicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = GestioneCucinaInterfacciaUI()
    mainWidget.show()
    sys.exit(app.exec_())