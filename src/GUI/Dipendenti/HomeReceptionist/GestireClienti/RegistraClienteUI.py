from datetime import date
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src.Attori.Persona import Persona

from src.Gestori.GestoreFile import GestoreFile
from src.GUI.FormUI import FormUI
from src.Gestori.GestorePersona import GestorePersona
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.exceptions import CorruptedFileError


class RegistraClienteUI(FormUI):

	clienteRegistrato = QtCore.pyqtSignal(Persona)

	def __init__(self, previous : QWidget = None): # type: ignore
		super().__init__()

		loadUi(GestoreFile.absolutePath('registraCliente.ui', Path.cwd()), self)

		self.previous = previous
		self.lineeditLabelPairs = {
			self.lineeditNome : self.labelNome,
			self.lineeditCognome : self.labelCognome,
			self.lineeditLuogoNascita : self.labelLuogoNascita,
			self.lineeditEmail : self.labelEmail,
			self.lineeditCellulare : self.labelCellulare
		}
		self._setValidators() # impostati i vlìalidator per le line edit da controllare
		self._setColorHints() # impostati i colori del testo
		self._setUpperCase() # maiuscola automatica per nome, cognome e luogo di nascita
		self.dateedit.setMaximumDate(date.today()) # il cliente non può essere nato nel futuro
		self._connectButtons()

		self.msg = QMessageBox()


	def _setValidators(self):
		self.lineeditNome.setValidator(GUIUtils.validators['soloLettere'])
		self.lineeditCognome.setValidator(GUIUtils.validators['soloLettere'])
		self.lineeditLuogoNascita.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression('.+\\(.+\\)')))
		self.lineeditEmail.setValidator(GUIUtils.validators['email'])
		self.lineeditCellulare.setValidator(GUIUtils.validators['cellulare'])


	def _setColorHints(self):
		self.lineeditLuogoNascita.textChanged.connect(self._setColorHint)
		self.lineeditEmail.textChanged.connect(self._setColorHint)
		self.lineeditCellulare.textChanged.connect(self._setColorHint)
	

	def _setUpperCase(self):
		def textToUpper(oldPos, newPos):
			if oldPos == 0 and newPos == 1:
				lineEdit = self.sender()
				text = lineEdit.text()
				lineEdit.setText(text[0].upper() + text[1:])
		
		self.lineeditNome.cursorPositionChanged.connect(textToUpper)
		self.lineeditCognome.cursorPositionChanged.connect(textToUpper)
		self.lineeditLuogoNascita.cursorPositionChanged.connect(textToUpper)


	def _connectButtons(self):
		self.btnIndietro.clicked.connect(self._btnIndietroClicked)
		self.btnHelpAsterisco.clicked.connect(self._btnHelpAsteriscoClicked)

    
	def _btnIndietroClicked(self):
		self.close()
		self.previous.show()


	def _btnHelpAsteriscoClicked(self):
		self._showMessage("L'asterisco accanto ad ogni campo vuol dire che la registrazione non può essere effettuata se prima tutti i campi non sono stati inseriti.", QMessageBox.Icon.Information)
	

	def _readClienti(self):
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			clienti = GestoreFile.leggiDictPickle(Path(paths['clienti']))
		except CorruptedFileError:
			self._showMessage(f"{Path(paths['clienti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		
		return clienti


	def isClienteInSystem(self) -> bool:
		toReturn = False
		clienti = self._readClienti()
		for cliente in clienti.values():
			if (cliente.getNome() == self.lineeditNome.text() and cliente.getCognome() == self.lineeditCognome.text() and 
				cliente.getDataNascita() == self.dateedit.date().toPyDate() and cliente.getLuogoNascita() == self.lineeditLuogoNascita.text()):
				self._showMessage('Questo cliente è già presente nel sistema, non può essere inserito nuovamente.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = True
		return toReturn


	def fieldsValid(self) -> bool:
		toReturn = True
		styleSheet = f"color: rgb(0, 170, 0);"
		if [self.lineeditEmail.styleSheet(), self.lineeditCellulare.styleSheet(), self.lineeditLuogoNascita.styleSheet()] != [styleSheet] * 3: # se le 3 line edit non hanno il testo verde
			self._showMessage('I dati in rosso non sono accettabili.\nQuando lo saranno il loro colore diventerà verde.', QMessageBox.Icon.Warning, 'Errore')
			toReturn = False
		return toReturn
	

	def salvaCliente(self):
		"""This method saves the customer in the file system, picking the data from this object fields."""
		if self.fieldsFilled(self.lineeditLabelPairs) and not self.isClienteInSystem() and self.fieldsValid():
			paths = GestoreFile.leggiJson(Path('paths.json'))
			try:
				GestorePersona.aggiungiPersona(Path(paths['clienti']), self.lineeditNome.text(), self.lineeditCognome.text(),
						self.dateedit.date().toPyDate(), self.lineeditLuogoNascita.text(), self.lineeditEmail.text(), self.lineeditCellulare.text())
			except CorruptedFileError:
				self._showMessage(f"{Path(paths['clienti'])} has been corrupted. To fix the issue, delete it.",
								  QMessageBox.Icon.Warning, 'Errore')
				self.close()
				raise
			
			clienti = GestoreFile.leggiDictPickle(Path(paths['clienti']))
			for cliente in clienti.values():
				if (cliente.getNome() == self.lineeditNome.text() and cliente.getCognome() == self.lineeditCognome.text() and 
					cliente.getDataNascita() == self.dateedit.date().toPyDate() and cliente.getLuogoNascita() == self.lineeditLuogoNascita.text()):
					self.clienteRegistrato.emit(cliente)
					return
	
	
	def clear(self):
		self.lineeditNome.clear()
		self.lineeditCognome.clear()
		self.lineeditLuogoNascita.clear()
		self.lineeditEmail.clear()
		self.lineeditCellulare.clear()
		self.dateedit.setDate(date(2000, 1, 1))

		# rimuovo i colori del testo di email, cellulare e luogo di nascita
		font = self.lineeditLuogoNascita.font()
		self.lineeditLuogoNascita.setStyleSheet('') 
		self.lineeditEmail.setStyleSheet('')
		self.lineeditCellulare.setStyleSheet('')
		# reimposto i font perchè con lo svuotamento dello style sheet si azzera anche il font
		self.lineeditLuogoNascita.setFont(font)
		self.lineeditEmail.setFont(font)
		self.lineeditCellulare.setFont(font)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RegistraClienteUI(QWidget())
    mainWidget.show()
    sys.exit(app.exec_())