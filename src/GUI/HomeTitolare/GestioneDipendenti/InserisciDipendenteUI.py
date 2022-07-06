import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from src.Attori.Dipendente import Dipendente
from src.Attori.Ruolo import Ruolo
from src.Gestori.GestoreFile import GestoreFile
from src.Gestori.GestorePersona import GestorePersona
from src.GUI.HomeTitolare.GestioneDipendenti.InserimentoDatiDipendenteUI import InserimentoDatiDipendenteUI
from src.GUI.HomeTitolare.GestioneDipendenti.InserimentoCredenzialiUI import InserimentoCredenzialiUI
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
		self.page2 = InserimentoCredenzialiUI(self.page1)
		self.page2.widgetVecchiaPassword.deleteLater() # non servirà inserire la vecchia password

		self.addTab(self.page1, 'Inserici Dipendente')

		self.page1.btnAnnulla.clicked.connect(self.close)
		self.page1.btnAvanti.clicked.connect(self._btnAvantiClicked)

		self.page2.btnIndietro.clicked.connect(self._btnIndietroClicked)
		self.page2.btnInserisci.clicked.connect(self._btnInserisciClicked)

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


	def _btnAvantiClicked(self):
		if (self.page1.fieldsFilled(self.page1.lineEditLabelPairs) and self.page1.fieldsValid()
		   and not self.page1.isUserInSystem()):
			
			self.addTab(self.page2, 'Inserisci Dipendente')
			self.removeTab(0)


	def _btnIndietroClicked(self):
		self.addTab(self.page1, 'Inserisci Dipendente')
		self.removeTab(0)

	
	def _btnInserisciClicked(self):
		
		if self.page2.verifyFields():
			paths = GestoreFile.leggiJson(Path('paths.json'))
				
			nome = self.page1.lineEditNome.text(); 				 cognome = self.page1.lineEditCognome.text()
			dataNascita = self.page1.dateEdit.date().toPyDate(); luogoNascita = self.page1.lineEditLuogoNascita.text()
			email = self.page1.lineEditEmail.text(); 			 cellulare = self.page1.lineEditCellulare.text()
			
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