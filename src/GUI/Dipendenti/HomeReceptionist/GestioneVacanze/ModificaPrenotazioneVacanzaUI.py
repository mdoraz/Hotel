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
			self.previous.lineeditTipoSoggiornoPrenotazione.setText(self.comboboxTipoSoggiorno.currentText())
			# modifico la prenotazione
			prenotazioneDaModificare = copy.deepcopy(self.prenotazioneModificata)
			self.prenotazioneModificata.setTipoSoggiorno(Soggiorno.enumFromStr(self.comboboxTipoSoggiorno.currentText()))
			self._modificaESalvaCamera(prenotazioneDaModificare) # salvo la mosifica su file


	def _btnCameraPeriodoClicked(self):
		def onCameraSelezionata(camera : Camera, periodo : PeriodoConData):
			# aggiorno la visualizzazione della prenotazione
			self.previous.lineeditNumeroCameraVisualizzaPrenotazione.setText(str(camera.getNumero()))
			self.previous.dateeditPrenotazioneInizio.setDate(periodo.getInizio())
			self.previous.dateeditPrenotazioneFine.setDate(periodo.getFine())
			self.close()
			# modifico la prenotazione
			prenotazioneDaModificare = copy.deepcopy(self.prenotazioneModificata)
			self.prenotazioneModificata.setCamera(camera)
			self.prenotazioneModificata.setPeriodo(periodo)
			self._modificaESalvaCamera(prenotazioneDaModificare) # salvo la modifica su file

		self.close()
		self.widgetSelezionaCamera = SelezionaCameraUI(self, self.prenotazioneModificata)
		self.widgetSelezionaCamera.cameraSelezionata.connect(onCameraSelezionata)
		self.widgetSelezionaCamera.show()


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()


	def _modificaESalvaCamera(self, prenotazioneDaModificare):
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			camere : dict[int, Camera] = GestoreFile.leggiDictPickle(Path(paths['camere']))
		except CorruptedFileError:
			self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
			self.close()
			self.previous.close()
			raise
		camere[self.prenotazioneModificata.getCamera().getNumero()].modificaPrenotazione(prenotazioneDaModificare, self.prenotazioneModificata)
		GestoreFile.salvaPickle(camere, Path(paths['camere']))



if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = ModificaPrenotazioneVacanzaUI(QWidget(), None) # type: ignore
	mainWidget.show()
	sys.exit(app.exec_())