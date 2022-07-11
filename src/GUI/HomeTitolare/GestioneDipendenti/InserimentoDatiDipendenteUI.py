from datetime import date
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Utilities.GUIUtils import GUIUtils
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.FormUI import FormUI


class InserimentoDatiDipendenteUI(FormUI):

	def __init__(self, previous : QWidget):
		super().__init__()
		
		self.pevious = previous
		loadUi(GestoreFile.absolutePath('inserimentoDatiDipendente.ui', Path.cwd()), self)
		
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
		
		self._setUpperCase() # rende maiuscola la prima lettera per nome, cognome e luogo di nascita inseriti.
		self._setDataNascitaBoundaries() # imposta un limite superiore e inferiore per la data di nascita
		self._setValidators() # imposta i validator restringere gli input accettati dalle lineEdit.
		self._setColorHints() # i dati inseriti sono rossi se non accettabili, verdi se accettabili.

	
	def _readDipendenti(self) -> dict:
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dipendenti = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		except TypeError:
			self._showMessage(f"{Path(paths['dipendenti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		
		return dipendenti


	def _setDataNascitaBoundaries(self):
		todayDay = date.today().day
		todayMonth = date.today().month
		todayYear = date.today().year
		self.dateEdit.setMaximumDate(QtCore.QDate(todayYear - 18, todayMonth, todayDay)) # no dipendenti minorenni
		self.dateEdit.setMinimumDate(QtCore.QDate(todayYear - 100, todayMonth, todayDay))


	def _setUpperCase(self):
		def textToUpper(oldPos, newPos):
			if oldPos == 0 and newPos == 1:
				lineEdit = self.sender()
				text = lineEdit.text()
				lineEdit.setText(text[0].upper() + text[1:])
		
		self.lineEditNome.cursorPositionChanged.connect(textToUpper)
		self.lineEditCognome.cursorPositionChanged.connect(textToUpper)
		self.lineEditLuogoNascita.cursorPositionChanged.connect(textToUpper)


	def _setValidators(self):
		self.lineEditNome.setValidator(GUIUtils.validators['soloLettere'])
		self.lineEditCognome.setValidator(GUIUtils.validators['soloLettere'])
		self.lineEditLuogoNascita.setValidator(GUIUtils.validators['soloLettere'])
		self.lineEditEmail.setValidator(GUIUtils.validators['email'])
		self.lineEditCellulare.setValidator(GUIUtils.validators['cellulare'])
		self.lineEditIBAN.setValidator(GUIUtils.validators['IBAN'])
	

	def _setColorHints(self):
		self.lineEditEmail.textChanged.connect(self._setColorHint)
		self.lineEditCellulare.textChanged.connect(self._setColorHint)
		self.lineEditIBAN.textChanged.connect(self._setColorHint)

	
	def isUserInSystem(self) -> bool:
		toReturn = False
		dipendenti = self._readDipendenti()
		for dipendente in dipendenti.values():
			if (dipendente.getNome() == self.lineEditNome.text() and dipendente.getCognome() == self.lineEditCognome.text() and 
				dipendente.getDataNascita() == self.dateEdit.date().toPyDate() and dipendente.getLuogoNascita() == self.lineEditLuogoNascita.text()):
				self._showMessage('Questo dipendente è già presente nel sistema, non può essere inserito nuovamente.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = True
		return toReturn

	
	def fieldsValid(self) -> bool:
		toReturn = True
		styleSheet = f"color: rgb(0, 170, 0);"
		if [self.lineEditEmail.styleSheet(), self.lineEditCellulare.styleSheet(), self.lineEditIBAN.styleSheet()] != [styleSheet] * 3: # se le 3 line edit non hanno il testo verde
			self._showMessage('I dati in rosso non sono accettabili.\nQuando lo saranno il loro colore diventerà verde.', QMessageBox.Icon.Warning, 'Errore')
			toReturn = False
		return toReturn

	
	
