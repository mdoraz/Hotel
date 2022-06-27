import sys
from datetime import date
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from Attori.Ruolo import Ruolo

from Gestori.GestoreFile import GestoreFile
from Gestori.GestorePersona import GestorePersona
from Utilities.encrypter import encrypt


class NuovoDipendenteUI(QTabWidget):
	
	hasBtnAvantiBeenClicked = False
	hasBtnIndietroBeenClicked = False
	
	def __init__(self):
		super().__init__()
		
		loadUi('ui/Titolare/inserisciDipendente1.ui', self)
		
		self.msg = QMessageBox() # per futuri messaggi
		self._setDataNascitaBoundaries() # imposta un limite superiore e inferiore per la data di nascita
		
		self.lineEditLabelPair = {
			self.lineEditNome : self.labelNome,
			self.lineEditCognome : self.labelCognome,
			self.lineEditLuogoNascita : self.labelLuogoNascita,
			self.lineEditEmail : self.labelEmail,
			self.lineEditCellulare : self.labelCellulare,
			self.lineEditIBAN : self.labelIBAN,
		}
		for label in self.lineEditLabelPair.values():
			label.hide() 							 # inizialmente tutte le lable sono nascoste
		
		self._uppercaseForNomeCognomeLuogoNascita() # rende maiuscola la prima lettera per nome, cognome e luogo di nascita inseriti.
		self._connectLabelAndText() # rende la label visibile solo se la corrispondente line edit non è vuota.
		self._setValidators() # imposta i validator restringere gli input accettati dalle lineEdit.
		self._setColorHints() # i dati inseriti sono rossi se non accettabili, verdi se accettabili.
		self._connectButtons() # dà una logica ai bottoni "annulla" e "avanti"


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

	
	def _connectLabelAndText(self):
		def conditionalShowLabel(oldPos, newPos):
			lineEdit = self.sender()
			if self.lineEditLabelPair[lineEdit].isHidden() and newPos == 1: # mostro la label se questa è nascosta e il cursore 
				self.lineEditLabelPair[lineEdit].show() 					# si trova in posizione 1 (è stato inserito un carattere)
		
		for lineEdit in self.lineEditLabelPair:
			lineEdit.cursorPositionChanged.connect(conditionalShowLabel)
			lineEdit.textChanged.connect(lambda text: self.lineEditLabelPair[self.sender()].hide() if text == '' else None) # quando la line edit torna vuota, la label scompare


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


	def _connectButtons(self):
		self.btnAnnulla.clicked.connect(self.close)
		self.btnAvanti.clicked.connect(self._avantiClicked)


	def _avantiClicked(self):
		for lineEdit in self.lineEditLabelPair:
			if lineEdit.text().strip() == '': # se la line edit è vuota o contiene solo spazi
				self._showMessage('Inserisci tutti i campi, per favore.', QMessageBox.Icon.Warning, 'Errore')
				return
		
		styleSheet = f"color: rgb(0, 170, 0); font-family: Arial; font-size: 10pt"
		if [self.lineEditEmail.styleSheet(), self.lineEditCellulare.styleSheet(), self.lineEditIBAN.styleSheet()] != [styleSheet] * 3: # se le 3 line edit non hanno il testo verde
			self._showMessage('I dati in rosso non sono accettabili.\nQuando lo saranno il loro colore diventerà verde.', QMessageBox.Icon.Warning, 'Errore')
			return

		if not NuovoDipendenteUI.hasBtnAvantiBeenClicked:
			loadUi('ui/Titolare/inserisciDipendente2.ui', self)
			NuovoDipendenteUI.hasBtnAvantiBeenClicked = True
		else:
			self.addTab(self.tabInserisciDipendente2, 'Inserisci Dipendente')  # type: ignore

		self.removeTab(0)
		
		if not NuovoDipendenteUI.hasBtnIndietroBeenClicked: # per evitare operazioni già effettuate
			self._addAndConnectEye()																	# almeno 8 caratteri, almeno una maiuscola, una minuscola e un numero
			self.lineEditPassword.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$")))
			self.btnIndietro.clicked.connect(self._indietroClicked)
			self.btnInserisci.clicked.connect(self._inserisciDipendenteClicked)
		

	def _addAndConnectEye(self):
		def showHidePassword(checked):
			if checked:
				self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
				showPasswordAction.setIcon(QtGui.QIcon('files/icons/eye-close.jpg'))
			else:
				self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
				showPasswordAction.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))
		
		showPasswordAction = QAction(QtGui.QIcon('files/icons/eye-open.jpg'), 'show/hide password', self.lineEditPassword)
		self.lineEditPassword.addAction(showPasswordAction, QLineEdit.ActionPosition.TrailingPosition) # azione aggiunta nella parte destra della line edit
		showPasswordAction.setCheckable(True)
		showPasswordAction.toggled.connect(showHidePassword)
	
	
	def _indietroClicked(self):
		if not NuovoDipendenteUI.hasBtnIndietroBeenClicked: # per evitare di risettarlo a True ad ogni click di "indietro"
			NuovoDipendenteUI.hasBtnIndietroBeenClicked = True
		self.addTab(self.tabInserisciDipendente1, 'Inserisci Dipendente')  # type: ignore
		self.removeTab(0)
				
	
	def _inserisciDipendenteClicked(self):
		def isPasswordCorrect() -> bool:
			toReturn = True
			if self.lineEditPassword.validator().validate(self.lineEditPassword.text(), 0) != QtGui.QValidator.State.Acceptable:
				self._showMessage('La password non rispetta la struttura richiesta.', QMessageBox.Icon.Warning, 'Errore')
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
		
		paths = GestoreFile.leggiJson(Path('paths.json'))
		if isPasswordCorrect() and not isUsernameUsed(paths):
			datiAggiuntivi = {
				'IBAN' : self.lineEditIBAN.text(),
				'turno' : True if self.comboBoxTurno.currentText() == 'Mattina' else False,
				'ruolo' : Ruolo.RECEPTIONIST if self.comboBoxRuolo.currentText() == 'Receptionist' else Ruolo.CAMERIERE,
				'username' : self.lineEditUsername.text(),
				'password' : encrypt(self.lineEditPassword.text())
			}
			GestorePersona.aggiungiPersona(Path(paths['dipendenti']), self.lineEditNome.text(), self.lineEditCognome.text(), 
										   self.dateEdit.date().toPyDate(), self.lineEditLuogoNascita.text(), 
										   self.lineEditEmail.text(), self.lineEditCellulare.text(), **datiAggiuntivi)
			self._showMessage('Il dipendente è stato inserito con successo!', QMessageBox.Icon.Information)
			self.close()
	

	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = NuovoDipendenteUI()
	mainWidget.show()
	sys.exit(app.exec_())