from copy import copy
from datetime import date
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GestioneVacanza.Vacanza import Vacanza
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Ombrellone import Ombrellone
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import CorruptedFileError

class ModificaTermineVacanzaOmbrelloneUI(QTabWidget):
	
	ombrelloneModificato = QtCore.pyqtSignal(Ombrellone)
	termineModificato = QtCore.pyqtSignal(Vacanza)

	def __init__(self, previous: QWidget, vacanza : Vacanza):
		super().__init__()

		loadUi(GestoreFile.absolutePath('ModificaTermineVacanzaOmbrellone.ui', Path.cwd()), self)

		self.previous = previous
		self.vacanza = vacanza

		self._fillComboboxOmbrelloniDisponibili()
		self.dateedit.setDate(self.vacanza.getPeriodo().getFine())
		self._setDateeditBoundaries()
		self._connectButtons()

	
	def _fillComboboxOmbrelloniDisponibili(self):
		thisOmbrelloneNotAdded = True
		global ombrelloni
		ombrelloni = self.previous._readDict('ombrelloni')
		for ombrellone in ombrelloni.values():
			if not ombrellone.isAssegnato():
				if thisOmbrelloneNotAdded and ombrellone.getNumero() > self.vacanza.getOmbrellone().getNumero():
					self.combobox.addItem(str(self.vacanza.getOmbrellone().getNumero()))
					thisOmbrelloneNotAdded = False
				self.combobox.addItem(str(ombrellone.getNumero()))
		self.combobox.setCurrentText(str(self.vacanza.getOmbrellone().getNumero()))


	def _setDateeditBoundaries(self):
		# la data di fine della vacanza attuale non può essere precedente alla data maggiore tra quella odierna e quella di inizio vacanza
		self.dateedit.setMinimumDate(date.today() if date.today() > self.vacanza.getPeriodo().getInizio() else self.vacanza.getPeriodo().getInizio())
		# la data di fine della vacanza attuale non può andare oltre la data di inizio della prossima prenotazione
		# che ha la camera associata a questa vacanza
		if len(self.vacanza.getCamera().getPrenotazioni()) > 0:
			self.dateedit.setMaximumDate(self.vacanza.getCamera().getPrenotazioni()[0].getPeriodo().getInizio())


	def _connectButtons(self):
		self.btnConferma.clicked.connect(self._btnConfermaClicked)
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)


	def _btnConfermaClicked(self):
		if self.dateedit.date().toPyDate() != self.vacanza.getPeriodo().getFine() or self.combobox.currentText() != str(self.vacanza.getOmbrellone().getNumero()):
			
			if self.dateedit.date().toPyDate() != self.vacanza.getPeriodo().getFine(): # se è stata modificata il termina della vacanza
				vecchiaVacanza = copy(self.vacanza)
				nuovoPeriodo = PeriodoConData(self.vacanza.getPeriodo().getInizio(), self.dateedit.date().toPyDate())
				self.vacanza.setPeriodo(nuovoPeriodo)
				self._salvaModifiche()
				self.termineModificato.emit(vecchiaVacanza)
			
			if self.combobox.currentText() != str(self.vacanza.getOmbrellone().getNumero()): # se è stato modificato il numero di ombrellone
				vecchioOmbrellone = self.vacanza.getOmbrellone()
				vecchioOmbrellone.terminaAssegnamento() # vecchio ombrellone non piu assegnato
				self.vacanza.setOmbrellone(ombrelloni[int(self.combobox.currentText())])
				self.vacanza.getOmbrellone().assegna({}) # assegno il nuovo ombrellone
				self._salvaModifiche()
				self.ombrelloneModificato.emit(vecchioOmbrellone)
		
			self.previous._showMessage('Vacanza modificata con successo!', QMessageBox.Icon.Information)
		
		self.close()


	def _salvaModifiche(self):
		camera = self.vacanza.getCamera()
		camera.setVacanzaAttuale(self.vacanza)
		camere = self._readCamere()
		camere[camera.getNumero()] = camera
		GestoreFile.salvaPickle(camere, Path(paths['camere']))


	def _readCamere(self) -> dict:
		global paths
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
		except CorruptedFileError: # se camere non e' un dizionario
			self._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
			self.close()
			raise
		return camere


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()
