import sys
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.AggiungereClientiCheckInUI import AggiungereClientiCheckInUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.EliminaPrenotazioneVacanzaUI import EliminaPrenotazioneVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.ModificaPrenotazioneVacanzaUI import ModificaPrenotazioneVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.ModificaTermineVacanzaOmbrelloneUI import ModificaTermineVacanzaOmbrelloneUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.RicercaPrenotazioneVacanzaUI import RicercaPrenotazioneVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.RicercaVacanzaUI import RicercaVacanzaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.SelezionaCameraUI import SelezionaCameraUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaClienteUI import RicercaClienteUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RegistraClienteUI import RegistraClienteUI
from src.Servizi.Camera import Camera
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import CorruptedFileError


class HomeGestioneVacanzeUI(QTabWidget):
	
	def __init__(self, previous: QWidget):
		super().__init__()
		
		loadUi(GestoreFile.absolutePath('HomeGestioneVacanze.ui', Path.cwd()), self)

		self.previous = previous

		self._hideElements()
		self._setValidators()
		self.lineeditNumeroCartaInserisciPrenotazione.textChanged.connect(self._setNumeroCartaHints)
		self._connectButtons()

		self.msg = QMessageBox()

	
	def _hideElements(self):
		# tab inserisci prenotazione
		self.widgetNumeroCameraInserimentoPrenotazione.hide();  self.widgetPeriodoInserimentoPrenotazione.hide()
		self.widgetTipoSoggiornoInserimentoPrenotazione.hide(); self.widgetClienteInserimentoPrenotazione.hide()
		self.labelClienteInserimentoPrenotazione.hide(); 		self.widgetNumeroCartaInserimentoPrenotazione.hide()
		self.widgetConfermaInserimentoPrenotazione.hide()
		# tab visualizza prenotazione
		self.groupboxPrenotazione.hide()
		self.widgetButtonsVisualizzaPrenotazione.hide()
		self.groupboxCheckIn.hide()
		

	def _setValidators(self):
		self.lineeditNumeroCartaInserisciPrenotazione.setValidator(GUIUtils.validators['numeroCarta'])
	
		
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


	def _connectButtons(self):
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)
		# tab inserisci prenotazione
		self.btnSelezionaCamera.clicked.connect(self._btnSelezionaCameraClicked)
		self.btnRicercaCliente.clicked.connect(self._btnRicercaClienteClicked)
		self.btnRegistraCliente.clicked.connect(self._btnRegistraClienteClicked)
		self.btnConfermaPrenotazione.clicked.connect(self._btnConfermaPrenotazioneClicked)
		# tab visualizza prenotazione
		self.btnRicercaPrenotazione.clicked.connect(self._btnRicercaPrenotazioneClicked)
		self.btnModificaPrenotazione.clicked.connect(self._btnModificaPrenotazioneClicked)
		self.btnEliminaPrenotazione.clicked.connect(self._btnEliminaPrenotazioneClicked)
		self.btnAggiungiClienti.clicked.connect(self._btnAggiungiClientiClicked)
		self.btnCheckIn.clicked.connect(self._btnCheckInClicked)
		# tab visualizza vacanza
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
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
		except CorruptedFileError: # se camere non e' un dizionario
			self._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
			self.close()
			raise
		camera = camere[int(self.lineeditNumeroCameraInserimentoPrenotazione.text())]
		
		datiPrenotazione = {
			'periodo' : PeriodoConData(self.dateeditInizioPrenotazione.date().toPyDate(), self.dateeditFinePrenotazione.date().toPyDate()),
			'tipoSoggiorno' : Soggiorno.enumFromStr(self.comboboxTipoSoggiorno.currentText()),
			'nominativo' : self.nominativoInserimentoPrenotazione,
			'numeroCarta' : self.lineeditNumeroCartaInserisciPrenotazione.text()
		}
		camera.prenota(datiPrenotazione)
		
		self._showMessage('Caparra prelevata e prenotazione inserita correttamente.')
		self._hideElements()
		

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
		if self.groupboxPrenotazione.isHidden():
			self.groupboxPrenotazione.show()
			self.widgetButtonsVisualizzaPrenotazione.show()
			self.groupboxCheckIn.show()


	def _btnModificaPrenotazioneClicked(self):
		self.widgetModificaPrenotazione = ModificaPrenotazioneVacanzaUI(self, self.prenotazioneVisualizzata)
		self.widgetModificaPrenotazione.show()


	def _btnEliminaPrenotazioneClicked(self):
		self.close()
		self.widgetEliminaPrenotazione = EliminaPrenotazioneVacanzaUI(self)
		self.widgetEliminaPrenotazione.show()


	def _btnAggiungiClientiClicked(self):
		self.close()
		self.widgetAggiungereClientiCheckIn = AggiungereClientiCheckInUI(self)
		self.widgetAggiungereClientiCheckIn.show()


	def _btnCheckInClicked(self):
		pass


	def _btnRicercaVacanzaClicked(self):
		self.close()
		self.widgetRicercaVacanza = RicercaVacanzaUI(self)
		self.widgetRicercaVacanza.show()


	def _btnModificaTermineVacanzaClicked(self):
		self.close()
		self.widgetModificaTermineVacanzaOmbrellone = ModificaTermineVacanzaOmbrelloneUI(self)
		self.widgetModificaTermineVacanzaOmbrellone.show()


	def _btnCheckOutClicked(self):
		pass


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()


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

