import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiCenaUI import ConfermaSceltaPastiCenaUI


class InserisciSceltaPastiCenaGiornoSuccessivoUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('InserisciSceltaPastiCenaGiornoSuccessivo.ui', Path.cwd()), self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

        self._fillTreeWidgetCena()

    def _fillTreeWidgetCena(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuCena = GestoreFile.leggiDictPickle(Path(paths['menuCena']))
        self.treewidgetAntipastiCena.clear()  # Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimiCena.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondiContorniCena.clear()  # che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandeCena.clear()  # uguale a come era prima
        if menuCena != {}:
            antipasti = menuCena["antipasto"]  # ottenere sottodizionario
            for k, v in antipasti.items():
                self.treewidgetAntipastiCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            primo = menuCena["primo"]  # ottenere sottodizionario
            for k, v in primo.items():
                self.treewidgetPrimiCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            secondoContorno = menuCena["secondoContorno"]  # ottenere sottodizionario
            for k, v in secondoContorno.items():
                self.treewidgetSecondiContorniCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            dolciBevande = menuCena["dolciBevande"]  # ottenere sottodizionario
            for k, v in dolciBevande.items():
                self.treewidgetDolciBevandeCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
        else:
            i = 0
            while i < 3:
                self.treewidgetAntipastiCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetPrimiCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetSecondiContorniCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetDolciBevandeCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                i += 1

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)


    def _btnAvantiClicked(self):
        self.widgetConfermaSceltaPastiCena = ConfermaSceltaPastiCenaUI(self)
        self.widgetConfermaSceltaPastiCena.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = InserisciSceltaPastiCenaGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())