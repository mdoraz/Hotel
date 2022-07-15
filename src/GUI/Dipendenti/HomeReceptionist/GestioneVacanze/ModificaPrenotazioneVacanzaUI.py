import sys
from pathlib import Path
import copy

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GUI.Dipendenti.HomeReceptionist.GestioneVacanze.SelezionaCameraUI import SelezionaCameraUI
from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import CorruptedFileError


class ModificaPrenotazioneVacanzaUI(QTabWidget):

	cameraPeriodoModificati = QtCore.pyqtSignal(PrenotazioneVacanza)
	tiposSoggiornoModificato = QtCore.pyqtSignal()

	def __init__(self, previous: QWidget, prenotazioneModificata : PrenotazioneVacanza):
		super().__init__()

		loadUi(GestoreFile.absolutePath('ModificaPrenotazioneVacanza.ui', Path.cwd()), self)

		self.previous = previous
		self.prenotazioneModificata = prenotazioneModificata

		self.comboboxTipoSoggiorno.setCurrentText(str(prenotazioneModificata.getTipoSoggiorno()))
		self._connectButtons()


	def _connectButtons(self):
		self.btnConferma.clicked.connect(self._btnConfermaClicked)
		self.btnCameraPeriodo.clicked.connect(self._btnCameraPeriodoClicked)
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)


	def _btnConfermaClicked(self):
		self.close()
		if Soggiorno.enumFromStr(self.comboboxTipoSoggiorno.currentText()) != self.prenotazioneModificata.getTipoSoggiorno(): # se il tipo di soggiorno è stato modificato
			# aggiorno la visualizzazione della prenotazione
			camere = self._readCamere()
			#self.previous.lineeditTipoSoggiornoPrenotazione.setText(self.comboboxTipoSoggiorno.currentText())
			camere[self.prenotazioneModificata.getCamera().getNumero()].eliminaPrenotazione(self.prenotazioneModificata) # elimino la prenotazione senza modifiche
			self.prenotazioneModificata.setTipoSoggiorno(Soggiorno.enumFromStr(self.comboboxTipoSoggiorno.currentText())) # modifico la prenotazione
			datiPrenotazione = {
				'prelevareCaparra' : False, # non bisogna prelevare di nuovo la caparra
				'nominativo' : self.prenotazioneModificata.getNominativo(),
				'tipoSoggiorno' : self.prenotazioneModificata.getTipoSoggiorno(),
				'numeroCarta' : self.prenotazioneModificata.getNumeroCarta(),
				'periodo' : self.prenotazioneModificata.getPeriodo()
			}
			camere[self.prenotazioneModificata.getCamera().getNumero()].prenota(datiPrenotazione) # riprenoto con i dati modificati
			GestoreFile.salvaPickle(camere, Path(paths['camere']))

			self.tiposSoggiornoModificato.emit()


	def _btnCameraPeriodoClicked(self):
		def onCameraSelezionata(camera : Camera, periodo : PeriodoConData):
			vecchiaPrenotazione = copy.deepcopy(self.prenotazioneModificata)
			
			# aggiorno la visualizzazione della prenotazione
			self.previous.lineeditNumeroCameraVisualizzaPrenotazione.setText(str(camera.getNumero()))
			self.previous.dateeditPrenotazioneInizio.setDate(periodo.getInizio())
			self.previous.dateeditPrenotazioneFine.setDate(periodo.getFine())
			self.previous.labelContatoreClienti.setText(self.previous.labelContatoreClienti.text()[:-1] + str(camera.getNumeroPersone()))
			self.close()
			
			# elimino la vecchia prenotazione dalla camera ad essa associata
			camere = self._readCamere()
			camere[self.prenotazioneModificata.getCamera().getNumero()].eliminaPrenotazione(self.prenotazioneModificata)
			GestoreFile.salvaPickle(camere, Path(paths['camere'])) # salvo l'eliminazione
			
			# modifico la prenotazione per aggiornare l'attributo prenotazioneVisualizzata della classe HomeGestioneVacanzeUI
			self.prenotazioneModificata.setPeriodo(periodo)
			self.prenotazioneModificata.setCamera(camera)
			if not self.previous.groupboxVacanza.isHidden(): # se nella HomeGestioneVacanzaUI c'è una vacanza visualizzata
				if self.previous.vacanzaVisualizzata.getCamera().getNumero() == camera.getNumero(): # se la vacanza è in corso nella camera la cui lista di prenotazioni è stata modificata
					self.previous.vacanzaVisualizzata.setCamera(camera) # per tenere sempre aggiornato la data massima in cui può terminare la vacanza

			# aggiungo la prenotazione modificata alla camera ad essa associata
			datiPrenotazione = {
				'prelevareCaparra' : False, # non bisogna prelevare di nuovo la caparra
				'nominativo' : self.prenotazioneModificata.getNominativo(),
				'tipoSoggiorno' : self.prenotazioneModificata.getTipoSoggiorno(),
				'numeroCarta' : self.prenotazioneModificata.getNumeroCarta(),
				'periodo' : periodo
			}
			camera.prenota(datiPrenotazione)

			self.cameraPeriodoModificati.emit(vecchiaPrenotazione) # quando lancio questo segnale, self.prenotazioneModificata (che è un riferimento della prenotazione passata al costruttore di questa classe)
																   # è stata modificata. Serve quindi passare la vecchia prenotazione per poterla eliminare ovunque serva sostituirla con quella nuova.


		self.close()
		self.widgetSelezionaCamera = SelezionaCameraUI(self, self.prenotazioneModificata)
		self.widgetSelezionaCamera.cameraSelezionata.connect(onCameraSelezionata)
		self.widgetSelezionaCamera.show()

	
	def _readCamere(self):
		global paths
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			camere : dict[int, Camera] = GestoreFile.leggiDictPickle(Path(paths['camere']))
		except CorruptedFileError:
			self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
			self.close()
			self.previous.close()
			raise
		return camere
	

	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = ModificaPrenotazioneVacanzaUI(QWidget(), None) # type: ignore
	mainWidget.show()
	sys.exit(app.exec_())