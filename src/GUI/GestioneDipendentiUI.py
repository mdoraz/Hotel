import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

class GestioneDipendentiUI(QTabWidget):
	
	def __init__(self):
		super().__init__()

		loadUi('ui/Titolare/gestioneDipendenti.ui', self)




if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = GestioneDipendentiUI()
	mainWidget.show()
	sys.exit(app.exec_())