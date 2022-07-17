from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GUI.SelezionaDaListaUI import SelezionaDaLista
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.customQtClasses import MyTreeWidgetItem
from src.Utilities.exceptions import CorruptedFileError


class RicercaClienteUI(QTabWidget):
	
	clienteTrovato = QtCore.pyqtSignal(Persona)

	def __init__(self, previous: QWidget):
		super().__init__()

		loadUi(GestoreFile.absolutePath('ricercaCliente.ui', Path.cwd()), self)
		
		self.previous = previous
		
		self._connectGroupBoxes() # solo una groupbox alla volta può essere checkata
		self._setValidators() # impostati i validator per le line edit
		self._setUpperCase() # maiuscola automatica per nome e cognome
		self._connectButtons()

		self.msg = QMessageBox()

	
	def _setValidators(self):
		self.lineeditNome.setValidator(GUIUtils.validators['soloLettere'])
		self.lineeditCognome.setValidator(GUIUtils.validators['soloLettere'])
		self.lineeditID.setValidator(GUIUtils.validators['soloNumeri'])


	def _setUpperCase(self):
		def textToUpper(oldPos, newPos):
			if oldPos == 0 and newPos == 1:
				lineEdit = self.sender()
				text = lineEdit.text()
				lineEdit.setText(text[0].upper() + text[1:])
	
		self.lineeditNome.cursorPositionChanged.connect(textToUpper)
		self.lineeditCognome.cursorPositionChanged.connect(textToUpper)
	

	def _connectGroupBoxes(self):
		self.groupboxCognomeNome.clicked.connect(lambda checked: self.groupboxID.setChecked(not checked)) # il click di groupboxCognomeNome influenza groupboxID
		self.groupboxID.clicked.connect(lambda checked: self.groupboxCognomeNome.setChecked(not checked)) # il click di groupboxID influenza groupboxCognomeNome
	

	def _connectButtons(self):
		self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)


	def _btnRicercaClienteClicked(self):
		def onClienteTrovato(cliente : Persona, windowToClose : QWidget):
			self.clienteTrovato.emit(cliente)
			windowToClose.close()

		if self.groupboxID.isChecked():
			if self.lineeditID.text().strip() == '': #se l'id è vuoto
				self._showMessage("Inserire l'ID per effettuare la ricerca, oppure selezionare un'altra modalità di ricerca.", 
								  QMessageBox.Icon.Warning, 'Errore')
				return
			id = int(self.lineeditID.text())
			clienti = self._readClienti()
			for cliente in clienti.values():
				if cliente.getId() == id:
					onClienteTrovato(cliente, self)
					return
			self._showMessage("Nessun cliente trovato con l'ID inserito.", QMessageBox.Icon.Warning, 'Errore')
		
		elif self.groupboxCognomeNome.isChecked():
			if self.lineeditCognome.text().strip() == '': # se il cognome è vuoto
				self._showMessage("Inserire il cognome per effettuare la ricerca, oppure selezionare un'altra modalità di ricerca.", 
								  QMessageBox.Icon.Warning, 'Errore')
				return
			cognome = self.lineeditCognome.text()
			clienti = self._readClienti()
			riscontri = []
			for cliente in clienti.values():
				if cliente.getCognome() == cognome:
					riscontri.append(cliente)
			if len(riscontri) == 0:
				self._showMessage(f"Non è stato trovato nessun cliente con il cognome '{cognome}'.", QMessageBox.Icon.Warning, 'Errore')
				return
			
			if self.lineeditNome.text().strip() != '':
				riscontriCognome = riscontri.copy() # copio la lista dei clienti col cognome inserito, prima di svuotarla
				riscontri.clear() # svuoto la lista di riscontri perchè sarà riempita dai clienti che hanno, oltre al cognome, anche il nome uguale a quello inserito
				nome = self.lineeditNome.text()
				for cliente in riscontriCognome:
					if cliente.getNome() == nome:
						riscontri.append(cliente)
				if len(riscontri) == 0:
					self._showMessage(f"Non è stato trovato nessun cliente che si chiama {nome} {cognome}.", QMessageBox.Icon.Warning, 'Errore')
					return
			
			# a questo punto del codice ho la lista riscontri non vuota che contiene i clienti con cognome (e nome, se inserito) che corrispondono a quelli inseriti
			if len(riscontri) == 1: # se un solo cliente corrisponde ai criteri di ricerca
				onClienteTrovato(riscontri[0], self)
			else:
				# mostro la lista di riscontri. l'utente selezionerà quello di interesse
				self.widgetClienti = SelezionaDaLista()
				self.widgetClienti.label.setText('Selezionare il cliente di interesse.')
				self.widgetClienti.treeWidget.setHeaderLabels(['ID', 'Cognome', 'Nome'])
				for cliente in riscontri:
					self.widgetClienti.treeWidget.addTopLevelItem(MyTreeWidgetItem(self.widgetClienti.treeWidget,
																			  [str(cliente.getId()), cliente.getCognome(), cliente.getNome()],
																			  cliente))
				self.widgetClienti.show()
				self.close()
				self.widgetClienti.treeWidget.itemDoubleClicked.connect(lambda item, column: onClienteTrovato(item.connectedObject, self.widgetClienti))


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()
	

	def _readClienti(self):
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			clienti = GestoreFile.leggiDictPickle(Path(paths['clienti']))
		except CorruptedFileError:
			self._showMessage(f"{Path(paths['clienti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		
		return clienti

	
	def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
