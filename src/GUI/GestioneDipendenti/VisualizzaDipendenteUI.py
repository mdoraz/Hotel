from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

from src.Gestori.GestoreFile import GestoreFile
from src.Attori.Dipendente import Dipendente

class VisualizzaDipendenteUI(QWidget):

	def __init__(self, dipendente : Dipendente, parent : QWidget = None):  # type: ignore
		super().__init__(parent)

		loadUi('ui/Titolare/visualizzaDipendente.ui', self)

		self.dipendente = dipendente
		self._fillFields()
		self._connectButtons()

		self.msg = QMessageBox() # perr futuri messaggi


	def _readDipendenti(self):
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dipendenti = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		except TypeError:
			self._showMessage(f"{Path(paths['dipendenti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		
		return dipendenti

	def _fillFields(self):
		# riempio l'intestazione
		self.labelIntestazioneNome.setText(f"{self.dipendente.getNome()} {self.dipendente.getCognome()}")
		self.labelIntestazioneID.setText(f"ID: {self.dipendente.getId()}")
		# riempio i dati personali
		self.labelNome.setText(self.dipendente.getNome())
		self.labelCognome.setText(self.dipendente.getCognome())
		self.labelDataNascita.setText(self.dipendente.getDataNascita().strftime('%d/%m/%Y'))
		self.labelLuogoNascita.setText(self.dipendente.getLuogoNascita())
		# riempio i dati lavorativi
		self.lineEditRuolo.setText(self.dipendente.getAutorizzazione().name.capitalize())
		self.lineEditTurno.setText('Mattina' if self.dipendente.getTurno() == 1 else 'Pomeriggio')
		self.lineEditIBAN.setText(self.dipendente.getIBAN())
		self.lineEditStipendio.setText(f"{self.dipendente.getStipendio()}")
		# riempio i contatti
		self.lineEditEmail.setText(self.dipendente.getEmail())
		self.lineEditCellulare.setText(self.dipendente.getCellulare())
		# riempio le credenziali
		self.lineEditUsername.setText(self.dipendente.getUsername())
		self.lineEditPassword.setText('password')


	def _connectButtons(self):

		self.btnDatiLavorativi.clicked.connect(self._modificaDatiLavorativiClicked)
		self.btnContatti.clicked.connect(self._modificaContattiClicked)
		self.btnCredenziali.clicked.connect(self._modificaCredenzialiClicked)


	def _modificaDatiLavorativiClicked(self):
		self.btnDatiLavorativi.setText('Salva')
		self.btnDatiLavorativi.clicked.connect(self._salvaDatiLavoraiviClicked)
		# modificare i campi per consentire la modifica
	

	def _salvaDatiLavoraiviClicked(self):
		pass #readDipendenti, sostituisco il dipendente con la chiave ID, salvo su pickle


	def _modificaContattiClicked(self):
		self.btnContatti.setText('Salva')
		self.btnContatti.clicked.connect(self._salvaContattiClicked)
		# modifica campi

	
	def _salvaContattiClicked(self):
		pass # readDipendenti, sostituisco il dipendente con la chiave ID, salvo su pickle


	def _modificaCredenzialiClicked(self):
		self.btnCredenziali.setText('Salva')
		self.btnCredenziali.clicked.connect(self._salvaCredenzialiClicked)
		# modifica campi

	
	def _salvaCredenzialiClicked(self):
		pass # readDipendenti, sostituisco il dipendente con la chiave ID, salvo su pickle

	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()
