from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src.GUI.GestioneDipendenti.FormUI import FormUI

class InserimentoCredenzialiDipendenteUI(FormUI):

	def __init__(self, previous : QWidget = None): # type: ignore
		super().__init__()
		
		self.previous = previous # per tornare alla pagina precedente al click del bottone "indietro"
		
		loadUi('ui/Titolare/GestisciDipendenti/inserimentoCredenzialiDipendente.ui', self)
		
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
		self._connectEye(eyeBtn2, self.lineEditConfermaPassword)																		 # 8 o più caratteri, almeno una maiuscola, una minuscola e un numero
		
		self.lineEditPassword.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$")))


	def _connectEye(self, eyeButton : QToolButton, lineEdit : QLineEdit):
		def showHidePassword(checked):
			if checked:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
				eyeButton.setIcon(QtGui.QIcon('files/icons/eye-close.jpg'))
			else:
				lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
				eyeButton.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))
		
		eyeButton.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))
		eyeButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
		eyeButton.setCheckable(True)
		eyeButton.clicked.connect(showHidePassword)
		widgetAction = QWidgetAction(lineEdit)
		widgetAction.setDefaultWidget(eyeButton)
		lineEdit.addAction(widgetAction, QLineEdit.ActionPosition.TrailingPosition) # azione aggiunta nella parte destra della line edit


	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()