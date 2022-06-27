from PyQt5.QtWidgets import *

class FormUI(QWidget):
	
	def __init__(self, n, **kwargs):
		"""n è un parametro fittizio. Senza di esso il costruttore non verrebbe chiamato in caso di ereditarietà multipla,
		in particolare nel caso in cui FormUI non sia nell'MRO la prima delle superclassi."""
		i = n
		super().__init__(**kwargs)


	def hideLabels(self, lineEditLabelPairs : dict):
		for label in lineEditLabelPairs.values():
			label.hide()


	def connectLabelAndText(self, lineEditLabelPairs : dict):
		"""Rende la label visibile solo se la corrispondente line edit non è vuota."""
		def conditionalShowLabel(oldPos, newPos):
			lineEdit = self.sender()
			if lineEditLabelPairs[lineEdit].isHidden() and newPos == 1: # mostro la label se questa è nascosta e il cursore 
				lineEditLabelPairs[lineEdit].show() 					# si trova in posizione 1 (è stato inserito un carattere)
		
		for lineEdit in lineEditLabelPairs:
			lineEdit.cursorPositionChanged.connect(conditionalShowLabel)
			lineEdit.textChanged.connect(lambda text: lineEditLabelPairs[self.sender()].hide() if text == '' else None) # quando la line edit torna vuota, la label scompare


	def showLabels(self, lineEditLabelPairs : dict):
		for label in lineEditLabelPairs.values():
			label.show()