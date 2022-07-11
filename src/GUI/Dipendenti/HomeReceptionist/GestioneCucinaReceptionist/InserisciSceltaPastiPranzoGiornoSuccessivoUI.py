import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiPranzoUI import ConfermaSceltaPastiPranzoUI


class InserisciSceltaPastiPranzoGiornoSuccessivoUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('InserisciSceltaPastiPranzoGiornoSuccessivo.ui',Path.cwd()), self)
        self.setMinimumSize(600, 700)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

        self._fillTreeWidgetPranzo()

    def _fillTreeWidgetPranzo(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuPranzo = GestoreFile.leggiDictPickle(Path(paths['menuPranzo']))
        self.treewidgetAntipastiPranzo.clear()  # Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimoPranzo.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondoContornoPranzo.clear()  # che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandePranzo.clear()  # uguale a come era prima
        if menuPranzo != {}:
            antipasti = menuPranzo["antipasto"] #ottenere sottodizionario
            for k,v in antipasti.items():
                self.treewidgetAntipastiPranzo.addTopLevelItem(QTreeWidgetItem([k,v], 0))
            primo = menuPranzo["primo"]  # ottenere sottodizionario
            for k, v in primo.items():
                self.treewidgetPrimoPranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            secondoContorno = menuPranzo["secondoContorno"]  # ottenere sottodizionario
            for k, v in secondoContorno.items():
                self.treewidgetSecondoContornoPranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            dolciBevande = menuPranzo["dolciBevande"]  # ottenere sottodizionario
            for k, v in dolciBevande.items():
                self.treewidgetDolciBevandePranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
        else:
            i = 0
            while i < 3:
                self.treewidgetAntipastiPranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetPrimoPranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetSecondoContornoPranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetDolciBevandePranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                i += 1

    def _connectButtons(self):
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self.close)

    def _btnAvantiClicked(self):
        self.widgetConfermaSceltaPastiPranzo = ConfermaSceltaPastiPranzoUI(self)
        self.widgetConfermaSceltaPastiPranzo.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = InserisciSceltaPastiPranzoGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())