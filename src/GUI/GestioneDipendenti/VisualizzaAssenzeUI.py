from datetime import date
from pathlib import Path
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

from src.Attori.Dipendente import Dipendente
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.customQtClasses import myListWidgetItem

class VisualizzaAssenzeUI(QWidget):

	def __init__(self, dipendente : Dipendente, parent : QWidget = None): # type: ignore
		super().__init__(parent)

		loadUi(GestoreFile.absolutePath('visualizzaAssenze.ui', Path.cwd()), self)

		self.dipendente = dipendente

		self.labelIntestazione.setText(f'Assenze di {self.dipendente.getNome()} {self.dipendente.getCognome()}')
		self._fillListWidget()
		self._setUpAndConnectButtons()

		self.msg = QMessageBox() # per futuri messaggi
	

	def _readDipendenti(self) -> dict:
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dipendenti = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		except TypeError:
			self._showMessage(f"{Path(paths['dipendenti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								QMessageBox.Icon.Critical, 'Errore critico')
			self.close()
			raise
		
		return dipendenti
	

	def _fillListWidget(self):
		row = 1
		for data in self.dipendente.getAssenze():
			newItem = myListWidgetItem(data.strftime('%d/%m/%Y'), data)
			newItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
			self.listWidget.addItem(newItem)


	def _setUpAndConnectButtons(self):
		
		self.btnPiu.setIcon(QtGui.QIcon(GestoreFile.absolutePath('plus.png', Path.cwd())))
		self.btnPiu.clicked.connect(self._btnPiuClicked)
		self.btnMeno.setIcon(QtGui.QIcon(GestoreFile.absolutePath('minus.png', Path.cwd())))
		self.btnMeno.clicked.connect(self._btnMenoClicked)
		

	def _btnMenoClicked(self):
		if self.listWidget.currentItem() == None:
			self._showMessage("Seleziona prima l'assenza da eliminare.", QMessageBox.Icon.Warning, 'Errore')
		else:
			selectedDate = self.listWidget.currentItem().connectedObject
			if selectedDate < date.today():
				self._showMessage("Impossibile eliminare un'assenza con data antecedente a quella odierna.", QMessageBox.Icon.Warning, 'Errore')
				return
			self.dipendente.rimuoviAssenza(selectedDate)
			self._salvaDipendente()
			self.listWidget.takeItem(self.listWidget.row(self.listWidget.currentItem()))


	def _btnPiuClicked(self):
		def btnSelezionaClicked():
			selectedDate = selezionaDataWidget.dateEdit.date().toPyDate()
			if selectedDate in self.dipendente.getAssenze():
				self._showMessage(f"Il giorno {selectedDate.strftime('%d/%m/%Y')} è gia stato inserito tra le assenze.", QMessageBox.Icon.Warning, 'Errore')
				return	
			self.dipendente.aggiungiAssenza(selectedDate)
			self._salvaDipendente()
			self._insertSortedDate(selectedDate)
			selezionaDataWidget.close()

		selezionaDataWidget = QWidget()
		loadUi(GestoreFile.absolutePath('selezionaData.ui', Path.cwd()), selezionaDataWidget)
		selezionaDataWidget.dateEdit.setMinimumDate(date.today())
		selezionaDataWidget.btnSeleziona.clicked.connect(btnSelezionaClicked)
		selezionaDataWidget.show()


	def _insertSortedDate(self, dataDaInserire : date):
		newItem = myListWidgetItem(dataDaInserire.strftime('%d/%m/%Y'), dataDaInserire)
		newItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
		dataInserita = False
		for row in range(0, self.listWidget.count()):
			item = self.listWidget.item(row) # restituisce l'item alla riga row. Ogni item che viene inserito nella list widget è della classe myListWidgetItem
			if dataDaInserire < item.connectedObject and not dataInserita: # se la data da inserire è antecedente a quella che si trova alla riga 'row'
				self.listWidget.insertItem(row, newItem)
				dataInserita = True
		if not dataInserita: # se dataDaInserire non è stata ancora inserita, viene aggiunta in fondo alla lista
			self.listWidget.addItem(newItem)

	
	def _salvaDipendente(self):
		# salvo le modifihe su file
		dipendenti = self._readDipendenti()
		dipendenti[self.dipendente.getId()] = self.dipendente
		paths = GestoreFile.leggiJson(Path('paths.json'))
		GestoreFile.salvaPickle(dipendenti, Path(paths['dipendenti']))

	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()




if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = VisualizzaAssenzeUI(QWidget())
	mainWidget.show()
	sys.exit(app.exec_())