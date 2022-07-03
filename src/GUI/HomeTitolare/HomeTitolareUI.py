import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi



class HomeTitolareUI(QTabWidget):
    def __init__(self):
        super().__init__()
        self.page1 = QWidget()
        loadUi('ui/Titolare/Home/homeTitolare.ui', self.page1)
        self.addTab(self.page1, 'Home Titolare')
        self.setMinimumSize(500, 300)
        self.setFont(QtGui.QFont('Arial', 10))

    def _connectButtons(self):
        self.page1.btnDatiPersonali.clicked.connect(self._btnDatiPersonaliClicked)
        self.page1.btnDipendenti.clicked.connect(self._btnDipendentiClicked)
        self.page1.btnStatistiche.clicked.connect(self._btnStatisticheClicked)
        self.page1.btnCucina.clicked.connect(self._btnCucinaClicked)
        self.page1.btnVacanze.clicked.connect(self._btnVacanzeClicked)

    def btnDatiPersonaliClicked(self):
        self.HomeTitolare.show()
        self.close()

    def btnDipendentiClicked(self):
        self.HomeTitolare.show()
        self.close()

    def btnStatisticheClicked(self):
        self.HomeTitolare.show()
        self.close()

    def btnCucinaClicked(self):
        self.HomeTitolare.show()
        self.close()

    def btnVacanzeClicked(self):
        self.HomeTitolare.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeTitolareUI()
    mainWidget.show()
    sys.exit(app.exec_())
