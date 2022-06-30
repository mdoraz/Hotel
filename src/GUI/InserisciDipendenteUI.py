import sys
import os
from datetime import date
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src.Attori.Ruolo import Ruolo
from src.GUI.FormUI import FormUI

from src.Gestori.GestoreFile import GestoreFile
from src.Gestori.GestorePersona import GestorePersona
from src.Utilities.encrypter import encrypt


class InserisciDipendenteUI(QTabWidget, FormUI):
	
	def __init__(self):
		kwargs = {'n' : 100} # parametro fittizio, utile a far attivare anche il costruttore di FormUI
		super().__init__(**kwargs)

		print(os.getcwd())

		loadUi('ui/Titolare/GestisciDipendenti/inserisciDipendente1.ui', self)
		tabWidgetPage2 = InserisciDipendentePage2(self)
		self.page2 = tabWidgetPage2.tabInserisciDipendente
		
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
		
		self.btnAnnulla.clicked.connect(self.close)
		self.btnAvanti.clicked.connect(self._avantiClicked)


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


	def _avantiClicked(self):
		for lineEdit in self.lineEditLabelPairs:
			if lineEdit.text().strip() == '': # se la line edit è vuota o contiene solo spazi
				self._showMessage('Inserisci tutti i campi, per favore.', QMessageBox.Icon.Warning, 'Errore')
				return
		
		styleSheet = f"color: rgb(0, 170, 0); font-family: Arial; font-size: 10pt"
		if [self.lineEditEmail.styleSheet(), self.lineEditCellulare.styleSheet(), self.lineEditIBAN.styleSheet()] != [styleSheet] * 3: # se le 3 line edit non hanno il testo verde
			self._showMessage('I dati in rosso non sono accettabili.\nQuando lo saranno il loro colore diventerà verde.', QMessageBox.Icon.Warning, 'Errore')
			return
		
		self.addTab(self.page2, 'Inserisci Dipendente')  # type: ignore
		self.removeTab(0)
	

	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()




class InserisciDipendentePage2(QTabWidget, FormUI):

	def __init__(self, parent : QWidget):
		kwargs = {'n' : 100} # parametro fittizio, utile a far attivare anche il costruttore di FormUI
		super().__init__(**kwargs)
		
		loadUi('ui/Titolare/GestisciDipendenti/inserisciDipendente2.ui', self)
		
		self.msg = QMessageBox() #per futuri messaggi

		self.lineEditLabelPairs = {
			self.lineEditUsername : self.labelUsername,
			self.lineEditPassword : self.labelPassword,
			self.lineEditConfermaPassword : self.labelConfermaPassword,
		}
		self.hideLabels(self.lineEditLabelPairs) # all'inizio tutte le label sono nascoste
		self.connectLabelAndText(self.lineEditLabelPairs) # rende la label visibile solo se la corrispondente line edit non è vuota.

		self.parentTabWidget = parent # per tornare alla pagina precedente al click del bottone "indietro"
		
		eyeBtn1 = QToolButton() # creati i bottoni per mostrare/nascondere la password
		eyeBtn2 = QToolButton()
		self._connectEye(eyeBtn1, self.lineEditPassword) # collega eyeBtn alla line edit corrispondente
		self._connectEye(eyeBtn2, self.lineEditConfermaPassword)																		 # 8 o più caratteri, almeno una maiuscola, una minuscola e un numero
		
		self.lineEditPassword.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$")))
		
		self.btnIndietro.clicked.connect(self._indietroClicked)
		self.btnInserisci.clicked.connect(self._inserisciDipendenteClicked)


	def _connectEye(self, eyeButton : QToolButton, lineEdit : QLineEdit):
		def showHidePassword(checked):
			if checked:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
				eyeButton.setIcon(QtGui.QIcon('files/icons/eye-close.jpg'))
			else:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
				eyeButton.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))
		
		eyeButton.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))
		eyeButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
		eyeButton.setCheckable(True)
		eyeButton.clicked.connect(showHidePassword)
		widgetAction = QWidgetAction(lineEdit)
		widgetAction.setDefaultWidget(eyeButton)
		lineEdit.addAction(widgetAction, QLineEdit.ActionPosition.TrailingPosition) # azione aggiunta nella parte destra della line edit

	
	def _indietroClicked(self):
		self.parentTabWidget.addTab(self.parentTabWidget.tabInserisciDipendente, 'Inserisci Dipendente')  # type: ignore
		self.parentTabWidget.removeTab(0)

	
	def _inserisciDipendenteClicked(self):
		def isPasswordCorrect() -> bool:
			toReturn = True
			if self.lineEditPassword.validator().validate(self.lineEditPassword.text(), 0)[0] != QtGui.QValidator.State.Acceptable:
				self._showMessage('La password non rispetta la struttura richiesta.', QMessageBox.Icon.Warning, 'Errore')
				print(self.lineEditPassword.validator().validate(self.lineEditPassword.text(), 0))
				toReturn = False
			elif self.lineEditConfermaPassword.text() != self.lineEditPassword.text():
				self._showMessage('La password e la sua conferma non corrispondono.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = False
			return toReturn

		def isUsernameUsed(paths : dict) -> bool:
			toReturn = False
			try:
				dipendenti = GestoreFile.leggiPickle(Path(paths['dipendenti']))
				if not isinstance(dipendenti, dict):
					self._showMessage(f"{Path(paths['dipendenti']).name} has been corrupted and ca't be restored.\nTo make the program run again, delete it.",
									  QMessageBox.Icon.Critical, 'Errore critico')
					self.close()
					return True
			except FileNotFoundError:
				dipendenti = {}
			for dipendente in dipendenti.values():
				if dipendente.getUsername() == self.lineEditUsername.text():
					self._showMessage('Username già in uso, inserirne un altro.', QMessageBox.Icon.Warning, 'Errore')
					toReturn = True
			return toReturn
		
		for lineEdit in self.lineEditLabelPairs:
			if lineEdit.text().strip() == '': # se la line edit è vuota o contiene solo spazi
				self._showMessage('Inserisci tutti i campi, per favore.', QMessageBox.Icon.Warning, 'Errore')
				return
		
		paths = GestoreFile.leggiJson(Path('paths.json'))
		if isPasswordCorrect() and not isUsernameUsed(paths):
			datiAggiuntivi = {
				'IBAN' : self.parentTabWidget.lineEditIBAN.text(),
				'turno' : True if self.parentTabWidget.comboBoxTurno.currentText() == 'Mattina' else False,
				'ruolo' : Ruolo.RECEPTIONIST if self.parentTabWidget.comboBoxRuolo.currentText() == 'Receptionist' else Ruolo.CAMERIERE,
				'username' : self.lineEditUsername.text(),
				'password' : encrypt(self.lineEditPassword.text())
			}
			GestorePersona.aggiungiPersona(Path(paths['dipendenti']), self.parentTabWidget.lineEditNome.text(), 
										   self.parentTabWidget.lineEditCognome.text(), self.parentTabWidget.dateEdit.date().toPyDate(),
										   self.parentTabWidget.lineEditLuogoNascita.text(), self.parentTabWidget.lineEditEmail.text(),
										   self.parentTabWidget.lineEditCellulare.text(), **datiAggiuntivi)
			self._showMessage('Il dipendente è stato inserito con successo!', QMessageBox.Icon.Information)
			self.parentTabWidget.close()
		
	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()




if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = InserisciDipendenteUI()
	mainWidget.show()
	sys.exit(app.exec_())