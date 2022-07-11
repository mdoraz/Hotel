import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.Dipendenti.HomeCamerieri.GestioneCucinaCamerieri.ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI import \
    ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI


class PrenotaColazioneInCameraGiornoSuccessivoUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('PrenotaColazioneInCameraGiornoSuccessivo.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

        self._fillTreeWidgetColazioneInCamera()

    def _fillTreeWidgetColazioneInCamera(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuColazione = GestoreFile.leggiDictPickle(Path(paths['menuColazione']))
        self.treewidgetDolceColazioneInCamera.clear()  # Queste tre righe che richiamano il metodo clear del treeWidget
        self.treewidgetSalatoColazioneInCamera.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetBevandeColazioneInCamera.clear()  # che se clicchiamo annulla il treeWidget torna come era prima
        if menuColazione != {}:
            dolci = menuColazione["dolce"]  # ottenere sottodizionario
            for k, v in dolci.items():
                self.treewidgetDolceColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            salato = menuColazione["salato"]  # ottenere sottodizionario
            for k, v in salato.items():
                self.treewidgetSalatoColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            bevande = menuColazione["bevande"]  # ottenere sottodizionario
            for k, v in bevande.items():
                self.treewidgetBevandeColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k, v], 0))
        else:
            i = 0
            while i < 3:
                self.treewidgetDolceColazioneInCamera.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetSalatoColazioneInCamera.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetBevandeColazioneInCamera.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                i += 1


    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnAvantiClicked(self):
        self.close()
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo = ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI(self)
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo.show()

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = PrenotaColazioneInCameraGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())
