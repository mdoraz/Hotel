import sys
from datetime import date, timedelta
from pathlib import Path
from copy import copy

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.VisualizzaClienteUI import VisualizzaClienteUI
from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.GestioneVacanza.Vacanza import Vacanza
from src.Gestori.GestoreFile import GestoreFile
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
		self._setupVisualizzaArriviPartenze()
		
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

	
	def _setupVisualizzaArriviPartenze(self):
		dataDomani = date.today() + timedelta(days = 1)
		camere : dict[int, Camera] = self._readDict('camere')
		
		# riempimento dei due tree widget
		for camera in camere.values():
			if camera.isAssegnato() and camera.getVacanzaAttuale().getPeriodo().getFine() == dataDomani:	# type: ignore
					self._aggiungiPartenza(camera.getVacanzaAttuale())										# type: ignore
		
		for camera in camere.values():
			for prenotazione in camera.getPrenotazioni():
				if prenotazione.getPeriodo().getInizio() == dataDomani:
					self._aggiungiArrivo(prenotazione)
					break
		
		# ridimensionameno delle colonne dei due tree widget
		self.treewidgetArrivi.header().resizeSection(0, 90)
		self.treewidgetArrivi.header().resizeSection(1, 170)
		self.treewidgetArrivi.header().resizeSection(2, 110)
		self.treewidgetArrivi.header().resizeSection(3, 110)
		self.treewidgetArrivi.header().resizeSection(4, 170)
		
		self.treewidgetPartenze.header().resizeSection(0, 80)
		self.treewidgetPartenze.header().resizeSection(1, 100)
		self.treewidgetPartenze.header().resizeSection(2, 160)
		self.treewidgetPartenze.header().resizeSection(3, 100)
		self.treewidgetPartenze.header().resizeSection(4, 100)
		self.treewidgetPartenze.header().resizeSection(5, 160)

		def showPrenotazione(item : MyTreeWidgetItem):
			self._onPrenotazioneSelezionata(item.connectedObject) # type: ignore
			self.innerTabWidget.setCurrentIndex(1)

		def showVacanza(item : MyTreeWidgetItem):
			self._onVacanzaTrovata(item.connectedObject) # type: ignore
			self.innerTabWidget.setCurrentIndex(2)

		# collegamenro del doppio click con la visualizzazione dell'elemento clickato
		self.treewidgetArrivi.itemDoubleClicked.connect(showPrenotazione)
		self.treewidgetPartenze.itemDoubleClicked.connect(showVacanza)


	def _aggiungiArrivo(self, prenotazione : PrenotazioneVacanza):
		self.treewidgetArrivi.addTopLevelItem(
			MyTreeWidgetItem(self.treewidgetArrivi,
							 [str(prenotazione.getCamera().getNumero()), 
							 str(prenotazione.getTipoSoggiorno()), prenotazione.getPeriodo().getInizio().strftime('%d/%m/%Y'),
							 prenotazione.getPeriodo().getFine().strftime('%d/%m/%Y'), prenotazione.getNumeroCarta(), 
							 f"{prenotazione.getNominativo().getCognome()} {prenotazione.getNominativo().getNome()} - ID: {prenotazione.getNominativo().getId()}"], 
							 prenotazione)
		)
	

	def _aggiungiPartenza(self, vacanza : Vacanza):
		self.treewidgetPartenze.addTopLevelItem(
			MyTreeWidgetItem(self.treewidgetPartenze, 
							 [str(vacanza.getCamera().getNumero()), str(vacanza.getOmbrellone().getNumero()),															# type: ignore
							 str(vacanza.getTipoSoggiorno()), vacanza.getPeriodo().getInizio().strftime('%d/%m/%Y'),										# type: ignore
							 vacanza.getPeriodo().getFine().strftime('%d/%m/%Y'), vacanza.getNumeroCarta(), 												# type:ignore
							 f"{vacanza.getNominativo().getCognome()} {vacanza.getNominativo().getNome()} - ID: {vacanza.getNominativo().getId()}"], 	# type: ignore
							 vacanza)
		)

	
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
		
		self._showMessage('Caparra prelevata e prenotazione inserita correttamente.', QMessageBox.Icon.Information)
		self._hideElementsInserisciPrenotazione()
		self.lineeditNumeroCartaInserisciPrenotazione.clear()
		self.comboboxTipoSoggiorno.setCurrentIndex(0)

		if self.dateeditInizioPrenotazione.date().toPyDate() == date.today() + timedelta(days = 1): # se la prenotazione inizia domani
			prenotazione = PrenotazioneVacanza(datiPrenotazione['periodo'], camera, datiPrenotazione['tipoSoggiorno'],
                                           	   datiPrenotazione['nominativo'], datiPrenotazione['numeroCarta'])
			self._aggiungiArrivo(prenotazione)
		

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
		self.labelContatoreClienti.setText('0/' + str(prenotazione.getCamera().getNumeroPersone()))

		self.treewidgetClientiCheckIn.clear() # svuoto il tree widget con la lista di clienti del check in
		self._addClienteCheckIn(prenotazione.getNominativo())
		self.btnPiu.setEnabled(True)
		self.btnMeno.setEnabled(False)
		self._fillListwidgetOmbrelloni()
		if self.groupboxPrenotazione.isHidden():
			self.groupboxPrenotazione.show()
			self.widgetButtonsVisualizzaPrenotazione.show()
			self.groupboxCheckIn.show()
			self.btnMeno.setEnabled(False)


	def _btnModificaPrenotazioneClicked(self):
		def onTipoSoggiornoModificato():
			self.lineeditTipoSoggiornoPrenotazione.setText(self.comboboxTipoSoggiorno.currentText())
			if self.prenotazioneVisualizzata.getPeriodo().getInizio() == date.today() + timedelta(days = 1): # se la prenotazione è visualizzata nella lista di arrivi
				i = 0
				while i < self.treewidgetArrivi.topLevelItemCount():
					if self.treewidgetArrivi.topLevelItem(i).connectedObject == self.prenotazioneVisualizzata:
						self.treewidgetArrivi.topLevelItem(i).connectedObject = self.prenotazioneVisualizzata # il confronto non coinvolge il tipo di soggiorno, che è diverso
						self.treewidgetArrivi.topLevelItem(i).setText(1, str(self.prenotazioneVisualizzata.getTipoSoggiorno())) # aggiornato il tipo di soggiorno mostrato
					i += 1
		
		def onCameraPeriodoModificati(vecchiaPrenotazione : PrenotazioneVacanza):
			nuovaCamera  = self.prenotazioneVisualizzata.getCamera()
			nuovoPeriodo = self.prenotazioneVisualizzata.getPeriodo()
			dataDomani = date.today() + timedelta(days = 1)
			
			# aggiornamento tab visualizza prenotazione
			self.lineeditNumeroCameraVisualizzaPrenotazione.setText(str(nuovaCamera.getNumero()))
			self.dateeditPrenotazioneInizio.setDate(nuovoPeriodo.getInizio())
			self.dateeditPrenotazioneFine.setDate(nuovoPeriodo.getFine())
			self.labelContatoreClienti.setText(self.labelContatoreClienti.text()[:-1] + str(nuovaCamera.getNumeroPersone()))
			if nuovaCamera.getNumeroPersone() <= self.treewidgetClientiCheckIn.topLevelItemCount() and self.btnPiu.isEnabled():
				self.btnPiu.setEnabled(False)
			if nuovaCamera.getNumeroPersone() > self.treewidgetClientiCheckIn.topLevelItemCount() and not self.btnPiu.isEnabled():
				self.btnPiu.setEnabled(True)
			
			# aggiornamento tab visualizza arrivi e partenze
			if vecchiaPrenotazione.getPeriodo().getInizio() == dataDomani: # se la vecchia prenotazione era tra gli arrivi
				# trovo la riga in cui si trova la vecchia prenotazione nel tree widget
				indiceRiga = 0
				while indiceRiga < self.treewidgetArrivi.topLevelItemCount():
					if self.treewidgetArrivi.topLevelItem(indiceRiga).connectedObject == vecchiaPrenotazione:
						break
					indiceRiga += 1
				
				if nuovoPeriodo.getInizio() != dataDomani: # se la prenotazione non inizia più domani
					self.treewidgetArrivi.takeTopLevelItem(indiceRiga) # prenotazione rimossa
				else: # se la data di inizio non è cambiata
					self.treewidgetArrivi.topLevelItem(indiceRiga).connectedObject = copy(self.prenotazioneVisualizzata)
					self.treewidgetArrivi.topLevelItem(indiceRiga).setText(0, str(nuovaCamera.getNumero())) # aggiorno il numero di camera mostrato
					self.treewidgetArrivi.topLevelItem(indiceRiga).setText(3, nuovoPeriodo.getFine().strftime('%d/%m/%Y')) # aggiorno la data di fine mostrata
			
			elif nuovoPeriodo.getInizio() == dataDomani:
				self._aggiungiArrivo(copy(self.prenotazioneVisualizzata))


		self.widgetModificaPrenotazione = ModificaPrenotazioneVacanzaUI(self, self.prenotazioneVisualizzata)
		self.widgetModificaPrenotazione.tiposSoggiornoModificato.connect(onTipoSoggiornoModificato)
		self.widgetModificaPrenotazione.cameraPeriodoModificati.connect(onCameraPeriodoModificati)
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
			# elimino la prenotazione dalla camera e salvo su file
			camere : dict[int, Camera] = self._readDict('camere')
			camere[self.prenotazioneVisualizzata.getCamera().getNumero()].eliminaPrenotazione(self.prenotazioneVisualizzata)
			GestoreFile.salvaPickle(camere, Path(paths['camere']))
			# se sto visualizzando una vacanza associata alla camera modificata, gli aggiorno l'attributo camera
			if not self.groupboxVacanza.isHidden() and self.vacanzaVisualizzata.getCamera().getNumero() == self.prenotazioneVisualizzata.getCamera().getNumero():
				self.vacanzaVisualizzata.setCamera(camere[self.prenotazioneVisualizzata.getCamera().getNumero()])
			
			self._showMessage('Prenotazione eliminata dal sistema.', QMessageBox.Icon.Information)
			self._hideElementsVisualizzaPrenotazione()

			if self.prenotazioneVisualizzata.getPeriodo().getInizio() == date.today() + timedelta(days = 1): # se la prenotazione iniziava domani
				i = 0
				while i < self.treewidgetArrivi.topLevelItemCount():
					if self.treewidgetArrivi.topLevelItem(i).connectedObject == self.prenotazioneVisualizzata:
						self.treewidgetArrivi.takeTopLevelItem(i)
						break
					i += 1


	def _btnPiuClicked(self):
		self.widgetScelta = QWidget(); self.widgetScelta.setWindowTitle('Struttura Alberghiera')
		self.widgetScelta.setMinimumSize(200, 150); self.widgetScelta.setGeometry(1500, 500, 200, 150)
		self.widgetScelta.setFont(QtGui.QFont('Arial', 10))
		
		btnRicerca = QPushButton('Ricerca cliente'); btnRegistra = QPushButton('Registra cliente')
		layout = QVBoxLayout(self.widgetScelta)
		layout.addWidget(btnRicerca)
		layout.addWidget(btnRegistra)

		def onRicercaClicked():
			self.widgetCercaClienteCheckIn = RicercaClienteUI(self)
			self.widgetScelta.close()
			self.widgetCercaClienteCheckIn.clienteTrovato.connect(self._addClienteCheckIn)
			self.widgetCercaClienteCheckIn.show()
		
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
		if self.treewidgetClientiCheckIn.topLevelItemCount() > 1:
			self.btnMeno.setEnabled(True)
		if self.treewidgetClientiCheckIn.topLevelItemCount() >= self.prenotazioneVisualizzata.getCamera().getNumeroPersone():
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
			if self.treewidgetClientiCheckIn.topLevelItemCount() < self.prenotazioneVisualizzata.getCamera().getNumeroPersone():
				self.btnPiu.setEnabled(True)


	def _fillListwidgetOmbrelloni(self):
		self.listwidgetOmbrelloni.clear()
		ombrelloni : dict[int, Ombrellone] = self._readDict('ombrelloni')
		for ombrellone in ombrelloni.values():
			if not ombrellone.isAssegnato():
				self.listwidgetOmbrelloni.addItem(MyListWidgetItem(f'Ombrellone {ombrellone.getNumero()}', ombrellone))


	def _btnCheckInClicked(self):
		if self.prenotazioneVisualizzata.getPeriodo().getInizio() > date.today(): # se la prenotazione inizia nei giorni a venire
			self._showMessage(f"Impossibile effettuare il check-in: la prenotazione inizia il {self.prenotazioneVisualizzata.getPeriodo().getInizio().strftime('%d/%m/%Y')}.",
							  QMessageBox.Icon.Warning, 'Errore')
			return
		if self.prenotazioneVisualizzata.getCamera().isAssegnato():
			self._showMessage(f"La camera {self.prenotazioneVisualizzata.getCamera().getNumero()} è al momento occupata, impossibile effettuare il check-in.",
							  QMessageBox.Icon.Warning, 'Errore')
			return
		if self.treewidgetClientiCheckIn.topLevelItemCount() > self.prenotazioneVisualizzata.getCamera().getNumeroPersone():
			self._showMessage(f"Inseriti troppi clienti per la camera {self.prenotazioneVisualizzata.getCamera().getNumero()}.",
							  QMessageBox.Icon.Warning, 'Errore')
			return
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

		if self.prenotazioneVisualizzata.getPeriodo().getFine() == date.today() + timedelta(days = 1): # se la vacanza appena creata col check-in termina domani
			vacanza = Vacanza(datiAssegnamento['prenotazione'], datiAssegnamento['clienti'], datiAssegnamento['ombrellone'])
			self._aggiungiPartenza(vacanza)
	

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
		if not vacanza.getNominativo() in vacanza.getClienti():
			self.lineeditNominativoVisualizzaVacanza.setText(self.lineeditNominativoVisualizzaVacanza.text() + ' - NON PRESENTE')

		self.treewidgetAltriClienti.clear() # svuoto il tree widget contenente gli altri clienti della vacanza
		# riempio il tree widget appena svuotato
		for cliente in vacanza.getClienti():
			if cliente.getId() != vacanza.getNominativo().getId(): # se il cliente non è colui che ha fatto la prenotazione
				self.treewidgetAltriClienti.addTopLevelItem(MyTreeWidgetItem(self.treewidgetAltriClienti,
																	[str(cliente.getId()), cliente.getCognome(), cliente.getNome()],
																	cliente))
		if self.groupboxVacanza.isHidden():
			self.groupboxVacanza.show()
			self.widgetButtonsVisualizzaVacanza.show()


	def _btnModificaTermineVacanzaClicked(self):
		def onOmbrelloneModificato(vecchioOmbrellone : Ombrellone):
			self.lineeditNumeroOmbrelloneVisualizzaVacanza.setText(str(self.vacanzaVisualizzata.getOmbrellone().getNumero()))
			self._insertOmbrelloneDisponibile(vecchioOmbrellone) # l'ombrellone associato precedentemente alla vacanza compare nella lista di ombrelloni diaponibili nel check-in
			self._removeOmbrelloneNonDisponibile(self.vacanzaVisualizzata.getOmbrellone()) # l'ombrellone ora associato alla vacanza scompare dalla quella lista


		def onTermineModificato(vecchiaVacanza : Vacanza):
			# aggiornamento tab visualizza vacanza
			self.dateeditFineVacanza.setDate(self.vacanzaVisualizzata.getPeriodo().getFine())
			
			# aggiornamento tree widget partenze
			dataDomani = date.today() + timedelta(days = 1)
			if vecchiaVacanza.getPeriodo().getFine() == dataDomani: # se la vacanza era tra le partenze, ora non lo è più quindi la elimino dal tree widget
				indiceRiga = 0
				while indiceRiga < self.treewidgetPartenze.topLevelItemCount():
					if self.treewidgetPartenze.topLevelItem(indiceRiga).connectedObject == vecchiaVacanza:
						break
					indiceRiga += 1
				self.treewidgetPartenze.takeTopLevelItem(indiceRiga)
			
			elif self.vacanzaVisualizzata.getPeriodo().getFine() == dataDomani: # se il nuovo termine è domani
				self._aggiungiPartenza(copy(self.vacanzaVisualizzata))
		
		
		self.widgetModificaTermineVacanzaOmbrellone = ModificaTermineVacanzaOmbrelloneUI(self, self.vacanzaVisualizzata)
		self.widgetModificaTermineVacanzaOmbrellone.ombrelloneModificato.connect(onOmbrelloneModificato)
		self.widgetModificaTermineVacanzaOmbrellone.termineModificato.connect(onTermineModificato)
		self.widgetModificaTermineVacanzaOmbrellone.show()


	def _btnCheckOutClicked(self):
		self.vacanzaVisualizzata.getCamera().terminaAssegnamento()
		self._showMessage('Costo della vacanza rimanente dal pagamento della caparra prelevato.\nCheck-out effettuato con successo!',
						  QMessageBox.Icon.Information)
		self._hideElementsVisualizzaVacanza()

		if not self.groupboxPrenotazione.isHidden(): # se si sta visualizzando una prenotazione
			# l'ombrellone associato alla vacanza da concludere torna nella lista degli ombrelloni selezionabili al check-in
			self._insertOmbrelloneDisponibile(self.vacanzaVisualizzata.getOmbrellone())
		
		if self.vacanzaVisualizzata.getPeriodo().getFine() == date.today() + timedelta(days = 1): # se doveva terminare domani ma è terminata in anticipo di 1 giorno
			i = 0
			while i < self.treewidgetPartenze.topLevelItemCount():
				if self.vacanzaVisualizzata == self.treewidgetPartenze.topLevelItem(i).connectedObject:
					self.treewidgetPartenze.takeTopLevelItem(i) # vacanza rimossa dalle partenze
					break
				i += 1 

	
	def _insertOmbrelloneDisponibile(self, ombrellone : Ombrellone):
		i = 0
		while (i < self.listwidgetOmbrelloni.count() and 
			   self.listwidgetOmbrelloni.item(i).connectedObject.getNumero() < ombrellone.getNumero()):
			i += 1
		self.listwidgetOmbrelloni.insertItem(i, MyListWidgetItem(f'Ombrellone {ombrellone.getNumero()}', ombrellone))
	

	def _removeOmbrelloneNonDisponibile(self, ombrellone : Ombrellone):
		i = 0
		while i < self.listwidgetOmbrelloni.count():
			item = self.listwidgetOmbrelloni.item(i)
			if item.connectedObject.getNumero() == ombrellone.getNumero():
				self.listwidgetOmbrelloni.takeItem(i)
				return
			i +=1


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()

	
	def _visualizzaCliente(self, cliente : Persona):
		def onClienteEliminato():
			# imposto a 0 l'id dell'istanza del cliente eliminato presente nella lista di clienti della vacanza visualizzata:
			# in questo modo, eliminare di nuovo questo cliente non comporterebbe l'eliminazione nel file clienti.pickle di un eventuale
			# altro cliente registrato successivamente all'eliminazione di questo e con lo stesso id.
			i = 0
			while i < self.treewidgetAltriClienti.topLevelItemCount():
				if self.treewidgetAltriClienti.topLevelItem(i).connectedObject == cliente:
					break
				i += 1
			self.treewidgetAltriClienti.topLevelItem(i).setText(0, '0') # aggiorno l'id viualizzato
			clienti = self.vacanzaVisualizzata.getClienti()
			for _cliente in clienti:
				if _cliente.getId() == self.treewidgetAltriClienti.topLevelItem(i).connectedObject.getId():
					_cliente.setId(0)
					self.treewidgetAltriClienti.topLevelItem(i).connectedObject = _cliente
					break
			self.vacanzaVisualizzata.setClienti(clienti)
			# salvo su file
			camere = self._readDict('camere')
			camere[self.vacanzaVisualizzata.getCamera().getNumero()].setVacanzaAttuale(self.vacanzaVisualizzata)
			GestoreFile.salvaPickle(camere, Path(paths['camere']))
			self.widgetVisualizzaCliente.close()
		
		self.widgetVisualizzaCliente = VisualizzaClienteUI(cliente)
		self.widgetVisualizzaCliente.clienteEliminato.connect(onClienteEliminato)
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

