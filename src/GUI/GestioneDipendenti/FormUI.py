from PyQt5.QtWidgets import *

class FormUI(QWidget):
	
	def __init__(self, formParent : QWidget = None, **kwargs): # type: ignore
		"""n è un parametro fittizio. Senza di esso il costruttore non verrebbe chiamato in caso di ereditarietà multipla,
		in particolare nel caso in cui FormUI non sia nell'MRO la prima delle superclassi."""
		super().__init__(formParent, **kwargs)


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

	
	def fieldsFilled(self, lineEditLabelPairs : dict) -> bool:
		"""Returns true if all line edits are not empty."""
		toReturn = True
		for lineEdit in lineEditLabelPairs:
			if lineEdit.text().strip() == '': # se la line edit è vuota o contiene solo spazi
				self._showMessage('Inserisci tutti i campi, per favore.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = False
		return toReturn

	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
