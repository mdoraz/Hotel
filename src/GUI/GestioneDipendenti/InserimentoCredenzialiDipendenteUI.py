from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Utilities.GUIUtils import GUIUtils
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.GestioneDipendenti.FormUI import FormUI

class InserimentoCredenzialiDipendenteUI(FormUI):

	def __init__(self, previous : QWidget = None): # type: ignore
		super().__init__()
		
		self.previous = previous # per tornare alla pagina precedente al click del bottone "indietro"
		
		loadUi(GestoreFile.absolutePath('inserimentoCredenzialiDipendente.ui', Path.cwd()), self)
		
		self.msg = QMessageBox() #per futuri messaggi

		self.lineEditLabelPairs = {
			self.lineEditUsername : self.labelUsername,
			self.lineEditPassword : self.labelPassword,
			self.lineEditConfermaPassword : self.labelConfermaPassword
		}
		self.hideLabels(self.lineEditLabelPairs) # all'inizio tutte le label sono nascoste
		self.connectLabelAndText(self.lineEditLabelPairs) # rende la label visibile solo se la corrispondente line edit non è vuota.
		
		eyeBtn1 = QToolButton() # creati i bottoni per mostrare/nascondere la password
		eyeBtn2 = QToolButton()
		self._connectEye(eyeBtn1, self.lineEditPassword) # collega eyeBtn alla line edit corrispondente
		self._connectEye(eyeBtn2, self.lineEditConfermaPassword)
		
		self.lineEditPassword.setValidator(GUIUtils.validators['password'])


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



	def _connectEye(self, eyeButton : QToolButton, lineEdit : QLineEdit):
		def showHidePassword(checked):
			if checked:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
				eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-closed.png', Path.cwd())))
			else:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
				eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-opened.png', Path.cwd())))

		eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-opened.png', Path.cwd())))
		eyeButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
		eyeButton.setCheckable(True)
		eyeButton.clicked.connect(showHidePassword)
		widgetAction = QWidgetAction(lineEdit)
		widgetAction.setDefaultWidget(eyeButton)
		lineEdit.addAction(widgetAction, QLineEdit.ActionPosition.TrailingPosition) # azione aggiunta nella parte destra della line edit

	
	def isPasswordCorrect(self) -> bool:
		"""Returns true if the password respects the correct structure."""
		toReturn = True
		if self.lineEditPassword.validator().validate(self.lineEditPassword.text(), 0)[0] != QtGui.QValidator.State.Acceptable:
			self._showMessage('La password non rispetta la struttura richiesta.', QMessageBox.Icon.Warning, 'Errore')
			toReturn = False
		elif self.lineEditConfermaPassword.text() != self.lineEditPassword.text():
			self._showMessage('La password e la sua conferma non corrispondono.', QMessageBox.Icon.Warning, 'Errore')
			toReturn = False
		return toReturn


	def isUsernameUsed(self) -> bool:
		"""Returns true if the username is not already in use."""
		toReturn = False
		dipendenti = self._readDipendenti()
		for dipendente in dipendenti.values():
			if dipendente.getUsername() == self.lineEditUsername.text():
				self._showMessage('Username già in uso, inserirne un altro.', QMessageBox.Icon.Warning, 'Errore')
				toReturn = True
		return toReturn

	
	def verifyFields(self):
		"""Returns true if all fields are filled, the password respects the correct structure and username is not already in use."""
		toReturn = False
		if (self.fieldsFilled(self.lineEditLabelPairs) and self.isPasswordCorrect() and not self.isUsernameUsed()):
			toReturn = True
		return toReturn
		
	
	def addField(self, index : int, textLabel : str):
		widget = QWidget()
		gridLayout = QGridLayout(widget)
		# elementi del layout
		hSpacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		hSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		newLabel = QLabel(textLabel)
		newLineEdit = QLineEdit()
		newLineEdit.setMinimumSize(320, 0)
		newLineEdit.setFrame(False)
		newLineEdit.setPlaceholderText('Vecchia password')
		# popolo il layout del widget
		gridLayout.addItem(hSpacer1, 0, 0)
		gridLayout.addWidget(newLabel, 0, 1)
		gridLayout.addItem(hSpacer2, 0, 2)
		gridLayout.addWidget(newLineEdit, 1, 1)
		# aggiungo il widget al layout del widget dell'inserimento delle credenziali
		self.layout().insertWidget(index, widget)
		
		newLabel.hide()
		self.connectLabelAndText({newLineEdit : newLabel})
