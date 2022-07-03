from typing import Iterable, Union
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

class MyTreeWidgetItem(QTreeWidgetItem):

	def __init__(self, parent : Union[QTreeWidget, QTreeWidgetItem], strings : Iterable[str], connectedObject : object):
		super().__init__(parent, strings, 0)
		self.connectedObject = connectedObject


class myListWidgetItem(QListWidgetItem):

	def __init__(self, text : str, connectedObject : object):
		super().__init__(text, None, 0)
		self.connectedObject = connectedObject
