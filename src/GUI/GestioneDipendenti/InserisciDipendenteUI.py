import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from src.Attori.Dipendente import Dipendente
from src.Attori.Ruolo import Ruolo
from src.Gestori.GestoreFile import GestoreFile
from src.Gestori.GestorePersona import GestorePersona
from src.GUI.GestioneDipendenti.InserimentoDatiDipendenteUI import InserimentoDatiDipendenteUI
from src.GUI.GestioneDipendenti.InserimentoCredenzialiDipendenteUI import InserimentoCredenzialiDipendenteUI
from src.Utilities.exeptions import DuplicateError
from src.Utilities.encrypter import encrypt


class InserisciDipendenteUI(QTabWidget):

	dipendenteAggiunto = QtCore.pyqtSignal(Dipendente)

	def __init__(self, previous : QWidget = None): # type: ignore
		super().__init__()

		self.setWindowTitle('Hotel: Inserisci Dipendente')
		self.setMinimumSize(600, 520)
		self.setFont(QtGui.QFont('Arial', 10))

		self.previous = previous
		self.page1 = InserimentoDatiDipendenteUI(previous)
		self.page2 = InserimentoCredenzialiDipendenteUI(self.page1)

		self.addTab(self.page1, 'Inserici Dipendente')

		self.page1.btnAnnulla.clicked.connect(self.close)
		self.page1.btnAvanti.clicked.connect(self._avantiClicked)

		self.page2.btnIndietro.clicked.connect(self._indietroClicked)
		self.page2.btnInserisci.clicked.connect(self._inserisciDipendenteClicked)

		self.msg = QMessageBox() # per futuri messaggi
	

	def _readDipendenti(self) -> dict:
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dipendenti = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		except TypeError:
			self._showMessage(f"{Path(paths['dipendenti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								 QMessageBox.Icon.Critical, 'Errore')
			self.close()
			raise
		
		return dipendenti


	def _avantiClicked(self):
		for lineEdit in self.page1.lineEditLabelPairs:
			if lineEdit.text().strip() == '': # se la line edit è vuota o contiene solo spazi
				self._showMessage('Inserisci tutti i campi, per favore.', QMessageBox.Icon.Warning, 'Errore')
				return
		
		dipendenti = self._readDipendenti()
		for dipendente in dipendenti.values():
			if (dipendente.getNome() == self.page1.lineEditNome.text() and dipendente.getCognome() == self.page1.lineEditCognome.text() and 
                dipendente.getDataNascita() == self.page1.dateEdit.date().toPyDate() and dipendente.getLuogoNascita() == self.page1.lineEditLuogoNascita.text()):
				self._showMessage('Questo dipendente è già presente nel sistema, non può essere inserito nuovamente.', QMessageBox.Icon.Warning, 'Errore')
				return

		styleSheet = f"color: rgb(0, 170, 0); font-family: Arial; font-size: 10pt"
		if [self.page1.lineEditEmail.styleSheet(), self.page1.lineEditCellulare.styleSheet(), self.page1.lineEditIBAN.styleSheet()] != [styleSheet] * 3: # se le 3 line edit non hanno il testo verde
			self._showMessage('I dati in rosso non sono accettabili.\nQuando lo saranno il loro colore diventerà verde.', QMessageBox.Icon.Warning, 'Errore')
			return
		
		self.addTab(self.page2, 'Inserisci Dipendente')
		self.removeTab(0)


	def _indietroClicked(self):
		self.addTab(self.page1, 'Inserisci Dipendente')
		self.removeTab(0)

	
	def _inserisciDipendenteClicked(self):
		def isPasswordCorrect() -> bool:
			toReturn = True
			if self.page2.lineEditPassword.validator().validate(self.page2.lineEditPassword.text(), 0)[0] != QtGui.QValidator.State.Acceptable:
				self._showMessage('La password non rispetta la struttura richiesta.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = False
			elif self.page2.lineEditConfermaPassword.text() != self.page2.lineEditPassword.text():
				self._showMessage('La password e la sua conferma non corrispondono.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = False
			return toReturn

		def isUsernameUsed(paths : dict) -> bool:
			toReturn = False
			dipendenti = self._readDipendenti()
			for dipendente in dipendenti.values():
				if dipendente.getUsername() == self.page2.lineEditUsername.text():
					self._showMessage('Username già in uso, inserirne un altro.', QMessageBox.Icon.Warning, 'Errore')
					toReturn = True
			return toReturn
		
		for lineEdit in self.page2.lineEditLabelPairs:
			if lineEdit.text().strip() == '': # se la line edit è vuota o contiene solo spazi
				self._showMessage('Inserisci tutti i campi, per favore.', QMessageBox.Icon.Warning, 'Errore')
				return
		
		paths = GestoreFile.leggiJson(Path('paths.json'))
		
		if isPasswordCorrect() and not isUsernameUsed(paths):
			nome = self.page1.lineEditNome.text(); 				cognome = self.page1.lineEditCognome.text()
			dataNascita = self.page1.dateEdit.date().toPyDate(); luogoNascita = self.page1.lineEditLuogoNascita.text()
			email = self.page1.lineEditEmail.text(); 			cellulare = self.page1.lineEditCellulare.text()
			
			datiAggiuntivi = {
				'IBAN' : self.page1.lineEditIBAN.text(),
				'turno' : True if self.page1.comboBoxTurno.currentText() == 'Mattina' else False,
				'ruolo' : Ruolo.RECEPTIONIST if self.page1.comboBoxRuolo.currentText() == 'Receptionist' else Ruolo.CAMERIERE,
				'username' : self.page2.lineEditUsername.text(),
				'password' : encrypt(self.page2.lineEditPassword.text())
			}
			try:
				GestorePersona.aggiungiPersona(Path(paths['dipendenti']), nome, cognome, dataNascita, luogoNascita, email, cellulare, **datiAggiuntivi)
			except DuplicateError:
				pass # è stato già verificato che il dipendente non è già presente nel sistema
			self.dipendenteAggiunto.emit(Dipendente(nome, cognome, dataNascita, luogoNascita, email, cellulare, datiAggiuntivi['IBAN'],
									  datiAggiuntivi['turno'], datiAggiuntivi['ruolo'], datiAggiuntivi['username'], datiAggiuntivi['password']))
			
			self._showMessage('Il dipendente è stato inserito con successo!', QMessageBox.Icon.Information)
			self.close()
	
	
	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()




if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = InserisciDipendenteUI()
	mainWidget.show()
	sys.exit(app.exec_())