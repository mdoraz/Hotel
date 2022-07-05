import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
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
        pass

    def _btnModificaMenuPranzoClicked(self):
        pass

    def _btnModificaMenuCenaClicked(self):
        pass

    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()

    def _btnTornarePaginaPrecedente_2Clicked(self):
        self.close()
        self.previous.show()

    def _btnTornarePaginaPrecedente_3Clicked(self):
        self.close()
        self.previous.show()
