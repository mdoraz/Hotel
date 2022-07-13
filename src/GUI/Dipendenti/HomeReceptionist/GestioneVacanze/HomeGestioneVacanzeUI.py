import sys
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.VisualizzaClienteUI import VisualizzaClienteUI
from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.GestioneVacanza.Vacanza import Vacanza
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.AggiungereClientiCheckInUI import AggiungereClientiCheckInUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.ModificaPrenotazioneVacanzaUI import ModificaPrenotazioneVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.ModificaTermineVacanzaOmbrelloneUI import ModificaTermineVacanzaOmbrelloneUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.RicercaPrenotazioneVacanzaUI import RicercaPrenotazioneVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.RicercaVacanzaUI import RicercaVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.SelezionaCameraUI import SelezionaCameraUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaClienteUI import RicercaClienteUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RegistraClienteUI import RegistraClienteUI
from src.Servizi.Camera import Camera
from src.Servizi.Ombrellone import Ombrellone
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.customQtClasses import MyListWidgetItem, MyTreeWidgetItem
from src.Utilities.exceptions import CorruptedFileError


class HomeGestioneVacanzeUI(QTabWidget):
	
	def __init__(self, previous: QWidget):
		super().__init__()
		
		loadUi(GestoreFile.absolutePath('HomeGestioneVacanze.ui', Path.cwd()), self)

		self.previous = previous

		self._setupInserisciPrenotazione()
		self._setupVisualizzaPrenotazione()
		self._setupVisualizzaVacanza()
		
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)

		self.msg = QMessageBox()
	
	
	def _setupInserisciPrenotazione(self):
		self._hideElementsInserisciPrenotazione()
		self._connectButtonsInserisciPrenotazione()
		self.lineeditNumeroCartaInserisciPrenotazione.setValidator(GUIUtils.validators['numeroCarta'])
		self.lineeditNumeroCartaInserisciPrenotazione.textChanged.connect(self._setNumeroCartaHints)

	def _setupVisualizzaPrenotazione(self):
		self._hideElementsVisualizzaPrenotazione()
		self._connectButtonsVisualizzaPrenotazione()
		self.treewidgetClientiCheckIn.header().resizeSection(0, 50) # restringo la prima colonna che contiene l'id
	
	def _setupVisualizzaVacanza(self):
		self._hideElementsVisualizzaVacanza()
		self._connectButtonsVisualizzaVacanza()
		self.treewidgetAltriClienti.header().resizeSection(0, 50) # restringo la prima colonna che contiene l'id
		self.treewidgetAltriClienti.itemDoubleClicked.connect(lambda item: self._visualizzaCliente(item.connectedObject))
	
	
	def _setNumeroCartaHints(self, text : str):
		label = self.labelTipoCartaInserimentoPrenotazione
		if text.strip() == '':
			label.setText('')
		else:
			if text[0] == '3' and len(text) == 15:
				label.setText('(American Express)')
			elif text[0] == '3' and len(text) == 14:
				label.setText('(Diners)')
			elif text[0] == '4' and len(text) == 16:
				label.setText('(Visa)')
			elif text[0] == '5' and len(text) == 16:
				label.setText('(MasterCard)')
			else:
				label.setText('')
		
		lineEdit = self.lineeditNumeroCartaInserisciPrenotazione
		font = lineEdit.font() # salvo il file prima della modifica dello style sheet, poichè questa potrebbe azzerare il font della line edit
	
		if (text != '' and lineEdit.validator().validate(text, 0)[0] == QtGui.QValidator.State.Acceptable and # se il testo è accettato dal validator
			label.text() != ''): # e la carta è di un tipo noto
			if lineEdit.styleSheet() != "color: rgb(0, 170, 0);":
				lineEdit.setStyleSheet("color: rgb(0, 170, 0);") # il testo diventa verde
				lineEdit.setFont(font)
		
		elif lineEdit.styleSheet() != "color: rgb(255, 0, 0);":
			lineEdit.setStyleSheet("color: rgb(255, 0, 0);") # il testo diventa rosso
			lineEdit.setFont(font)


	def _hideElementsInserisciPrenotazione(self):
		self.widgetNumeroCameraInserimentoPrenotazione.hide();  self.widgetPeriodoInserimentoPrenotazione.hide()
		self.widgetTipoSoggiornoInserimentoPrenotazione.hide(); self.widgetClienteInserimentoPrenotazione.hide()
		self.labelClienteInserimentoPrenotazione.hide(); 		self.widgetNumeroCartaInserimentoPrenotazione.hide()
		self.widgetConfermaInserimentoPrenotazione.hide()

	def _hideElementsVisualizzaPrenotazione(self):
		self.groupboxPrenotazione.hide()
		self.widgetButtonsVisualizzaPrenotazione.hide()
		self.groupboxCheckIn.hide()

	def _hideElementsVisualizzaVacanza(self):
		self.groupboxVacanza.hide()
		self.widgetButtonsVisualizzaVacanza.hide()


	def _connectButtonsInserisciPrenotazione(self):
		self.btnSelezionaCamera.clicked.connect(self._btnSelezionaCameraClicked)
		self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
		self.btnRegistraCliente.clicked.connect(self._btnRegistraClienteClicked)
		self.btnConfermaPrenotazione.clicked.connect(self._btnConfermaPrenotazioneClicked)

	def _connectButtonsVisualizzaPrenotazione(self):
		self.btnRicercaPrenotazione.clicked.connect(self._btnRicercaPrenotazioneClicked)
		self.btnModificaPrenotazione.clicked.connect(self._btnModificaPrenotazioneClicked)
		self.btnEliminaPrenotazione.clicked.connect(self._btnEliminaPrenotazioneClicked)
		
		self.btnPiu.setIcon(QtGui.QIcon(GestoreFile.absolutePath('plus.png', Path.cwd())))
		self.btnMeno.setIcon(QtGui.QIcon(GestoreFile.absolutePath('minus.png', Path.cwd())))
		self.btnPiu.clicked.connect(self._btnPiuClicked)
		self.btnMeno.clicked.connect(self._btnMenoClicked)

		self.btnCheckIn.clicked.connect(self._btnCheckInClicked)

	
	def _connectButtonsVisualizzaVacanza(self):
		self.btnRicercaVacanza.clicked.connect(self._btnRicercaVacanzaClicked)
		self.btnModificaTermineVacanza.clicked.connect(self._btnModificaTermineVacanzaClicked)
		self.btnCheckOut.clicked.connect(self._btnCheckOutClicked)


	def _btnSelezionaCameraClicked(self):
		self.widgetSelezionaCamera = SelezionaCameraUI(self)
		self.widgetSelezionaCamera.show()

		def onCameraSelezionata(camera : Camera, periodo : PeriodoConData):
			if self.widgetNumeroCameraInserimentoPrenotazione.isHidden():
				self.widgetNumeroCameraInserimentoPrenotazione.show()
				self.widgetPeriodoInserimentoPrenotazione.show()
				self.widgetTipoSoggiornoInserimentoPrenotazione.show()
				self.widgetClienteInserimentoPrenotazione.show()
				
			self.lineeditNumeroCameraInserimentoPrenotazione.setText(str(camera.getNumero()))
			self.dateeditInizioPrenotazione.setDate(periodo.getInizio())
			self.dateeditFinePrenotazione.setDate(periodo.getFine())
		
		self.widgetSelezionaCamera.cameraSelezionata.connect(onCameraSelezionata)
		

	def _btnRicercaClienteClicked(self):
		self.widgetRicercaCliente = RicercaClienteUI(self)
		self.widgetRicercaCliente.clienteTrovato.connect(self._clienteSelezionato)
		self.widgetRicercaCliente.show()


	def _btnRegistraClienteClicked(self):
		self.widgetRegistraCliente = RegistraClienteUI(self)
		self.widgetRegistraCliente.btnRegistraCliente.clicked.connect(self._onRegistraClienteClicked)
		self.widgetRegistraCliente.clienteRegistrato.connect(self._clienteSelezionato)
		self.widgetRegistraCliente.show()
	

	def _onRegistraClienteClicked(self):
		if (self.widgetRegistraCliente.fieldsFilled(self.widgetRegistraCliente.lineeditLabelPairs) and 
		   not self.widgetRegistraCliente.isClienteInSystem() and self.widgetRegistraCliente.fieldsValid()):
			self.widgetRegistraCliente.salvaCliente()
			self._showMessage('Cliente registrato con successo!')
			self.widgetRegistraCliente.close()


	def _clienteSelezionato(self, cliente : Persona):
		self.nominativoInserimentoPrenotazione = cliente 
		self.labelClienteInserimentoPrenotazione.setText(
			f"Cliente:\n{cliente.getCognome()} {cliente.getNome()} (ID: {cliente.getId()})"
		)
		if self.labelClienteInserimentoPrenotazione.isHidden():
			self.labelClienteInserimentoPrenotazione.show()
			self.widgetNumeroCartaInserimentoPrenotazione.show()
			self.widgetConfermaInserimentoPrenotazione.show()
			self.labelTipoCartaInserimentoPrenotazione.setText('')


	def _btnConfermaPrenotazioneClicked(self):
		styleSheet = "color: rgb(0, 170, 0);"
		if self.lineeditNumeroCartaInserisciPrenotazione.styleSheet() != styleSheet:
			self._showMessage('Carta di credito non valida.', QMessageBox.Icon.Warning, 'Errore')
			return
		camere = self._readDict('camere')
		camera = camere[int(self.lineeditNumeroCameraInserimentoPrenotazione.text())]
		
		datiPrenotazione = {
			'periodo' : PeriodoConData(self.dateeditInizioPrenotazione.date().toPyDate(), self.dateeditFinePrenotazione.date().toPyDate()),
			'tipoSoggiorno' : Soggiorno.enumFromStr(self.comboboxTipoSoggiorno.currentText()),
			'nominativo' : self.nominativoInserimentoPrenotazione,
			'numeroCarta' : self.lineeditNumeroCartaInserisciPrenotazione.text()
		}
		camera.prenota(datiPrenotazione)
		
		self._showMessage('Caparra prelevata e prenotazione inserita correttamente.')
		self._hideElementsInserisciPrenotazione()
		self.lineeditNumeroCartaInserisciPrenotazione.clear()
		self.comboboxTipoSoggiorno.setCurrentIndex(0)
		

	def _btnRicercaPrenotazioneClicked(self):
		self.widgetRicercaPrenotazione = RicercaPrenotazioneVacanzaUI(self)
		self.widgetRicercaPrenotazione.prenotazioneSelezionata.connect(self._onPrenotazioneSelezionata)
		self.widgetRicercaPrenotazione.show()

	
	def _onPrenotazioneSelezionata(self, prenotazione : PrenotazioneVacanza):
		self.prenotazioneVisualizzata = prenotazione
		self.lineeditTipoSoggiornoPrenotazione.setText(str(prenotazione.getTipoSoggiorno()))
		self.lineeditNumeroCameraVisualizzaPrenotazione.setText(str(prenotazione.getCamera().getNumero()))
		self.lineEditNominativoVisualizzaPrenotazione.setText(
			f"{prenotazione.getNominativo().getCognome()} {prenotazione.getNominativo().getNome()} (ID: {prenotazione.getNominativo().getId()})"
		)
		self.dateeditPrenotazioneInizio.setDate(prenotazione.getPeriodo().getInizio())
		self.dateeditPrenotazioneFine.setDate(prenotazione.getPeriodo().getFine())
		self.labelContatoreClienti.setText(self.labelContatoreClienti.text()[:-1] + str(prenotazione.getCamera().getNumeroPersone()))
		
		self._addClienteCheckIn(prenotazione.getNominativo())
		self._fillListwidgetOmbrelloni()
		if self.groupboxPrenotazione.isHidden():
			self.groupboxPrenotazione.show()
			self.widgetButtonsVisualizzaPrenotazione.show()
			self.groupboxCheckIn.show()
			self.btnMeno.setEnabled(False)


	def _btnModificaPrenotazioneClicked(self):
		self.widgetModificaPrenotazione = ModificaPrenotazioneVacanzaUI(self, self.prenotazioneVisualizzata)
		self.widgetModificaPrenotazione.show()


	def _btnEliminaPrenotazioneClicked(self):
		richiestaConferma = QMessageBox()
		richiestaConferma.setIcon(QMessageBox.Icon.Warning)
		richiestaConferma.setWindowTitle('ConfermaEliminazione')
		richiestaConferma.setText("Confermi l'eliminazione di questa prenotazione?")
		richiestaConferma.addButton('Si', QMessageBox.ButtonRole.YesRole)
		noButton = richiestaConferma.addButton(QMessageBox.StandardButton.No)
		richiestaConferma.exec()

		if richiestaConferma.clickedButton() == noButton:
			pass # non accade nulla, eliminazione annullata
		else:
			camere : dict[int, Camera] = self._readDict('camere')
			camere[self.prenotazioneVisualizzata.getCamera().getNumero()].eliminaPrenotazione(self.prenotazioneVisualizzata)
			GestoreFile.salvaPickle(camere, Path(paths['camere']))
			self._showMessage('Prenotazione eliminata dal sistema.', QMessageBox.Icon.Information)
			self._hideElementsVisualizzaPrenotazione()
	

	def _btnPiuClicked(self):
		self.widgetScelta = QWidget(); self.widgetScelta.setWindowTitle('Struttura Alberghiera')
		self.widgetScelta.setMinimumSize(200, 150); self.widgetScelta.setGeometry(1500, 500, 200, 150)
		self.widgetScelta.setFont(QtGui.QFont('Arial', 10))
		
		btnRicerca = QPushButton('Ricerca cliente'); btnRegistra = QPushButton('Registra cliente')
		layout = QVBoxLayout(self.widgetScelta)
		layout.addWidget(btnRicerca)
		layout.addWidget(btnRegistra)

		def onRicercaClicked():
			self.widgetRicercaClienteCheckIn = RicercaClienteUI(self)
			self.widgetScelta.close()
			self.widgetRicercaClienteCheckIn.clienteTrovato.connect(self._addClienteCheckIn)
			self.widgetRicercaClienteCheckIn.show()
		
		def onRegistraClicked():
			self.widgetRegistraClienteCheckIn = RegistraClienteUI(self)
			def registraClienteClicked():
				if (self.widgetRegistraClienteCheckIn.fieldsFilled(self.widgetRegistraClienteCheckIn.lineeditLabelPairs) and 
				   not self.widgetRegistraClienteCheckIn.isClienteInSystem() and self.widgetRegistraClienteCheckIn.fieldsValid()):
					self.widgetRegistraClienteCheckIn.salvaCliente() # qui self.widgetRegistraClienteCheckIn lancia il segnale 'clienteRegistato'
					self._showMessage('Cliente registrato con successo!')
					self.widgetRegistraClienteCheckIn.close()
			
			self.widgetScelta.close()
			self.widgetRegistraClienteCheckIn.clienteRegistrato.connect(self._addClienteCheckIn)
			self.widgetRegistraClienteCheckIn.btnRegistraCliente.clicked.connect(registraClienteClicked)
			self.widgetRegistraClienteCheckIn.show()

		btnRicerca.clicked.connect(onRicercaClicked)
		btnRegistra.clicked.connect(onRegistraClicked)
		self.widgetScelta.show()
	

	def _addClienteCheckIn(self, cliente : Persona):
		i = 0
		while i < self.treewidgetClientiCheckIn.topLevelItemCount():
			item = self.treewidgetClientiCheckIn.topLevelItem(i)
			if item.connectedObject.getId() == cliente.getId():
				self._showMessage('Cliente già aggiunto alla lista.', QMessageBox.Icon.Warning, 'Errore')
				return
			i += 1
		self.treewidgetClientiCheckIn.addTopLevelItem(MyTreeWidgetItem(self.treewidgetClientiCheckIn,
													  [str(cliente.getId()), cliente.getCognome(), cliente.getNome()],
													  cliente))
		self.labelContatoreClienti.setText(str(int(self.labelContatoreClienti.text()[0]) + 1) + self.labelContatoreClienti.text()[1:])
		# controllo se riattivare il bottone meno o disattivare il bottone piu
		if not self.btnMeno.isEnabled():
			self.btnMeno.setEnabled(True)
		if self.treewidgetClientiCheckIn.topLevelItemCount() == self.prenotazioneVisualizzata.getCamera().getNumeroPersone():
			self.btnPiu.setEnabled(False)


	def _btnMenoClicked(self):
		if self.treewidgetClientiCheckIn.currentItem() == None:
			self._showMessage("Seleziona prima il cliente da rimuovere.", QMessageBox.Icon.Warning, 'Errore')
		else:
			self.treewidgetClientiCheckIn.takeTopLevelItem(self.treewidgetClientiCheckIn.indexOfTopLevelItem(
																						self.treewidgetClientiCheckIn.currentItem()))
			self.labelContatoreClienti.setText(str(int(self.labelContatoreClienti.text()[0]) - 1) + self.labelContatoreClienti.text()[1:])
			self.treewidgetClientiCheckIn.setCurrentItem(None)
			# controllo se riattivare il bottone piu o disattivare il bottone meno
			if self.treewidgetClientiCheckIn.topLevelItemCount() == 1:
				self.btnMeno.setEnabled(False)
			if not self.btnPiu.isEnabled():
				self.btnPiu.setEnabled(True)


	def _fillListwidgetOmbrelloni(self):
		ombrelloni : dict[int, Ombrellone] = self._readDict('ombrelloni')
		for ombrellone in ombrelloni.values():
			if not ombrellone.isAssegnato():
				self.listwidgetOmbrelloni.addItem(MyListWidgetItem(f'Ombrellone {ombrellone.getNumero()}', ombrellone))


	def _btnCheckInClicked(self):
		if self.listwidgetOmbrelloni.currentItem() == None:
			self._showMessage("Selezionare l'ombrellone da assegnare alla camera durante la vacanza.", QMessageBox.Icon.Warning, 'Errore')
			return
		# creazione della lista di clienti
		clienti = []
		i = 0
		while i < self.treewidgetClientiCheckIn.topLevelItemCount():
			clienti.append(self.treewidgetClientiCheckIn.topLevelItem(i).connectedObject)
			i += 1
		# assegnamento della camera
		datiAssegnamento = {
			'prenotazione' : self.prenotazioneVisualizzata,
			'clienti' : clienti,
			'ombrellone' : self.listwidgetOmbrelloni.currentItem().connectedObject
		}
		self.prenotazioneVisualizzata.getCamera().assegna(datiAssegnamento)

		self._showMessage('Check-in effettuato con successo!', QMessageBox.Icon.Information)
		self._hideElementsVisualizzaPrenotazione()



	def _btnRicercaVacanzaClicked(self):
		self.widgetRicercaVacanza = RicercaVacanzaUI(self)
		self.widgetRicercaVacanza.vacanzaTrovata.connect(self._onVacanzaTrovata)
		self.widgetRicercaVacanza.show()

	
	def _onVacanzaTrovata(self, vacanza : Vacanza):
		self.vacanzaVisualizzata = vacanza
		self.lineeditCameraVisualizzaVacanza.setText(str(vacanza.getCamera().getNumero()))
		self.lineeditNumeroOmbrelloneVisualizzaVacanza.setText(str(vacanza.getOmbrellone().getNumero()))
		self.lineeditTipoSoggiornoVisualizzaVacanza.setText(str(vacanza.getTipoSoggiorno()))
		self.lineeditNumeroCartaVacanza.setText(vacanza.getNumeroCarta())
		self.dateeditInizioVacanza.setDate(vacanza.getPeriodo().getInizio())
		self.dateeditFineVacanza.setDate(vacanza.getPeriodo().getFine())
		self.lineeditNominativoVisualizzaVacanza.setText(
			f'{vacanza.getNominativo().getCognome()} {vacanza.getNominativo().getNome()} (ID: {vacanza.getNominativo().getId()})'
		)
		for cliente in vacanza.getClienti():
			if cliente.getId() != vacanza.getNominativo().getId(): # se il cliente non è colui che ha fatto la prenotazione
				self.treewidgetAltriClienti.addTopLevelItem(MyTreeWidgetItem(self.treewidgetAltriClienti,
																	[str(cliente.getId()), cliente.getCognome(), cliente.getNome()],
																	cliente))
		if self.groupboxVacanza.isHidden():
			self.groupboxVacanza.show()
			self.widgetButtonsVisualizzaVacanza.show()
				


	def _btnModificaTermineVacanzaClicked(self):
		self.close()
		self.widgetModificaTermineVacanzaOmbrellone = ModificaTermineVacanzaOmbrelloneUI(self)
		self.widgetModificaTermineVacanzaOmbrellone.show()


	def _btnCheckOutClicked(self):
		pass


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()

	
	def _visualizzaCliente(self, cliente : Persona):
		self.widgetVisualizzaCliente = VisualizzaClienteUI(cliente)
		self.widgetVisualizzaCliente.show()
		self.treewidgetAltriClienti.setCurrentItem(None)


	def _readDict(self, pathsKey : str) -> dict:
		global paths
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dictionary = GestoreFile.leggiDictPickle(Path(paths[pathsKey]))
		except CorruptedFileError: # se camere non e' un dizionario
			self._showMessage(f"{Path(paths[pathsKey])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
			self.close()
			raise
		return dictionary


	def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = HomeGestioneVacanzeUI(QWidget())
	mainWidget.show()
	sys.exit(app.exec_())

