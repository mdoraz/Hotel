from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

from src.Attori.Dipendente import Dipendente
from src.Attori.Ruolo import Ruolo
from src.GUI.GestioneDipendenti.InserimentoCredenzialiDipendenteUI import InserimentoCredenzialiDipendenteUI
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.encrypter import encrypt, decrypt

class VisualizzaDipendenteUI(QWidget):

	showComboBox = False
	dipendenteEliminato = QtCore.pyqtSignal()

	def __init__(self, dipendente : Dipendente, parent : QWidget = None):  # type: ignore
		super().__init__(parent)

		loadUi(GestoreFile.absolutePath('visualizzaDipendente.ui', Path.cwd()), self)

		self.dipendente = dipendente
		self._fillFields() # riempio tutti i campi
		self._createComboBoxes() # creo le combo box di ruilo e turno da mostrare in caso di modifica
		self._setValidators() # imposto validator e colori per il testo per IBAN, stipendio, email e cellulare
		self._connectButtons()

		self.msg = QMessageBox() # perr futuri messaggi


	def _readDipendenti(self):
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dipendenti = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		except TypeError:
			self._showMessage(f"{Path(paths['dipendenti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		
		return dipendenti

	def _fillFields(self):
		# riempio l'intestazione
		self.labelIntestazioneNome.setText(f"{self.dipendente.getNome()} {self.dipendente.getCognome()}")
		self.labelIntestazioneID.setText(f"ID: {self.dipendente.getId()}")
		# riempio i dati personali
		self.labelNome.setText(self.dipendente.getNome())
		self.labelCognome.setText(self.dipendente.getCognome())
		self.labelDataNascita.setText(self.dipendente.getDataNascita().strftime('%d/%m/%Y'))
		self.labelLuogoNascita.setText(self.dipendente.getLuogoNascita())
		# riempio i dati lavorativi
		self.lineEditRuolo.setText(self.dipendente.getAutorizzazione().name.capitalize())
		self.lineEditTurno.setText('Mattina' if self.dipendente.getTurno() == 1 else 'Pomeriggio')
		self.lineEditIBAN.setText(self.dipendente.getIBAN())
		self.lineEditStipendio.setText(f"{self.dipendente.getStipendio()}")
		# riempio i contatti
		self.lineEditEmail.setText(self.dipendente.getEmail())
		self.lineEditCellulare.setText(self.dipendente.getCellulare())
		# riempio le credenziali
		self.lineEditUsername.setText(self.dipendente.getUsername())
		self.lineEditPassword.setText('password')

	
	def _createComboBoxes(self):
		self.comboBoxRuolo = QComboBox()
		self.comboBoxRuolo.addItems(['Receptionist', 'Cameriere'])
		self.comboBoxRuolo.setCurrentText(self.dipendente.getAutorizzazione().name.capitalize())

		self.comboBoxTurno = QComboBox()
		self.comboBoxTurno.addItems(['Mattina', 'Pomeriggio'])
		self.comboBoxTurno.setCurrentText('Mattina' if self.dipendente.getTurno() == True else 'Pomeriggio')

	
	def _setValidators(self):
		self.lineEditIBAN.setValidator(GUIUtils.validators['IBAN'])
		self.lineEditStipendio.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]{3,4}")))
		self.lineEditEmail.setValidator(GUIUtils.validators['email'])
		self.lineEditCellulare.setValidator(GUIUtils.validators['cellulare'])


	def _connectButtons(self):
		self.btnDatiLavorativi.clicked.connect(self._modificaDatiLavorativiClicked)
		self.btnContatti.clicked.connect(self._modificaContattiClicked)
		self.btnCredenziali.clicked.connect(self._modificaCredenzialiClicked)
		self.btnElimina.clicked.connect(self._btnEliminaClicked)

	
	def _modificaDatiLavorativiClicked(self):
		self.btnDatiLavorativi.setText('Salva')
		self.btnDatiLavorativi.clicked.disconnect(self._modificaDatiLavorativiClicked)
		self.btnDatiLavorativi.clicked.connect(self._salvaDatiLavoraiviClicked)
		
		# sostituisco le line edit di ruolo e turno con due combo
		row, ruolo = self.groupBoxDatiLavorativi.layout().getWidgetPosition(self.lineEditRuolo) # recupero la riga di linEditRuolo nella group box in cui si trova
		rowResult = self.groupBoxDatiLavorativi.layout().takeRow(row) # rimuove dal layout la riga 'row' e la restituisce
		rowResult.fieldItem.widget().hide() # nascondo self.lineEditRuolo
		if self.showComboBox == True:
			self.comboBoxRuolo.show()
		self.groupBoxDatiLavorativi.layout().insertRow(row, rowResult.labelItem.widget(), self.comboBoxRuolo)
		
		row, ruolo = self.groupBoxDatiLavorativi.layout().getWidgetPosition(self.lineEditTurno)
		rowResult = self.groupBoxDatiLavorativi.layout().takeRow(row)
		rowResult.fieldItem.widget().hide() # nascondo self.lineEditTurno
		if self.showComboBox == True:
			self.comboBoxTurno.show()
		self.groupBoxDatiLavorativi.layout().insertRow(row, rowResult.labelItem.widget(), self.comboBoxTurno)
		
		# imposto le line edit di IBAN e stipendio come modificabili
		self.lineEditIBAN.setReadOnly(False)
		self.lineEditStipendio.setReadOnly(False)
		# imposto i colori del testo
		self.lineEditIBAN.textChanged.connect(self._setColorHint)
		self.lineEditStipendio.textChanged.connect(self._setColorHint)


	def _salvaDatiLavoraiviClicked(self):
		IBAN = self.lineEditIBAN.text()
		stipendio = self.lineEditStipendio.text()
		stipendioValidator = self.lineEditStipendio.validator()
		
		# controllo la validità del contenuto delle line edit di IBAN e stipendio
		if [GUIUtils.validators['IBAN'].validate(IBAN, 0)[0], stipendioValidator.validate(stipendio, 0)[0]] != [QtGui.QValidator.State.Acceptable] * 2: # se IBAN o stipendio non sono accettabili
			self._showMessage('IBAN o stipendio non sono accettabili. Ricontrollare, per favore.', QMessageBox.Icon.Warning, 'Errore')
			return
		# se tutto è corretto, modifico il dipendente visualizzato
		self.dipendente.setIBAN(IBAN)
		self.dipendente.setTurno(True if self.comboBoxTurno.currentText() == 'Mattina' else False)
		self.dipendente.setAutorizzazione(Ruolo.RECEPTIONIST if self.comboBoxRuolo.currentText() == 'Receptionist' else Ruolo.CAMERIERE)

		if stipendio != str(self.dipendente.getStipendio()): # se lo stipendio è stato cambiato manualmente
			self.dipendente.setStipendio(stipendio)
		else:
			self.dipendente.setStipendio(1000 if self.dipendente.getAutorizzazione().name == 'CAMERIERE' else 1200) # lo stipendio si adatta al nuovo ruolo
			self.lineEditStipendio.setText(str(self.dipendente.getStipendio())) # cambio valore della line edit
		
		self._salvaDipendente()
		
		# il bottone torna ad essere connesso alla modifica
		self.btnDatiLavorativi.setText('Modifica')
		self.btnDatiLavorativi.clicked.disconnect(self._salvaDatiLavoraiviClicked)
		self.btnDatiLavorativi.clicked.connect(self._modificaDatiLavorativiClicked)
		
		# sostituisco le combo box di ruolo e turno con line edit immodificabili
		row, role = self.groupBoxDatiLavorativi.layout().getWidgetPosition(self.comboBoxRuolo) # recupero la riga di comboBoxRuolo nella group box in cui si trova
		rowResult = self.groupBoxDatiLavorativi.layout().takeRow(row) # rimuove dal layout la riga 'row' e la restituisce
		rowResult.fieldItem.widget().hide() # nascondo self.comboBoxRuolo
		self.lineEditRuolo.setText(rowResult.fieldItem.widget().currentText())
		self.lineEditRuolo.show()
		self.groupBoxDatiLavorativi.layout().insertRow(row, rowResult.labelItem.widget(), self.lineEditRuolo)

		row, role = self.groupBoxDatiLavorativi.layout().getWidgetPosition(self.comboBoxTurno)
		rowResult = self.groupBoxDatiLavorativi.layout().takeRow(row)
		rowResult.fieldItem.widget().hide() # nascondo self.comboBoxTurno
		self.lineEditTurno.setText(rowResult.fieldItem.widget().currentText())
		self.lineEditTurno.show()
		self.groupBoxDatiLavorativi.layout().insertRow(row, rowResult.labelItem.widget(), self.lineEditTurno)

		if self.showComboBox == False:
			self.showComboBox = True # la prossima volta che verrà cliccato 'modifica' verranno mostrate le combo box, visto che sono state nascoste precedentemente in questo metodo
		
		# le line edit non sono piu modificabili
		self.lineEditIBAN.setReadOnly(True)
		self.lineEditStipendio.setReadOnly(True)
		# rimossi i colori del testo
		self.lineEditIBAN.setStyleSheet("font-family: Arial; font-size: 11pt")
		self.lineEditStipendio.setStyleSheet("font-family: Arial; font-size: 11pt")


	def _modificaContattiClicked(self):
		self.btnContatti.setText('Salva')
		self.btnContatti.clicked.disconnect(self._modificaContattiClicked)
		self.btnContatti.clicked.connect(self._salvaContattiClicked)
		
		# imposto le line edit di IBAN e stipendio come modificabili
		self.lineEditEmail.setReadOnly(False)
		self.lineEditCellulare.setReadOnly(False)
		# imposto i colori del testo
		self.lineEditEmail.textChanged.connect(self._setColorHint)
		self.lineEditCellulare.textChanged.connect(self._setColorHint)

	
	def _salvaContattiClicked(self):
		email = self.lineEditEmail.text()
		cellulare = self.lineEditCellulare.text()

		# controllo la validità del contenuto delle line edit
		if [GUIUtils.validators['email'].validate(email, 0)[0], GUIUtils.validators['cellulare'].validate(cellulare, 0)[0]] != [QtGui.QValidator.State.Acceptable] * 2: # se email o cellulare non sono accettabili
			self._showMessage('Email o cellulare non sono accettabili. Ricontrollare, per favore.', QMessageBox.Icon.Warning, 'Errore')
			return

		self.dipendente.setEmail(email)
		self.dipendente.setCellulare(cellulare)

		self._salvaDipendente()

		# il bottone torna ad essere connesso alla modifica
		self.btnContatti.setText('Modifica')
		self.btnContatti.clicked.disconnect(self._salvaContattiClicked)
		self.btnContatti.clicked.connect(self._modificaContattiClicked)
		
		# le line edit non sono piu modificabili
		self.lineEditEmail.setReadOnly(True)
		self.lineEditCellulare.setReadOnly(True)
		# rimossi i colori del testo
		self.lineEditEmail.setStyleSheet("font-family: Arial; font-size: 11pt")
		self.lineEditCellulare.setStyleSheet("font-family: Arial; font-size: 11pt")


	def _modificaCredenzialiClicked(self):
		self.modificaCredenzialiWidget = InserimentoCredenzialiDipendenteUI()
		self.modificaCredenzialiWidget.setWindowTitle('Modifica credenziali')
		self.modificaCredenzialiWidget.addField(3, 'Vecchia password')

		# monkey patching per aggiungere a runtime label e line edit della vecchia password agli attributi di credenzialiWidget
		self.modificaCredenzialiWidget.labelVecchiaPassword = self.modificaCredenzialiWidget.layout().itemAt(3).widget().layout().itemAtPosition(0,1).widget()
		self.modificaCredenzialiWidget.lineEditVecchiaPassword = self.modificaCredenzialiWidget.layout().itemAt(3).widget().layout().itemAtPosition(1,1).widget()
		#self.modificaCredenzialiWidget.lineEditLabelPairs[self.modificaCredenzialiWidget.lineEditVecchiaPassword] = self.modificaCredenzialiWidget.labelVecchiaPassword

		# vecchia password nascosta, aggiornato il campo relatio alla password, username ha inizialmente line edit piena e label visibile
		self.modificaCredenzialiWidget.lineEditVecchiaPassword.setEchoMode(QLineEdit.EchoMode.Password)
		self.modificaCredenzialiWidget.lineEditPassword.setPlaceholderText('Nuova password')
		self.modificaCredenzialiWidget.labelPassword.setText('Nuova password')
		self.modificaCredenzialiWidget.lineEditUsername.setText(self.dipendente.getUsername())
		self.modificaCredenzialiWidget.labelUsername.show()
		
		self.modificaCredenzialiWidget.btnIndietro.clicked.connect(self.modificaCredenzialiWidget.close)
		self.modificaCredenzialiWidget.btnInserisci.setText('Salva modifiche')
		self.modificaCredenzialiWidget.btnInserisci.clicked.connect(self._salvaCredenzialiClicked)
		self.modificaCredenzialiWidget.show()
		
	
	def _salvaCredenzialiClicked(self):
		usernameChanged = passwordChanged = False
		# se lo username è vuoto o contiene solo spazi
		if self.modificaCredenzialiWidget.lineEditUsername.text().strip() == '':
			self._showMessage('Username non valido.', QMessageBox.Icon.Warning, 'Errore')
			return
		# se è stato cambiato username
		if self.modificaCredenzialiWidget.lineEditUsername.text() != self.dipendente.getUsername():
			# se non è già in uso da un altro utente
			if not self.modificaCredenzialiWidget.isUsernameUsed():
				self.dipendente.setUsername(self.modificaCredenzialiWidget.lineEditUsername.text())
				self.lineEditUsername.setText(self.dipendente.getUsername())
				usernameChanged = True
			else:
				return
		
		lineEditLabelPairs = {
			self.modificaCredenzialiWidget.lineEditVecchiaPassword : self.modificaCredenzialiWidget.labelVecchiaPassword,
			self.modificaCredenzialiWidget.lineEditPassword : self.modificaCredenzialiWidget.labelPassword,
			self.modificaCredenzialiWidget.lineEditConfermaPassword : self.modificaCredenzialiWidget.labelConfermaPassword
		}
		# se almeno una delle line edit delle password non è vuota
		if (self.modificaCredenzialiWidget.lineEditVecchiaPassword.text().strip() != '' or
			self.modificaCredenzialiWidget.lineEditPassword.text().strip() != '' or
			self.modificaCredenzialiWidget.lineEditConfermaPassword.text().strip() != ''):
			# se non sono tutte piene
			if not self.modificaCredenzialiWidget.fieldsFilled(lineEditLabelPairs):
				self._showMessage('Se si vuole modificare la password, inserire tutti i campi relativi alle password.\nSe non si vuole modificarla, lasciare vuoti tutti i campi.',
								  QMessageBox.Icon.Warning, 'Errore')
				self.modificaCredenzialiWidget.msg.hide()
				return
			# se la vecchia password non è corretta
			elif self.modificaCredenzialiWidget.lineEditVecchiaPassword.text() != decrypt(self.dipendente.getPassword()):
				self._showMessage('La vecchia password non è corretta, riprovare.', QMessageBox.Icon.Warning, 'Errore')
				return
			# se la password rispetta la struttura specificata e coincide con la conferma password
			if self.modificaCredenzialiWidget.isPasswordCorrect():
				self.dipendente.setPassword(encrypt(self.modificaCredenzialiWidget.lineEditPassword.text()))
				passwordChanged = True
			else:
				return
		
		# se sono avvenute modifiche, le salvo e imposto il messaggio da mostrare alla fine
		if usernameChanged and passwordChanged:
			self._salvaDipendente()
			msg = 'Username e password modificati con successo!'
		elif usernameChanged:
			self._salvaDipendente()
			msg = 'Username modificato con successo!'
		elif passwordChanged:
			self._salvaDipendente()
			msg = 'Password modificata con successo!'
		else:
			msg = ''

		if msg != '':
			self._showMessage(msg, QMessageBox.Icon.Warning, 'Errore')
		self.modificaCredenzialiWidget.close()


	def _btnEliminaClicked(self):
		richiestaConferma = QMessageBox()
		richiestaConferma.setIcon(QMessageBox.Icon.Warning)
		richiestaConferma.setWindowTitle('ConfermaEliminazione')
		richiestaConferma.setText("Sei sicuro di voler eliminare dal sistema questo dipendente?")
		siButton = richiestaConferma.addButton('Si', QMessageBox.ButtonRole.YesRole)
		noButton = richiestaConferma.addButton(QMessageBox.StandardButton.No)
		richiestaConferma.exec()

		if richiestaConferma.clickedButton() == noButton:
			pass # non accade nulla, eliminazione annullata
		else:
			dipendenti = self._readDipendenti()
			del dipendenti[self.dipendente.getId()]
			paths = GestoreFile.leggiJson(Path('paths.json'))
			GestoreFile.salvaPickle(dipendenti, Path(paths['dipendenti']))
			self.dipendenteEliminato.emit()
			self._showMessage('Dipendente eliminato dal sistema!', QMessageBox.Icon.Information)
			self.close()


	

	def _setColorHint(self, text): # text è il testo della line edit da controllare
		fontType = "font-family: Arial; font-size: 11pt"
		lineEdit = self.sender()
		
		if text != '' and lineEdit.validator().validate(text, 0)[0] == QtGui.QValidator.State.Acceptable: # se il testo è accettato dal validator
			if lineEdit.styleSheet() != f"color: rgb(0, 170, 0); {fontType}":
				lineEdit.setStyleSheet(f"color: rgb(0, 170, 0); {fontType}") # il testo diventa verde
		
		elif lineEdit.styleSheet() != f"color: rgb(255, 0, 0); {fontType}":
			lineEdit.setStyleSheet(f"color: rgb(255, 0, 0); {fontType}") # il testo diventa rosso


	def _salvaDipendente(self):
		# salvo le modifihe su file
		dipendenti = self._readDipendenti()
		dipendenti[self.dipendente.getId()] = self.dipendente
		paths = GestoreFile.leggiJson(Path('paths.json'))
		GestoreFile.salvaPickle(dipendenti, Path(paths['dipendenti']))

	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
