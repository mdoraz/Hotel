from datetime import date
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src.GUI.GestioneDipendenti.FormUI import FormUI

class InserimentoDatiDipendenteUI(FormUI):

	def __init__(self, previous : QWidget):
		super().__init__()
		
		self.pevious = previous
		loadUi('ui/Titolare/inserimentoDatiDipendente.ui', self)
		
		self.msg = QMessageBox() # per futuri messaggi
		
		self.lineEditLabelPairs = {
			self.lineEditNome : self.labelNome,
			self.lineEditCognome : self.labelCognome,
			self.lineEditLuogoNascita : self.labelLuogoNascita,
			self.lineEditEmail : self.labelEmail,
			self.lineEditCellulare : self.labelCellulare,
			self.lineEditIBAN : self.labelIBAN,
		}
		self.hideLabels(self.lineEditLabelPairs) # all'inizio tutte le label sono nascoste
		self.connectLabelAndText(self.lineEditLabelPairs) # rende la label visibile solo se la corrispondente line edit non è vuota.
		
		self._uppercaseForNomeCognomeLuogoNascita() # rende maiuscola la prima lettera per nome, cognome e luogo di nascita inseriti.
		self._setDataNascitaBoundaries() # imposta un limite superiore e inferiore per la data di nascita
		self._setValidators() # imposta i validator restringere gli input accettati dalle lineEdit.
		self._setColorHints() # i dati inseriti sono rossi se non accettabili, verdi se accettabili.


	def _setDataNascitaBoundaries(self):
		todayDay = date.today().day
		todayMonth = date.today().month
		todayYear = date.today().year
		self.dateEdit.setMaximumDate(QtCore.QDate(todayYear - 18, todayMonth, todayDay)) # no dipendenti minorenni
		self.dateEdit.setMinimumDate(QtCore.QDate(todayYear - 100, todayMonth, todayDay))


	def _uppercaseForNomeCognomeLuogoNascita(self):
		def textToUpper(oldPos, newPos):
			if oldPos == 0 and newPos == 1:
				lineEdit = self.sender()
				text = lineEdit.text()
				lineEdit.setText(text[0].upper() + text[1:])
		
		self.lineEditNome.cursorPositionChanged.connect(textToUpper)
		self.lineEditCognome.cursorPositionChanged.connect(textToUpper)
		self.lineEditLuogoNascita.cursorPositionChanged.connect(textToUpper)


	def _setValidators(self):
		self.lineEditNome.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z'àèòìù ]+"))) # solo lettere e spazi
		self.lineEditCognome.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z'àèòìù ]+")))
		self.lineEditLuogoNascita.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z'àèòìù ]+")))
		
		self.lineEditCellulare.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{10,10}"))) # 10 numeri
		self.lineEditIBAN.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{27,27}"))) #27 numeri
		
		# provider email accettati: gmail, outlook, hotmail, yahoo, tim, alice, libero, aruba
		pattern = ".+@(gmail\\.com|outlook\\.(com|it)|hotmail\\.com|yahoo\\.(com|it)|tim\\.it|alice\\.it|libero\\.it|aruba\\.(com|it))"
		self.lineEditEmail.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(pattern)))
	

	def _setColorHints(self):
		def setColorHint(text): # text è il testo della line edit da controllare, fixedLength la lunghezza che deve avere per essere accettabile
			fontType = "font-family: Arial; font-size: 10pt"
			lineEdit = self.sender()
			
			if text != '' and lineEdit.validator().validate(text, 0)[0] == QtGui.QValidator.State.Acceptable: # se il testo è accettato dal validator
				if lineEdit.styleSheet() != f"color: rgb(0, 170, 0); {fontType}":
					lineEdit.setStyleSheet(f"color: rgb(0, 170, 0); {fontType}") # il testo diventa verde
			
			elif lineEdit.styleSheet() != f"color: rgb(255, 0, 0); {fontType}":
				lineEdit.setStyleSheet(f"color: rgb(255, 0, 0); {fontType}") # il testo diventa rosso

		self.lineEditEmail.textChanged.connect(setColorHint)
		self.lineEditCellulare.textChanged.connect(setColorHint)
		self.lineEditIBAN.textChanged.connect(setColorHint)

	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()