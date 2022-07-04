import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.HomePageProgramma.LoginProgrammaUI import LoginProgrammaUI



class HomePageUI(QTabWidget):
    def __init__(self):
        super().__init__()
        self.page1 = QWidget()
        loadUi(GestoreFile.absolutePath('homePage.ui', Path.cwd()), self.page1)
        self.addTab(self.page1, 'Home Programma')
        self.setMinimumSize(500,300)

        self.page1.btnDipendente.clicked.connect(self.btnDipendenteClicked)
        self.page1.btnTitolare.clicked.connect(self.btnTitolareClicked)

    def btnDipendenteClicked(self):
        dictyonary = GestoreFile.leggiJson(Path('paths.json'))
        self.loginDipendente = LoginProgrammaUI(self, Path(dictyonary['dipendenti']))
        self.loginDipendente.show()
        self.close()

    def btnTitolareClicked(self):
        dictyonary = GestoreFile.leggiJson(Path('paths.json'))
        self. loginTitolare = LoginProgrammaUI(self, Path(dictyonary['titolare']))
        self.loginTitolare.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomePageUI()
    mainWidget.show()
    sys.exit(app.exec_())