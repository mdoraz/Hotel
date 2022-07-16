from typing import Iterable, Union
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

class MyTreeWidgetItem(QTreeWidgetItem):

	def __init__(self, parent : Union[QTreeWidget, QTreeWidgetItem], strings : Iterable[str], connectedObject : object):
		super().__init__(parent, strings, 0)
		self.connectedObject = connectedObject


class MyListWidgetItem(QListWidgetItem):

	def __init__(self, text : str, connectedObject : object):
		super().__init__(text, None, 0)
		self.connectedObject = connectedObject


class MyTableWidgetItem(QTableWidgetItem):

	def __init__(self, text : str, connectedObject : object):
		super().__init__(text, 0)
		self.connectedObject = connectedObject


class MyTableWidget(QTableWidget):

	lastRowNotEmpty = QtCore.pyqtSignal()

	def __init__(self, parent : QWidget = None): # type: ignore
		super().__init__(parent)
		self.itemChanged.connect(self._analyzeItemChangment)
		self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


	def firstEmptyRow(self, column : int) -> int:
		"""Returns the row index of the first empty cell of this table widget in the specified column"""
		lastRowIndex = self.rowCount() - 1
		item = self.item(lastRowIndex, column) # se table.rowCount() == 0, lastRowIndex == -1, quindi item == None --> non entro nel while, ritorno 0
		while(item == None and lastRowIndex >= 0):
			lastRowIndex -= 1
			item = self.item(lastRowIndex, column)
		return lastRowIndex + 1


	def _analyzeItemChangment(self, item : QTableWidgetItem):
		"""Slot to connect to the signal itemChanged of this table widget."""
		if item.row() == self.rowCount() - 1: # se l'item modificato si trova all'ultima riga
			lastRowEmpty = True
			for i in range(0, self.columnCount()):
				if self.item(item.row(), i) != None:
					lastRowEmpty = False
			
			if not lastRowEmpty: # se c'e almeno 1 cella non vuota nell'ultima riga
				self.lastRowNotEmpty.emit()
	

	def swapItems(self, item1 : Union[QTableWidgetItem, QtCore.QModelIndex], item2 : Union[QTableWidgetItem, QtCore.QModelIndex]):
		itemA = self.item(item1.row(), item1.column())
		itemB = self.item(item2.row(), item2.column())

		if itemA == None and itemB == None:
			return # se sono enteambi item nulli, non avviene lo scambio
		elif itemA == None or itemB == None: # se una delle due celle da scambiare è vuota
			emptyModelIndex = item1 if itemA == None else item2 # emptyItem è della classe QModelIndex
			fullItem = itemA if itemA != None else itemB # fullItem è della classe QTableWidgetItem (o sottoclassi, come MyQTableWidget)

			oldFullItemRow = fullItem.row() # salvo la riga della cella che verrà abbandonata da fullItem
			oldFullItemColumn = fullItem.column() # salvo la colonna della cella che verrà abbandonata da fullItem
			fullItem.setSelected(False) # deseleziono la cella di partenza di fullItem

			self.takeItem(fullItem.row(), fullItem.column())
			self.setItem(emptyModelIndex.row(), emptyModelIndex.column(), fullItem)

			fullItem.setSelected(False) # deseleziono la cella di arrivo di fullItem

			self.shiftColumnUp(oldFullItemRow + 1, oldFullItemColumn)
			# anche fullItem scala in alto, finchè non incontra una cella non vuota oppure non arriva alla prima riga
			while self.item(fullItem.row() - 1, fullItem.column()) == None and fullItem.row() > 0:
				self.setItem(fullItem.row() - 1, fullItem.column(), self.takeItem(fullItem.row(), fullItem.column())) # fullItem si sposta di una riga sopra
		else:
			itemArow = itemA.row()		 ; itemBrow = itemB.row()
			itemAcolumn = itemA.column() ; itemBcolumn = itemB.column()

			self.takeItem(itemArow, itemAcolumn)
			self.takeItem(itemBrow, itemBcolumn)
			self.setItem(itemArow, itemAcolumn, itemB)
			self.setItem(itemBrow, itemBcolumn, itemA)

			itemA.setSelected(False) # deseleziono le celle scambiate
			itemB.setSelected(False)
		
		self.clearEmptyBottom()
	

	def findItem(self, connectedObject : object) -> Union[MyTableWidgetItem, None]:
		i = 0
		while i < self.columnCount():
			j = 0
			while j < self.rowCount():
				item = self.item(j, i)
				if isinstance(item, MyTableWidgetItem):
					if connectedObject == item.connectedObject:
						return item
				j += 1
			i += 1
		return None
	

	def addItem(self, column : int, item : MyTableWidgetItem):
		"""Adds item at the bottom of the specified column of this table widget"""
		row = self.firstEmptyRow(column) # cerco l'indice della riga in cui inserire item
		if row == self.rowCount():
			self.insertRow(self.rowCount())
			self.setVerticalHeaderLabels([''] * self.rowCount())

		self.setItem(row, column, item)

	
	def removeItem(self, item : MyTableWidgetItem):
		"""Removes the item from this table widget"""
		oldItemRow = item.row() # fisso riga e colonna dell'item perchè dopo la sua rimozione dal table widgeti metodi row() e column()
		oldItemColumn = item.column() # restituiranno -1
		
		self.takeItem(item.row(), item.column())
		self.shiftColumnUp(oldItemRow + 1, oldItemColumn)
		self.clearEmptyBottom()


	def shiftColumnUp(self, row : int, column : int):
		"""starting from the index 'row', all the items of column will shift one position up"""
		for indexRow in range(row, self.rowCount()):
			item = self.takeItem(indexRow, column)
			self.setItem(indexRow - 1, column, item)
	

	def clearEmptyBottom(self):
		"""Removes the last empty rows"""
		lastRowEmpty = True
		for i in range(0, self.columnCount()):
			if self.item(self.rowCount() - 1, i) != None:
				lastRowEmpty = False

		while lastRowEmpty:
			self.removeRow(self.rowCount() - 1)
			
			for i in range(0, self.columnCount()):
				if self.item(self.rowCount() - 1, i) != None:
					lastRowEmpty = False

	
