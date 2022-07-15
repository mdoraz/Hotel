from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaClienteUI import RicercaClienteUI
from src.GUI.FormUI import FormUI
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.GUIUtils import GUIUtils


class VisualizzaClienteUI(FormUI):

	clienteEliminato = QtCore.pyqtSignal()

	def __init__(self, cliente : Persona = None, previous : QWidget = None): # type: ignore
		super().__init__()

		loadUi(GestoreFile.absolutePath('visualizzaCliente.ui', Path.cwd()), self)

		self.previous = previous
		self.cliente = cliente
		
		if cliente != None: # se è stato passato un cliente al costruttore, mostro i suoi dati
			self._fillFields(self.cliente)
		else: # altrimenti nascondo i campi vuoti per fare prima ricercare il cliente
			self._hideElements()

		self._setValidators()
		self._connectButtons()
		self.msg = QMessageBox()

	
	def _hideElements(self):
		self.groupboxSchedaCliente.hide()
		self.btnModificaContatti.hide()
		self.btnElimina.hide()

	
	def _setValidators(self):
		self.lineeditEmail.setValidator(GUIUtils.validators['email'])
		self.lineeditCellulare.setValidator(GUIUtils.validators['cellulare'])


	def _connectButtons(self):
		self.btnRicerca.clicked.connect(self._btnRicercaClicked)
		self.btnModificaContatti.clicked.connect(self._modificaContattiClicked)
		self.btnElimina.clicked.connect(self._btnEliminaClicked)

	
	def _btnRicercaClicked(self):
		self.widgetRicercaCliente = RicercaClienteUI(self)
		self.widgetRicercaCliente.clienteTrovato.connect(self._onClienteTrovato)
		self.widgetRicercaCliente.show()

	
	def _onClienteTrovato(self, cliente):
		self.cliente = cliente
		self._fillFields(cliente)
	

	def _fillFields(self, cliente : Persona):
		self.lineeditID.setText(str(cliente.getId()))
		self.lineeditNome.setText(cliente.getNome())
		self.lineeditCognome.setText(cliente.getCognome())
		self.lineeditLuogoNascita.setText(cliente.getLuogoNascita())
		self.lineeditEmail.setText(cliente.getEmail())
		self.lineeditCellulare.setText(cliente.getCellulare())
		self.dateedit.setDate(cliente.getDataNascita())
		if self.groupboxSchedaCliente.isHidden():
			self.groupboxSchedaCliente.show()
			self.btnModificaContatti.show()
			self.btnElimina.show()


	def _modificaContattiClicked(self):
		self.btnModificaContatti.clicked.disconnect(self._modificaContattiClicked)
		self.btnModificaContatti.clicked.connect(self._salvaModificheClicked)
		self.btnModificaContatti.setText('Salva modifiche')

		# imposto le line edit di email e cellulare come modificabili
		self.lineeditEmail.setReadOnly(False)
		self.lineeditCellulare.setReadOnly(False)
		# imposto i colori del testo
		self.lineeditEmail.textChanged.connect(self._setColorHint)
		self.lineeditCellulare.textChanged.connect(self._setColorHint)

	
	def _salvaModificheClicked(self):
		email = self.lineeditEmail.text()
		cellulare = self.lineeditCellulare.text()

		# controllo la validità del contenuto delle line edit
		if [GUIUtils.validators['email'].validate(email, 0)[0], GUIUtils.validators['cellulare'].validate(cellulare, 0)[0]] != [QtGui.QValidator.State.Acceptable] * 2: # se email o cellulare non sono accettabili
			self._showMessage('Email o cellulare non sono accettabili. Ricontrollare, per favore.', QMessageBox.Icon.Warning, 'Errore')
			return
		
		self.cliente.setEmail(email)
		self.cliente.setCellulare(cellulare)

		self._salvaCliente()

		# il bottone torna ad essere connesso alla modifica
		self.btnModificaContatti.setText('Modifica contatti')
		self.btnModificaContatti.clicked.disconnect(self._salvaModificheClicked)
		self.btnModificaContatti.clicked.connect(self._modificaContattiClicked)
		
		# le line edit non sono piu modificabili
		self.lineeditEmail.setReadOnly(True)
		self.lineeditCellulare.setReadOnly(True)
		# rimossi i colori del testo
		self.lineeditEmail.textChanged.disconnect(self._setColorHint)
		self.lineeditCellulare.textChanged.disconnect(self._setColorHint)
		font = self.lineeditEmail.font()
		self.lineeditEmail.setStyleSheet("")
		self.lineeditCellulare.setStyleSheet("")
		# uno style sheet vuoto resetta anche il font della line edit, quindi va reimpostato
		self.lineeditEmail.setFont(font)
		self.lineeditCellulare.setFont(font)
		
	
	def _btnEliminaClicked(self):
		richiestaConferma = QMessageBox()
		richiestaConferma.setIcon(QMessageBox.Icon.Warning)
		richiestaConferma.setWindowTitle('ConfermaEliminazione')
		richiestaConferma.setText("Confermi l'eliminazione di questo cliente?")
		richiestaConferma.addButton('Si', QMessageBox.ButtonRole.YesRole)
		noButton = richiestaConferma.addButton(QMessageBox.StandardButton.No)
		richiestaConferma.exec()

		if richiestaConferma.clickedButton() == noButton:
			pass # non accade nulla, eliminazione annullata
		else:
			clienti = self._readDict('clienti')
			try: 
				del clienti[self.cliente.getId()]
			except KeyError: # nel caso in cui arrivo alla visualizzazione senza passare per la ricerca (che cerca in clienti.pickle)
				self._showMessage('Cliente non presente nel sistema.', QMessageBox.Icon.Warning, 'Errore')
				return
			GestoreFile.salvaPickle(clienti, Path(paths['clienti']))
			self.clienteEliminato.emit()
			self._showMessage('Cliente eliminato dal sistema!', QMessageBox.Icon.Information)
			self._hideElements()

			# rimuovere le prenotazioni a nome di quel cliente
			camere : dict[int, Camera] = self._readDict('camere')
			for camera in camere.values():
				for prenotazione in camera.getPrenotazioni():
					if prenotazione.getNominativo().getId() == self.cliente.getId():
						camera.eliminaPrenotazione(prenotazione)
			GestoreFile.salvaPickle(camere, Path(paths['camere']))
		

	def _salvaCliente(self):
		clienti = self._readDict('clienti')
		clienti[self.cliente.getId()] = self.cliente
		GestoreFile.salvaPickle(clienti, Path(paths['clienti']))
	

	def _readDict(self, pathsKey : str) -> dict:
		global paths
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dictionary = GestoreFile.leggiDictPickle(Path(paths[pathsKey]))
		except TypeError:
			self._showMessage(f"{Path(paths[pathsKey]).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		return dictionary
	

	def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
