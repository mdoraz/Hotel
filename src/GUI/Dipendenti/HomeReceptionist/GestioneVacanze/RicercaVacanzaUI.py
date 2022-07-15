from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GestioneVacanza.Vacanza import Vacanza
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.exceptions import CorruptedFileError


class RicercaVacanzaUI(QTabWidget):
	
	vacanzaTrovata = QtCore.pyqtSignal(Vacanza)
	
	def __init__(self, previous: QWidget):
		super().__init__()
		
		loadUi(GestoreFile.absolutePath('RicercaVacanza.ui', Path.cwd()), self)
		
		self.previous = previous
		self._fillCombobox()
		self._connectButtons()


	def _fillCombobox(self):
		global camere
		camere = self._readCamere()
		for camera in camere.values():
			if camera.isAssegnato():
				self.combobox.addItem(str(camera.getNumero()))


	def _connectButtons(self):
		self.btnCerca.clicked.connect(self._btnCercaClicked)
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)


	def _btnCercaClicked(self):
		numeroCamera = int(self.combobox.currentText())
		self.vacanzaTrovata.emit(camere[numeroCamera].getVacanzaAttuale())
		self.close()
  

	def _readCamere(self) -> dict[int, Camera]:
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
		except CorruptedFileError: # se camere non e' un dizionario
			self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
			self.close()
			raise
		return camere


	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()
