from pathlib import Path
from datetime import date, timedelta

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.exceptions import CorruptedFileError

class VisualizzaSceltaPastiCenaUI(QWidget):
    
    def __init__(self, previous: QWidget):
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('VisualizzaSceltaPastiCena.ui', Path.cwd()), self)
        
        self.previous = previous
        self._resizeColumns()
        self._connectButtons()

        self.msg = QMessageBox()

        self.dateEditCena.setMinimumDate(date.today())
        self.dateEditCena.setMaximumDate(date.today() + timedelta(days=1))
    

    def _resizeColumns(self):
        self.treewidgetAntipasti.header().resizeSection(0, 250)
        self.treewidgetPrimi.header().resizeSection(0, 250)
        self.treewidgetSecondiContorni.header().resizeSection(0, 250)
        self.treewidgetDolciBevande.header().resizeSection(0, 250)


    def _connectButtons(self):
        self.btnCerca.clicked.connect(self._btnCercaClicked)
        self.btnElimina.clicked.connect(self._btnEliminaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)


    def _btnCercaClicked(self):
        camere = self._readCamere()
        numeroCamera = int(self.comboboxCena.currentText())
        camera = camere[numeroCamera]
        if not camera.isAssegnato():
            self.previous._showMessage(
                f"La camera {self.comboboxCena.currentText()} non è attualmente assegnata.",
                QMessageBox.Icon.Warning)
            return
        try:
            global cena
            cena = camera.getVacanzaAttuale().getSceltePastiCena()[
                self.dateEditCena.date().toPyDate()]
        except:
            self.previous._showMessage(
                f"Per la camera {self.comboboxPranzo.currentText()} non esiste alcuna prenotazione nella data inserita",
                QMessageBox.Icon.Warning)
            return

        antipasti = cena['antipasti']
        primi = cena['primo']
        secondiContorni = cena['secondiContorni']
        dolciBevande = cena['dolciBevande']

        self.treewidgetAntipasti.clear() # permette di svuotare il treewidget di interesse
        for k, v in antipasti.items():
            self.treewidgetAntipasti.addTopLevelItem(QTreeWidgetItem([k, v]))
        self.treewidgetPrimi.clear()
        for k, v in primi.items():
            self.treewidgetPrimi.addTopLevelItem(QTreeWidgetItem([k, v]))
        self.treewidgetSecondiContorni.clear()
        for k, v in secondiContorni.items():
            self.treewidgetSecondiContorni.addTopLevelItem(QTreeWidgetItem([k, v]))
        self.treewidgetDolciBevande.clear()
        for k, v in dolciBevande.items():
            self.treewidgetDolciBevande.addTopLevelItem(QTreeWidgetItem([k, v]))


    def _btnEliminaClicked(self):
        data = self.dateEditCena.date().toPyDate()
        numeroCamera = int(self.comboboxCena.currentText())
        del camere[numeroCamera].getVacanzaAttuale().getSceltePastiCena()[data]
        camere[numeroCamera].getVacanzaAttuale().setSceltePastiCena(cena)
        GestoreFile.salvaPickle(camere, Path(paths['camere']))
        self.previous._showMessage(
            f"La scelta dei pasti del pranzo della camera {self.comboboxCena.currentText()} per la data {data.strftime('%d/%m/%Y')} è stata eliminata correttamente",
            QMessageBox.Icon.Information)
        self.close()
        self.previous.show()


    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()


    def _readCamere(self):
        global paths
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            global camere
            camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
        except CorruptedFileError:
            self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.",
                                       QMessageBox.Icon.Warning, 'Errore')
            self.close()
            self.previous.close()
            raise
        return camere


    def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()
