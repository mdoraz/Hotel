from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Servizi.Bici import Bici
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.customQtClasses import MyTreeWidgetItem
from src.Utilities.exceptions import CorruptedFileError


class AssegnaBiciSenzaPrenotazioneUI(QWidget):

	btnIndietroClicked = QtCore.pyqtSignal()
	
	def __init__(self, previous: QWidget):
		super().__init__()
		
		loadUi(GestoreFile.absolutePath('AssegnaBiciSenzaPrenotazione.ui', Path.cwd()), self)

		self.previous = previous

		self._fillTreewidgetBici()
		self._fillComboboxCamere()
		self._connectButtons()

		self.msg = QMessageBox()


	def _fillTreewidgetBici(self):
		#global biciclette
		biciclette = self._readDict('bici')
		
		for bicicletta in biciclette.values():
			if not bicicletta.isAssegnato(): # aggiungo al tree widget solo le biciclette attualmente non assegnate
				self.treewidget.addTopLevelItem(MyTreeWidgetItem(self.treewidget,
																 [str(bicicletta.getNumero()), 'Donna' if bicicletta.getTipo() == True else 'Uomo'],
																 bicicletta))

	
	def _fillComboboxCamere(self):
		#global camere
		camere = self._readDict('camere')

		for camera in camere.values():
			if camera.isAssegnato(): # aggiungo alla combo box solo i numeri delle camere assegnate
				self.combobox.addItem(str(camera.getNumero()))


	def _connectButtons(self):
		self.btnAssegna.clicked.connect(self._btnAssegnaClicked)
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)


	def _btnAssegnaClicked(self):
		if len(self.treewidget.selectedItems()) == 0:
			self._showMessage('Selezionare almeno una bici da assegnare.', QMessageBox.Icon.Warning, 'Errore')
			return

		camere = self._readDict('camere')
		biciclette = self._readDict('bici')
		numeroCamera = int(self.combobox.currentText())
		datiAssegnamento = {
			'camera' : camere[numeroCamera],
			'prenotazione' : None,
			'biciclette' : biciclette,
			'camere' : camere
		}
		for item in self.treewidget.selectedItems():
			bici = item.connectedObject
			bici.assegna(datiAssegnamento)
			self._rimuoviBici(bici) # rimuovo la bici dal tree widget poich?? non ?? pi?? assegnabile
		
		self._showMessage('Biciclette assegnate con successo!', QMessageBox.Icon.Information)

	
	def aggiungiBici(self, bici : list[Bici]): # inserimento ordinato di una bici nel tree widget
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
			self._showMessage(f"{Path(paths[pathsKey]).name} ?? stato corrotto irreversibilmente. Per risolvere il problema, eliminalo.", QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		return dictionary


	def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
