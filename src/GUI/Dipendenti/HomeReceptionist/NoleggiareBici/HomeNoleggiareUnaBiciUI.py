import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.AssegnaBiciSenzaPrenotazioneUI import AssegnaBiciSenzaPrenotazioneUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.RiconsegnaBiciUI import RiconsegnaBiciUI


class HomeNoleggiareUnaBiciUI(QTabWidget):
	
	def __init__(self, previous: QWidget):
		super().__init__()
		
		self.setWindowTitle('Struttura Alberghiera')
		self.setMinimumSize(480, 530)
		self.setFont(QtGui.QFont('Arial', 10))

		self.tab1 = AssegnaBiciSenzaPrenotazioneUI(previous)
		self.tab2 = RiconsegnaBiciUI(previous)

		self.addTab(self.tab1, 'Assegna Bici')
		self.addTab(self.tab2, 'Riconsegna Bici')

		self.tab1.btnIndietroClicked.connect(self.close) # type: ignore
		self.tab2.btnIndietroClicked.connect(self.close) # type: ignore
		self.tab2.biciRiconsegnate.connect(self.tab1.aggiungiBici)

		self.msg = QMessageBox()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = HomeNoleggiareUnaBiciUI(QWidget())
	mainWidget.show()
	sys.exit(app.exec_())