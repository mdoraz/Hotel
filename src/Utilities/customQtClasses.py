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


	def firstEmptyRow(self, column : int) -> int:
		"""Returns the row index of the first empty cell of this table widget in the specified column"""
		lastRowIndex = self.rowCount() - 1
		item = self.item(lastRowIndex, column) # se table.rowCount() == 0, lastRowIndex == -1, quindi item == None --> non entro nel while, ritorno 0
		while(item == None and lastRowIndex >= 0):
			lastRowIndex -= 1
			item = self.item(lastRowIndex, column)
		return lastRowIndex + 1


	def _analyzeItemChangment(self, item : QTableWidgetItem):
		if item.row() == self.rowCount() - 1: # se l'item modificato si trova all'ultima riga
			lastRowEmpty = True
			for i in range(0, self.columnCount()):
				if self.item(item.row(), i) != None:
					lastRowEmpty = False
			
			if not lastRowEmpty: # se c'e almeno 1 cella noon vuota nell'ultima riga
				self.lastRowNotEmpty.emit()

	
