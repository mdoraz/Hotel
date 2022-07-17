from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.GestioneVacanza.Stato import Stato
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Bici import Bici
from src.Servizi.Camera import Camera
from src.Utilities.customQtClasses import MyTreeWidgetItem
from src.Utilities.exceptions import CorruptedFileError


class RiconsegnaBiciUI(QWidget):

	btnIndietroClicked = QtCore.pyqtSignal()
	biciRiconsegnate = QtCore.pyqtSignal(list)

	def __init__(self, previous : QWidget):
		super().__init__()

		loadUi(GestoreFile.absolutePath('RiconsegnaBici.ui', Path.cwd()), self)

		self.previous = previous

		self.groupbox.hide()
		self._fillComboboxCamere()
		self._connectButtons()

		self.msg = QMessageBox()


	def _fillComboboxCamere(self):
		camere = self._readDict('camere')

		for camera in camere.values():
			if camera.isAssegnato(): # aggiungo alla combo box solo i numeri delle camere assegnate
				self.combobox.addItem(str(camera.getNumero()))
	

	def _connectButtons(self):
		self.btnRicercaNoleggi.clicked.connect(self._btnRicercaNoleggiClicked)
		self.btnTerminaNoleggi.clicked.connect(self._btnTerminaNoleggiClicked)
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)
	
	
	def _btnRicercaNoleggiClicked(self):
		numeroCamera = int(self.combobox.currentText())
		camere = self._readDict('camere')
		camera : Camera = camere[numeroCamera]

		self.treewidget.clear()
		for noleggio in camera.getVacanzaAttuale().getNoleggiBici(): # type: ignore
			if noleggio.isInCorso():
				bici = noleggio.getBici()
				self.treewidget.addTopLevelItem(MyTreeWidgetItem(self.treewidget,
																 [str(bici.getNumero()), 'Donna' if bici.getTipo() == True else 'Uomo'],
																 bici))
		
		if self.treewidget.topLevelItemCount() == 0: # se non ci sono noleggi in corso per la camera inserita
			self._showMessage(f'Non ci sono noleggi in corso per la camera {camera.getNumero()}.', QMessageBox.Icon.Warning, 'Errore')
			return
		
		if self.groupbox.isHidden():
			self.groupbox.show()

	
	def _btnTerminaNoleggiClicked(self):
		if len(self.treewidget.selectedItems()) == 0:
			self._showMessage('Selezionare almeno una bici da riconsegnare', QMessageBox.Icon.Warning, 'Errore')
			return

		biciRiconsegnate = []
		for item in self.treewidget.selectedItems():
			bici : Bici = item.connectedObject
			try:
				bici.terminaAssegnamento()
			except CorruptedFileError:
				self._showMessage(f"{Path(paths['camere']).name} è stato corrotto irreversibilmente. Per risolvere il problema, eliminalo.", QMessageBox.Icon.Critical, 'Errore')
				return
			self._rimuoviBici(bici) # rimuovo la bici dal tree widget poichè è stata riconsegnata
			biciRiconsegnate.append(bici)

		self._showMessage('Biciclette riconsegnate nuovamente disponibili!', QMessageBox.Icon.Information)
		self.groupbox.hide()
		self.biciRiconsegnate.emit(biciRiconsegnate)


	
	def aggiungiBici(self, bici : list[Bici]):
		# rimuovo dal tree widget gli item e metto le ripsettive bici nella lista 'bici'
		while self.treewidget.topLevelItemCount() > 0:
			bici.append(self.treewidget.takeTopLevelItem(0).connectedObject)
		
		bici.sort(key = lambda bicicletta: bicicletta.getNumero()) # ordino la lista di bici in ordine di numero crescente

		# riaggiungo le bici al tree widget
		for bicicletta in bici:
			self.treewidget.addTopLevelItem(MyTreeWidgetItem(self.treewidget,
													   		   [str(bicicletta.getNumero()), 'Donna' if bicicletta.getTipo() == True else 'Uomo'], 
													   		   bicicletta))

	def _rimuoviBici(self, bici : Bici):
		i = 0
		while i < self.treewidget.topLevelItemCount():
			item = self.treewidget.topLevelItem(i)
			if bici.getNumero() == item.connectedObject.getNumero():
				self.treewidget.takeTopLevelItem(i)
				return
			i += 1
	

	def _btnIndietroClicked(self):
		self.btnIndietroClicked.emit()
		self.close()
		self.previous.show()

	
	def _readDict(self, pathsKey : str) -> dict:
		global paths
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dictionary = GestoreFile.leggiDictPickle(Path(paths[pathsKey]))
		except CorruptedFileError: # se camere non e' un dizionario
			self._showMessage(f"{Path(paths[pathsKey]).name} è stato corrotto irreversibilmente. Per risolvere il problema, eliminalo.", QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		return dictionary
	

	def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
