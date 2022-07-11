import sys
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.EliminaClienteUI import EliminaClienteUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.ModificaClienteUI import ModificaClienteUI
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaClienteUI import RicercaClienteUI
from src.Gestori.GestoreFile import GestoreFile


class VisualizzaClienteUI(QWidget):

	def __init__(self, previous : QWidget = None): # type: ignore
		super().__init__()

		loadUi(GestoreFile.absolutePath('visualizzaCliente.ui', Path.cwd()), self)

		self.previous = previous
		self._hideElements()
		self.groupboxSchedaCliente.hide()

		self._connectButtons()

	
	def _hideElements(self):
		self.groupboxSchedaCliente.hide()
		self.btnModifica.hide()
		self.btnElimina.hide()


	def _connectButtons(self):
		self.btnRicerca.clicked.connect(self._btnRicercaClicked)
		self.btnModifica.clicked.connect(self._btnModificaClicked)
		self.btnElimina.clicked.connect(self._btnEliminaClicked)

	
	def _btnRicercaClicked(self):
		self.widgetRicercaCliente = RicercaClienteUI(self)
		self.widgetRicercaCliente.clienteTrovato.connect(self._fillFields)
		self.widgetRicercaCliente.show()
	

	def _fillFields(self, cliente : Persona):
		self.lineeditID.setText(str(cliente.getId()))
		self.lineeditNome.setText(cliente.getNome())
		self.lineeditCognome.setText(cliente.getCognome())
		self.lineeditLuogoNascita.setText(cliente.getLuogoNascita())
		self.lineeditEmail.setText(cliente.getEmail())
		self.lineeditCellulare.setText(cliente.getCellulare())
		self.dateedit.setDate(cliente.getDataNascita())
		if self.groupboxSchedaCliente.isHidden():
			self.groupboxSchedaCliente.show()
			self.btnModifica.show()
			self.btnElimina.show()


	def _btnModificaClicked(self):
		self.close()
		self.widgetModificaCliente = ModificaClienteUI(self)
		self.widgetModificaCliente.show()
		
	
	def _btnEliminaClicked(self):
		self.close()
		self.widgetEliminaCliente = EliminaClienteUI(self)
		self.widgetEliminaCliente.show()
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaClienteUI()
    mainWidget.show()
    sys.exit(app.exec_())