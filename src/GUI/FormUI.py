from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from src.Gestori.GestoreFile import GestoreFile

class FormUI(QWidget):
	
	def __init__(self, formParent : QWidget = None, **kwargs): # type: ignore
		super().__init__(formParent, **kwargs)

		self.msg = QMessageBox() # per futuri messaggi


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
	

	def _setColorHint(self, text : str): # text è il testo della line edit da controllare
		"""Slot to connect to a signal 'textChanged' of a line edit that has a validator.\n
		This method makes the line edit text green
		if and only if passing that text to the validate method of the line edit validator, the result is Acceptable."""
		lineEdit = self.sender()
		font = lineEdit.font() # salvo il file prima della modifica dello style sheet, poichè questa potrebbe azzerare il font della line edit
		
		if text != '' and lineEdit.validator().validate(text, 0)[0] == QtGui.QValidator.State.Acceptable: # se il testo è accettato dal validator
			if lineEdit.styleSheet() != f"color: rgb(0, 170, 0);":
				lineEdit.setStyleSheet(f"color: rgb(0, 170, 0);") # il testo diventa verde
				lineEdit.setFont(font)
		
		elif lineEdit.styleSheet() != f"color: rgb(255, 0, 0);":
			lineEdit.setStyleSheet(f"color: rgb(255, 0, 0);") # il testo diventa rosso
			lineEdit.setFont(font)


	def _addAndConnectEye(self, lineEdit : QLineEdit):
		eyeButton = QToolButton()
		def showHidePassword(checked):
			if checked:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
				eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-closed.png', Path.cwd())))
			else:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
				eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-opened.png', Path.cwd())))

		eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-opened.png', Path.cwd())))
		eyeButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
		eyeButton.setCheckable(True)
		eyeButton.clicked.connect(showHidePassword)
		widgetAction = QWidgetAction(lineEdit)
		widgetAction.setDefaultWidget(eyeButton)
		lineEdit.addAction(widgetAction, QLineEdit.ActionPosition.TrailingPosition) # azione aggiunta nella parte destra della line edit

	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
