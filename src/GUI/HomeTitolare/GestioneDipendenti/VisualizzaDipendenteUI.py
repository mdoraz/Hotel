from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

from src.Attori.Dipendente import Dipendente
from src.Attori.Ruolo import Ruolo
from src.GUI.HomeTitolare.GestioneDipendenti.FormUI import FormUI
from src.GUI.HomeTitolare.GestioneDipendenti.InserimentoCredenzialiUI import InserimentoCredenzialiUI
from src.GUI.HomeTitolare.GestioneDipendenti.VisualizzaAssenzeUI import VisualizzaAssenzeUI
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.encrypter import encrypt, decrypt


class VisualizzaDipendenteUI(FormUI):

	showComboBox = False
	dipendenteEliminato = QtCore.pyqtSignal()
	turnoModificato = QtCore.pyqtSignal(Dipendente, bool)

	def __init__(self, dipendente : Dipendente, parent : QWidget = None):  # type: ignore
		super().__init__(parent)

		loadUi(GestoreFile.absolutePath('visualizzaDipendente.ui', Path.cwd()), self)

		self.dipendente = dipendente
		self._fillFields() # riempio tutti i campi
		self._createComboBoxes() # creo le combo box di ruilo e turno da mostrare in caso di modifica
		self._setValidators() # imposto validator e colori per il testo per IBAN, stipendio, email e cellulare
		self._connectButtons()


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
		self.btnModificaDatiLavorativi.clicked.connect(self._btnModificaDatiLavorativiClicked)
		self.btnModificaContatti.clicked.connect(self._btnModificaContattiClicked)
		self.btnCredenziali.clicked.connect(self._mostraCredenziali)
		self.btnAssenze.clicked.connect(self._mostraAssenze)
		self.btnElimina.clicked.connect(self._btnEliminaClicked)

	
	def _btnModificaDatiLavorativiClicked(self):
		self.btnModificaDatiLavorativi.setText('Salva')
		self.btnModificaDatiLavorativi.clicked.disconnect(self._btnModificaDatiLavorativiClicked)
		self.btnModificaDatiLavorativi.clicked.connect(self._salvaDatiLavoraiviClicked)
		
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
		self.dipendente.setAutorizzazione(Ruolo.RECEPTIONIST if self.comboBoxRuolo.currentText() == 'Receptionist' else Ruolo.CAMERIERE)
		turno = 'Mattina' if self.dipendente.getTurno() == True else 'Pomeriggio'
		if turno != self.comboBoxTurno.currentText():
			self.dipendente.setTurno(True if self.comboBoxTurno.currentText() == 'Mattina' else False)
			self.turnoModificato.emit(self.dipendente, self.dipendente.getTurno()) # emetto il segnale passando il nuovo turno del dipendente

		if stipendio != str(self.dipendente.getStipendio()): # se lo stipendio è stato cambiato manualmente
			self.dipendente.setStipendio(stipendio)
		else:
			self.dipendente.setStipendio(1000 if self.dipendente.getAutorizzazione().name == 'CAMERIERE' else 1200) # lo stipendio si adatta al nuovo ruolo
			self.lineEditStipendio.setText(str(self.dipendente.getStipendio())) # cambio valore della line edit
		
		self._salvaDipendente()
		
		# il bottone torna ad essere connesso alla modifica
		self.btnModificaDatiLavorativi.setText('Modifica')
		self.btnModificaDatiLavorativi.clicked.disconnect(self._salvaDatiLavoraiviClicked)
		self.btnModificaDatiLavorativi.clicked.connect(self._btnModificaDatiLavorativiClicked)
		
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
		self.lineEditIBAN.textChanged.disconnect(self._setColorHint)
		self.lineEditStipendio.textChanged.disconnect(self._setColorHint)


	def _btnModificaContattiClicked(self):
		self.btnModificaContatti.setText('Salva')
		self.btnModificaContatti.clicked.disconnect(self._btnModificaContattiClicked)
		self.btnModificaContatti.clicked.connect(self._salvaContattiClicked)
		
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
		self.btnModificaContatti.setText('Modifica')
		self.btnModificaContatti.clicked.disconnect(self._salvaContattiClicked)
		self.btnModificaContatti.clicked.connect(self._btnModificaContattiClicked)
		
		# le line edit non sono piu modificabili
		self.lineEditEmail.setReadOnly(True)
		self.lineEditCellulare.setReadOnly(True)
		# rimossi i colori del testo
		self.lineEditEmail.setStyleSheet("font-family: Arial; font-size: 11pt")
		self.lineEditCellulare.setStyleSheet("font-family: Arial; font-size: 11pt")
		self.lineEditEmail.textChanged.disconnect(self._setColorHint)
		self.lineEditCellulare.textChanged.disconnect(self._setColorHint)


	def _mostraCredenziali(self):
		self.credenzialiWidget = InserimentoCredenzialiUI()
		self.vecchiaPasswordAdded = False # al primo click sul bottone modifica, saranno aggiunti label e line edit per la vecchia password
		
		self.credenzialiWidget.setWindowTitle('Modifica credenziali')
		self.credenzialiWidget.labelIntestazione.hide()
		
		self.credenzialiWidget.lineEditUsername.setText(self.dipendente.getUsername()) # username inizialmente ha line edit piena
		self.credenzialiWidget.labelUsername.show()									# e label visibile
		self._widgetCredenzialiSoloVisualizzazione()
		self.credenzialiWidget.show()
		

	def _widgetCredenzialiSoloVisualizzazione(self): # configura credenzialiWidget per la sola visualizzazione
		self.credenzialiWidget.lineEditUsername.setReadOnly(True)
		self.credenzialiWidget.lineEditPassword.setReadOnly(True)

		self.credenzialiWidget.labelIstruzioniPassword.hide()
		self.credenzialiWidget.lineEditConfermaPassword.hide() # nascondo conferma password
		self.credenzialiWidget.lineEditVecchiaPassword.hide() # e vecchia password
		
		self.credenzialiWidget.lineEditPassword.setText('password') # per riempire la password con pallini neri
		self.credenzialiWidget.lineEditPassword.actions()[0].defaultWidget().hide() # nascondo l'occhiolino
		self.credenzialiWidget.labelPassword.show()

		self.credenzialiWidget.btnInserisci.setText('Modifica')
		try:
			self.credenzialiWidget.btnInserisci.clicked.disconnect(self._salvaCredenzialiClicked)
			self.credenzialiWidget.lineEditVecchiaPassword.hide() # se riesco a disconnettere btnInserisci senza andare in eccezione, è stato cliccato almeno una volta il bottone modifica
			self.credenzialiWidget.labelPassword.setText('Password')
		except:
			pass
		self.credenzialiWidget.btnInserisci.clicked.connect(self._modificaCredenzialiClicked)
		self.credenzialiWidget.btnIndietro.setText('Indietro')
		self.credenzialiWidget.btnIndietro.clicked.connect(self.credenzialiWidget.close)


	def _modificaCredenzialiClicked(self):
		self.credenzialiWidget.lineEditUsername.setReadOnly(False)
		self.credenzialiWidget.lineEditPassword.setReadOnly(False)

		self.credenzialiWidget.labelIstruzioniPassword.show()
		self.credenzialiWidget.lineEditConfermaPassword.show()
		self.credenzialiWidget.lineEditVecchiaPassword.show()
		
		# aggiornate label e line edit relative alla password
		self.credenzialiWidget.lineEditPassword.setText('')
		self.credenzialiWidget.lineEditPassword.setPlaceholderText('Nuova password')
		self.credenzialiWidget.labelPassword.setText('Nuova password')
		self.credenzialiWidget.lineEditPassword.actions()[0].defaultWidget().show() # mostro l'occhiolino

		self.credenzialiWidget.btnInserisci.setText('Salva')
		self.credenzialiWidget.btnInserisci.clicked.disconnect(self._modificaCredenzialiClicked)
		self.credenzialiWidget.btnInserisci.clicked.connect(self._salvaCredenzialiClicked)
		self.credenzialiWidget.btnIndietro.setText('Annulla')
		self.credenzialiWidget.btnIndietro.clicked.disconnect(self.credenzialiWidget.close)
		self.credenzialiWidget.btnIndietro.clicked.connect(self._widgetCredenzialiSoloVisualizzazione)
		
	
	def _salvaCredenzialiClicked(self):
		
		usernameChanged = passwordChanged = False
		# se lo username è vuoto o contiene solo spazi
		if self.credenzialiWidget.lineEditUsername.text().strip() == '':
			self._showMessage('Username non valido.', QMessageBox.Icon.Warning, 'Errore')
			return
		# se è stato cambiato username
		if self.credenzialiWidget.lineEditUsername.text() != self.dipendente.getUsername():
			# se non è già in uso da un altro utente
			if not self.credenzialiWidget.isUsernameUsed():
				self.dipendente.setUsername(self.credenzialiWidget.lineEditUsername.text())
				self.lineEditUsername.setText(self.dipendente.getUsername())
				usernameChanged = True
			else:
				return
		
		# tolgo da credenzialiWidget.lineEditLabelPairs la entry dello username
		lineEditLabelPairs = {k : v for k, v in self.credenzialiWidget.lineEditLabelPairs.items() if v != self.credenzialiWidget.labelUsername}
		
		# se almeno una delle line edit delle password non è vuota
		if ([lineEdit.text().strip() for lineEdit in lineEditLabelPairs] != [''] * len(lineEditLabelPairs.keys())):
			
			# se non sono tutte piene
			if not self.credenzialiWidget.fieldsFilled(lineEditLabelPairs): # linEditLabelPairs senza username
				self._showMessage('Se si vuole modificare la password, inserire tutti i campi relativi alle password.\nSe non si vuole modificarla, lasciare vuoti tutti i campi.',
								  QMessageBox.Icon.Warning, 'Errore')
				self.credenzialiWidget.msg.hide()
				return
			# se la vecchia password non è corretta
			if self.credenzialiWidget.lineEditVecchiaPassword.text() != decrypt(self.dipendente.getPassword()):
				self._showMessage('La vecchia password non è corretta, riprovare.', QMessageBox.Icon.Warning, 'Errore')
				return

			# se la password rispetta la struttura specificata e coincide con la conferma password
			if not self.credenzialiWidget.isPasswordCorrect():
				return # l'errore opportuno è stato già mostrato dal metodo isPasswordCorrect
			else:
				self.dipendente.setPassword(encrypt(self.credenzialiWidget.lineEditPassword.text()))
				passwordChanged = True
		
		# se sono avvenute modifiche, le salvo e imposto il messaggio da mostrare alla fine
		if usernameChanged and passwordChanged:
			msg = 'Username e password modificati con successo!'
		elif usernameChanged:
			msg = 'Username modificato con successo!'
		elif passwordChanged:
			msg = 'Password modificata con successo!'
		else:
			msg = ''

		if msg != '':
			self._salvaDipendente()
			self._showMessage(msg, QMessageBox.Icon.Warning, 'Errore')
		self.credenzialiWidget.close()

	def _mostraAssenze(self):
		self.assenzeWidget = VisualizzaAssenzeUI(self.dipendente)
		self.assenzeWidget.show()


	def _btnEliminaClicked(self):
		richiestaConferma = QMessageBox()
		richiestaConferma.setIcon(QMessageBox.Icon.Warning)
		richiestaConferma.setWindowTitle('ConfermaEliminazione')
		richiestaConferma.setText("Sei sicuro di voler eliminare dal sistema questo dipendente?")
		richiestaConferma.addButton('Si', QMessageBox.ButtonRole.YesRole)
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
