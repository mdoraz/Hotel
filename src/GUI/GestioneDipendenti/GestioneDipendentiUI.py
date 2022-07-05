import sys
import platform
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

from src.Attori.Dipendente import Dipendente
from src.Attori.Ruolo import Ruolo
from src.GUI.GestioneDipendenti.InserisciDipendenteUI import InserisciDipendenteUI
from src.GUI.GestioneDipendenti.VisualizzaDipendenteUI import VisualizzaDipendenteUI
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.customQtClasses import MyTableWidget, MyTableWidgetItem


class GestioneDipendentiUI(QTabWidget):
	
	turnoModificato = QtCore.pyqtSignal(Dipendente)

	def __init__(self, previous : QWidget): #previous è un oggetto che rappresente la pagina precedente al oggetto della classe attuale
		super().__init__()

		loadUi(GestoreFile.absolutePath('gestioneDipendenti.ui', Path.cwd()), self)

		self.previous = previous

		if platform.system() == 'Darwin':
			position = QTabBar.ButtonPosition.LeftSide  # se sistema operativo è MacOs
		else:
			position = QTabBar.ButtonPosition.RightSide  # se sistema operativo è diverso da MacOs

		self.tabBar().tabButton(0,position).deleteLater()  # il tab button all'indice 0 della tab bar sarà eliminato
		self.tabBar().setTabButton(0, position, None)  # type: ignore
		self.tabBar().tabButton(1, position).deleteLater()  # il tab button all'indice 1 della tab bar sarà eliminato
		self.tabBar().setTabButton(1, position, None)  # type: ignore
		self.tabCloseRequested.connect(self.removeTab) # il click della x di una tab fa chiudere quella tab
		
		self._setUpTabDipendenti()
		self._setUpTabTurni()

		self._connectButtons()

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

	def _setUpTabDipendenti(self):
		self._fillTreeWidgetDipendenti() # riempita la tree widget con i dipendenti in memoria
		self.treeWidgetDipendenti.itemDoubleClicked.connect(self._visualizzaDipendente) # al doppio click di un item della tree widget, viene mostrato l'account del dipendente corrispondente
	

	def _setUpTabTurni(self):
		self._addTableTurni() # aggiungo le tabelle della classe MyTableWidget
		self._fillTableTurni() #riempita le due table widget dei turni
		self._addButtonsTurni()

		# il bottone scambia si attiva solo quando è consentito lo scambio del turno tra due dipendenti
		self.tableReceptionist.itemSelectionChanged.connect(lambda: self._connectBtnScambia(self.tableReceptionist, self.btnScambiaReceptionist))
		self.tableCamerieri.itemSelectionChanged.connect(lambda: self._connectBtnScambia(self.tableCamerieri, self.btnScambiaCamerieri))
		
		# il bottone piu' si attiva solo quando la tabella ha l'ultima riga non vuota
		self.tableReceptionist.lastRowNotEmpty.connect(lambda: self.btnPlusReceptionist.setEnabled(True))
		self.tableCamerieri.lastRowNotEmpty.connect(lambda: self.btnPlusCamerieri.setEnabled(True))

	
	def _fillTreeWidgetDipendenti(self):
		dipendenti = self._readDipendenti()

		for dipendente in dipendenti.values():
			self.treeWidgetDipendenti.addTopLevelItem(QTreeWidgetItem([f"{dipendente.getId()}" , dipendente.getCognome(), 
													  dipendente.getNome()], 0))

		self.treeWidgetDipendenti.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder) # cognomi in ordine alfabetico


	def _addTableTurni(self):
		self.tableReceptionist = MyTableWidget()
		self.tableReceptionist.setColumnCount(2)
		self.tableReceptionist.setHorizontalHeaderLabels(['Mattina', 'Pomeriggio'])
		self.tableReceptionist.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		self.layoutGroupReceptionist.addWidget(self.tableReceptionist, 0, 0, 1, -1)

		self.tableCamerieri = MyTableWidget()
		self.tableCamerieri.setColumnCount(2)
		self.tableCamerieri.setHorizontalHeaderLabels(['Mattina', 'Pomeriggio'])
		self.tableCamerieri.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		self.layoutGroupCamerieri.addWidget(self.tableCamerieri, 0, 0, 1, -1)	


	def _fillTableTurni(self):

		dipendenti = self._readDipendenti()
		for dipendente in dipendenti.values():
			item = MyTableWidgetItem(f'{dipendente.getCognome()}({dipendente.getId()})', dipendente)
			if dipendente.getAutorizzazione() == Ruolo.RECEPTIONIST:
				if dipendente.getTurno() == True: # turno di mattina
					rowIndex = self.tableReceptionist.firstEmptyRow(0)
					if rowIndex + 1 > self.tableReceptionist.rowCount(): # se la tabella non ha la riga in cui deve essere inserito l'item
						self.tableReceptionist.setRowCount(rowIndex + 1) # imposto il numero di righe fino a quella che mi serve
					self.tableReceptionist.setItem(rowIndex, 0, item) # inserisco l'item nella colonna 0
				else: # turno di pomeriggio
					rowIndex = self.tableReceptionist.firstEmptyRow(1)
					if rowIndex + 1 > self.tableReceptionist.rowCount():
						self.tableReceptionist.setRowCount(rowIndex + 1)
					self.tableReceptionist.setItem(rowIndex, 1, item) # inserisco l'item nella colonna 1
			elif dipendente.getAutorizzazione() == Ruolo.CAMERIERE:
				if dipendente.getTurno() == True:
					rowIndex = self.tableCamerieri.firstEmptyRow(0)
					if rowIndex + 1 > self.tableCamerieri.rowCount():
						self.tableCamerieri.setRowCount(rowIndex + 1)
					self.tableCamerieri.setItem(rowIndex, 0, item)
				else:
					rowIndex = self.tableCamerieri.firstEmptyRow(1)
					if rowIndex + 1 > self.tableCamerieri.rowCount():
						self.tableCamerieri.setRowCount(rowIndex + 1)
					self.tableCamerieri.setItem(rowIndex, 1, item)
		
		self.tableReceptionist.setVerticalHeaderLabels([''] * self.tableReceptionist.rowCount()) # il nome di ogni riga diventa vuoto
		self.tableCamerieri.setVerticalHeaderLabels([''] * self.tableCamerieri.rowCount())


	def _addButtonsTurni(self):
		self.layoutGroupReceptionist.addWidget(self.btnScambiaReceptionist, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
		self.layoutGroupCamerieri.addWidget(self.btnScambiaCamerieri, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)

		self.btnPlusReceptionist = QToolButton()
		self.btnPlusReceptionist.setIcon(QtGui.QIcon(GestoreFile.absolutePath('plus.png', Path.cwd())))
		self.layoutGroupReceptionist.addWidget(self.btnPlusReceptionist, 1, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
		self.btnPlusCamerieri = QToolButton()
		self.btnPlusCamerieri.setIcon(QtGui.QIcon(GestoreFile.absolutePath('plus.png', Path.cwd())))
		self.layoutGroupCamerieri.addWidget(self.btnPlusCamerieri, 1, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

	
	def _connectButtons(self):
		self.btnNuovoDipendente.clicked.connect(self._btnNuovoDipendenteClicked)
		self.btnHelp.clicked.connect(lambda: self._showMessage('Si possono scambiare di turno due dipendenti selezionandoli e cliccando su "Scambia".\n' + 
															   'N.B.: i due dipendenti devono avere lo stesso ruolo e devono avere uno il turno ' +
															   'di mattina e uno quello di pomeriggio.', QMessageBox.Icon.Information))
		self.btnScambiaReceptionist.clicked.connect(self._scambiaTurni)
		self.btnScambiaCamerieri.clicked.connect(self._scambiaTurni)
		self.btnPlusReceptionist.clicked.connect(self._btnPlusClicked)
		self.btnPlusCamerieri.clicked.connect(self._btnPlusClicked)
		self.btnIndietro1.clicked.connect(self.btnIndietroClicked)
		self.btnIndietro2.clicked.connect(self.btnIndietroClicked)

	
	def _connectBtnScambia(self, table : QTableWidget, button : QAbstractButton):
		selectedCells = table.selectedIndexes() # considera anche la selezione di celle vuote
		if len(selectedCells) != 2:
			if button.isEnabled():
				button.setEnabled(False)
		else: # gli item selezionati sono 2
			if (selectedCells[0].column() + selectedCells[1].column() == 1  and # se un item è nella colonna 0 e l'altro nella colonna 1
				not (table.selectedIndexes()[0].model().data(table.selectedIndexes()[0]) == None and table.selectedIndexes()[1].model().data(table.selectedIndexes()[1]) == None)): # e non sono entrambi celle vuote
				button.setEnabled(True)

	
	def _visualizzaDipendente(self, itemClicked : QTreeWidgetItem):
		
		id = itemClicked.text(0) # prendo l'id del dipendente slezionato
		dipendenti = self._readDipendenti()
		self.widgetVisualizzaDipendente = VisualizzaDipendenteUI(dipendenti[int(id)], self)
		self.addTab(self.widgetVisualizzaDipendente, f"Visualizza ID {dipendenti[int(id)].getId()}")
		index = self.count() - 1
		self.setCurrentIndex(index)
		
		def func():
			self.treeWidgetDipendenti.takeTopLevelItem(
				self.treeWidgetDipendenti.indexOfTopLevelItem(self.treeWidgetDipendenti.currentItem())
			) # rimuove dal tree widget dei dipendenti la riga del dipendente eliminato
			self.removeTab(index) # chiude la tab che visualizzava il dipendente eliminato
		
		self.widgetVisualizzaDipendente.dipendenteEliminato.connect(func)
		self.widgetVisualizzaDipendente.turnoModificato.connect(self._aggiornaTableTurni)
		
		def aggiornaTurno(mainWidget : VisualizzaDipendenteUI, dipendente : Dipendente):
				mainWidget.dipendente.setTurno(dipendente.getTurno())
				mainWidget.lineEditTurno.setText('Mattina' if dipendente.getTurno() == True else 'Pomeriggio')
				mainWidget.comboBoxTurno.setCurrentText('Mattina' if dipendente.getTurno() == True else 'Pomeriggio')
		
		self.turnoModificato.connect(lambda dipendente: 
											aggiornaTurno(self.widgetVisualizzaDipendente, dipendente) 
											if dipendente.isTheSame(self.widgetVisualizzaDipendente.dipendente)
											else None)


	def _aggiornaTableTurni(self, dipendente : Dipendente, nuovoTurno : bool):
		text = f'{dipendente.getCognome()}({dipendente.getId()})'
		table = QTableWidget()
		if dipendente.getAutorizzazione() == Ruolo.RECEPTIONIST:
			table = self.tableReceptionist
		elif dipendente.getAutorizzazione() == Ruolo.CAMERIERE:
			table = self.tableCamerieri
		
		item = table.findItems(text, QtCore.Qt.MatchFlag.MatchExactly)[0]
		oldItemRow = item.row()
		column = 1 - item.column() # salvo l'indice della colonna in cui inserire item, cioè quella in cui non si trova attualmente
		row = table.firstEmptyRow(column) # cerco l'indice della riga in cui inserire item
		if row == table.rowCount():
			table.insertRow(table.rowCount())
			table.setVerticalHeaderLabels([''] * table.rowCount())
		
		table.takeItem(item.row(), item.column())
		table.setItem(row, column, item)

		table.shiftColumnUp(oldItemRow + 1, 1 - item.column())
		# se l'ultima riga rimane completamente vuota viene eliminata
		while table.item(table.rowCount() - 1, 0) == None and table.item(table.rowCount() - 1, 1) == None:
			table.removeRow(table.rowCount() - 1)

	
	def _btnNuovoDipendenteClicked(self):
		def addSortedItem(dipendente : Dipendente):				# diminuisco l'id di 1 perche il dipendente passato a questa funzione è stato creato subito dopo la creazione della sua 'copia' 
			self.treeWidgetDipendenti.addTopLevelItem(QTreeWidgetItem([f"{dipendente.getId() - 1}", dipendente.getCognome(), # che è stata salvata sul file dipendenti.pickle
													  dipendente.getNome()], 0))
			self.treeWidgetDipendenti.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder) # cognomi in ordine alfabetico
		
		self.widgetInserisciDipendente = InserisciDipendenteUI(self)
		self.widgetInserisciDipendente.show()
		self.widgetInserisciDipendente.dipendenteAggiunto.connect(addSortedItem)

	
	def _scambiaTurni(self):
		table = QTableWidget()
		btnPlus = QToolButton()
		if self.sender() == self.btnScambiaReceptionist:
			table = self.tableReceptionist
			btnPlus = self.btnPlusReceptionist
		elif self.sender() == self.btnScambiaCamerieri:
			table = self.tableCamerieri
			btnPlus = self.btnPlusCamerieri

		selectedIndexes = table.selectedIndexes()
		selectedItems = table.selectedItems()
		
		if selectedIndexes[0].model().data(selectedIndexes[0]) == None or selectedIndexes[1].model().data(selectedIndexes[1]) == None:
			
			fullItem = selectedItems[0] # selectedItems contiene 1 solo elemento, quello non nullo tra le 2 celle selezionate
			emptyModelIndex = selectedIndexes[0] if selectedIndexes[0].model().data(selectedIndexes[0]) == None else selectedIndexes[1] # assegno il QTableWidgetItem vuoto

			table.swapItems(fullItem, emptyModelIndex)
			
			# salvo le modifiche per il dipendente spostato di turno
			dipendente = fullItem.connectedObject # type: ignore
			dipendente.setTurno(True if fullItem.column() == 0 else False)
			dipendenti = self._readDipendenti()
			dipendenti[dipendente.getId()] = dipendente
			paths = GestoreFile.leggiJson(Path('paths.json'))
			GestoreFile.salvaPickle(dipendenti, Path(paths['dipendenti']))

			self.turnoModificato.emit(dipendente)
		else:
			item1 = selectedItems[0]
			item2 = selectedItems[1]
			table.swapItems(item1, item2)
			
			# salvo la modifica di turno per i due dipendenti coinvolti nello scambio
			dipendente1 = item1.connectedObject # type: ignore
			dipendente1.setTurno(True if item1.column() == 0 else False)
			dipendente2 = item2.connectedObject # type: ignore
			dipendente2.setTurno(True if item2.column() == 0 else False)
			# salvo su file
			dipendenti = self._readDipendenti()
			dipendenti[dipendente1.getId()] = dipendente1
			dipendenti[dipendente2.getId()] = dipendente2
			paths = GestoreFile.leggiJson(Path('paths.json'))
			GestoreFile.salvaPickle(dipendenti, Path(paths['dipendenti']))

			self.turnoModificato.emit(dipendente1)
			self.turnoModificato.emit(dipendente2)

		if not btnPlus.isEnabled():
			btnPlus.setEnabled(True) # il bottone piu' viene attivato perchè sono state cancellate tutte le righe vuote (da swapItems)
		

	def _btnPlusClicked(self):
		table = MyTableWidget()
		if self.sender() == self.btnPlusReceptionist:
			table = self.tableReceptionist
		elif self.sender() == self.btnPlusCamerieri:
			table = self.tableCamerieri
		
		self.sender().setEnabled(False)
		table.insertRow(table.rowCount())
		table.setVerticalHeaderLabels([''] * table.rowCount())


	def btnIndietroClicked(self):
		self.previous.show()
		self.close()
	
	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()




if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = GestioneDipendentiUI(QWidget())
	mainWidget.show()
	sys.exit(app.exec_())