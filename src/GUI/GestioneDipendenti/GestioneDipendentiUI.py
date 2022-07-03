import sys
import platform
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi

from src.Attori.Dipendente import Dipendente
from src.GUI.GestioneDipendenti.InserisciDipendenteUI import InserisciDipendenteUI
from src.GUI.GestioneDipendenti.VisualizzaDipendenteUI import VisualizzaDipendenteUI
from src.Gestori.GestoreFile import GestoreFile

class GestioneDipendentiUI(QTabWidget):
	
	def __init__(self, previous : QWidget):
		super().__init__()

		loadUi(GestoreFile.getAbsolutePath('gestioneDipendenti.ui', Path.cwd()), self)

		self.previous = previous

		if platform.system() == 'Darwin':
			position = QTabBar.ButtonPosition.LeftSide  # se sistema operativo è MacOs
		else:
			position = QTabBar.ButtonPosition.RightSide  # se sistema operativo è diverso da MacOs

		self.tabBar().tabButton(0,position).deleteLater()  # il tab button all'indice 0 della tab bar sarà eliminato
		self.tabBar().setTabButton(0, position, None)  # type: ignore
		self.tabBar().tabButton(1, position).deleteLater()  # il tab button all'indice 1 della tab bar sarà eliminato
		self.tabBar().setTabButton(1, position, None)  # type: ignore

		self.tabCloseRequested.connect(self.removeTab) # il click della x di una tab fa chiudere quella tab
		self._fillTreeWidgetDipendenti() # riempita la tree widget con i dipendenti in memoria
		self._connectButtons()

		self.msg = QMessageBox() # per futuri messaggi


	def _readDipendenti(self) -> dict:
		paths = GestoreFile.leggiJson(Path('paths.json'))
		try:
			dipendenti = GestoreFile.leggiDictPickle(Path(paths['dipendenti']))
		except TypeError:
			self._showMessage(f"{Path(paths['dipendenti']).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
								QMessageBox.Icon.Critical, 'Errore critico')
			self.close()
			raise
		
		return dipendenti


	def _fillTreeWidgetDipendenti(self):
		
		dipendenti = self._readDipendenti()

		for dipendente in dipendenti.values():
			self.treeWidgetDipendenti.addTopLevelItem(QTreeWidgetItem([f"{dipendente.getId()}" , dipendente.getCognome(), 
													  dipendente.getNome()], 0))

		self.treeWidgetDipendenti.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder) # cognomi in ordine alfabetico

	
	def _connectButtons(self):
		self.btnNuovoDipendente.clicked.connect(self._btnNuovoDipendenteClicked)
		self.btnVisualizzaAccount.clicked.connect(self._btnVisualizzaAccountClicked)
		self.btnVisualizzaAssenze.clicked.connect(self._btnVisualizzaAssenzeClicked)
		self.btnIndietro1.clicked.connect(self.btnIndietroClicked)
		self.btnIndietro2.clicked.connect(self.btnIndietroClicked)

	
	def _btnVisualizzaAccountClicked(self):
		if self.treeWidgetDipendenti.currentItem() == None:
			self._showMessage("Seleziona prima il dipendente di cui viualizzare l'account", QMessageBox.Icon.Warning, 'Errore')
		else:
			id = self.treeWidgetDipendenti.currentItem().text(0) # prendo l'id del dipendente slezionato
			dipendenti = self._readDipendenti()
			self.widgetVisualizzaDipendente = VisualizzaDipendenteUI(dipendenti[int(id)])
			self.addTab(self.widgetVisualizzaDipendente, f"Visualizza ID {dipendenti[int(id)].getId()}")
			index = self.count() - 1
			self.setCurrentIndex(index)
			
			def func():
				self.treeWidgetDipendenti.takeTopLevelItem(
					self.treeWidgetDipendenti.indexOfTopLevelItem(self.treeWidgetDipendenti.currentItem())
				) # rimuove dal tree widget dei dipendenti la riga del dipendente eliminato
				self.removeTab(index) # chiude la tab che visualizzava il dipendente eliminato
			
			self.widgetVisualizzaDipendente.dipendenteEliminato.connect(func)


	def _btnVisualizzaAssenzeClicked(self):
		pass
	

	def _btnNuovoDipendenteClicked(self):
		def addSortedItem(dipendente : Dipendente):				# diminuisco l'id di 1 perche il dipendente passato a questa funzione è stato creato subito dopo la creazione della sua 'copia' 
			self.treeWidgetDipendenti.addTopLevelItem(QTreeWidgetItem([f"{dipendente.getId() - 1}", dipendente.getCognome(), # che è stata salvata sul file dipendenti.pickle
													  dipendente.getNome()], 0))
			self.treeWidgetDipendenti.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder) # cognomi in ordine alfabetico
		
		self.widgetInserisciDipendente = InserisciDipendenteUI(self)
		self.widgetInserisciDipendente.show()
		self.widgetInserisciDipendente.dipendenteAggiunto.connect(addSortedItem)
	

	def btnIndietroClicked(self):
		self.previous.show()
		self.close()
		

	def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
		self.msg.setWindowTitle(windowTitle)
		self.msg.setIcon(icon)
		self.msg.setText(text)
		self.msg.show()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWidget = GestioneDipendentiUI(QWidget())
	mainWidget.show()
	sys.exit(app.exec_())