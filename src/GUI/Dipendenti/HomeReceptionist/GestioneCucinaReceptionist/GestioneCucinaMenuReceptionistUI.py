from datetime import date, timedelta

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiCenaUI import \
    ConfermaSceltaPastiCenaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.ConfermaSceltaPastiPranzoUI import \
    ConfermaSceltaPastiPranzoUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.VisualizzaSceltaPastiCenaUI import \
    VisualizzaSceltaPastiCenaUI
from src.GUI.Dipendenti.HomeReceptionist.GestioneCucinaReceptionist.VisualizzaSceltaPastiPranzoUI import \
    VisualizzaSceltaPastiPranzoUI
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.exceptions import CorruptedFileError


class GestioneCucinaMenuReceptionistUI(QTabWidget):
   
    def __init__(self, previous: QWidget ):
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('GestioneCucina.ui', Path.cwd()), self)
        
        self.previous = previous
        self._connectButtons()

        self._hideWidget()
        self._resizeColumns()

        self._fillTreeWidgetColazioneInCamera()
        self._fillTreeWidgetPranzo()
        self._fillTreeWidgetCena()

        self.msg = QMessageBox()


    def _hideWidget(self):
        self.widgetSceltaPastiPranzo.hide()
        self.widgetSceltaPastiCena.hide()
        self.comboboxPranzo.hide()
        self.comboboxCena.hide()

    
    def _resizeColumns(self):
        # colazione
        self.treewidgetDolceColazioneInCamera.header().resizeSection(0, 200)
        self.treewidgetSalatoColazioneInCamera.header().resizeSection(0, 200)
        self.treewidgetBevandeColazioneInCamera.header().resizeSection(0, 200)
        # pranzo
        self.treewidgetAntipastiPranzo.header().resizeSection(0, 200)
        self.treewidgetPrimoPranzo.header().resizeSection(0, 200)
        self.treewidgetSecondoContornoPranzo.header().resizeSection(0, 200)
        self.treewidgetDolciBevandePranzo.header().resizeSection(0, 200)
        # cena
        self.treewidgetAntipastiCena.header().resizeSection(0, 200)
        self.treewidgetPrimiCena.header().resizeSection(0, 200)
        self.treewidgetSecondiContorniCena.header().resizeSection(0, 200)
        self.treewidgetDolciBevandeCena.header().resizeSection(0, 200)


    def _fillTreeWidgetColazioneInCamera(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuColazione = GestoreFile.leggiDictPickle(Path(paths['menuColazione']))
        self.treewidgetDolceColazioneInCamera.clear()  #Queste tre righe che richiamano il metodo clear del treeWidget
        self.treewidgetSalatoColazioneInCamera.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetBevandeColazioneInCamera.clear()  #che se clicchiamo annulla il treeWidget torna come era prima
        if menuColazione != {}:
            dolci = menuColazione["dolce"] #ottenere sottodizionario
            for k, v in dolci.items():
                self.treewidgetDolceColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k,v], 0))
            salato = menuColazione["salato"] #ottenere sottodizionario
            for k, v in salato.items():
                self.treewidgetSalatoColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k,v], 0))
            bevande = menuColazione["bevande"]  #ottenere sottodizionario
            for k, v in bevande.items():
                self.treewidgetBevandeColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k, v], 0))
        else:
            i = 0
            while i < 3:
                self.treewidgetDolceColazioneInCamera.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetSalatoColazioneInCamera.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetBevandeColazioneInCamera.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                i += 1

    def _fillTreeWidgetPranzo(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuPranzo = GestoreFile.leggiDictPickle(Path(paths['menuPranzo']))
        self.treewidgetAntipastiPranzo.clear() #Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimoPranzo.clear() #ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondoContornoPranzo.clear() #che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandePranzo.clear() #uguale a come era prima
        if menuPranzo != {}:
            antipasti = menuPranzo["antipasto"] #ottenere sottodizionario
            for k,v in antipasti.items():
                self.treewidgetAntipastiPranzo.addTopLevelItem(QTreeWidgetItem([k,v], 0))
            primo = menuPranzo["primo"]  #ottenere sottodizionario
            for k, v in primo.items():
                self.treewidgetPrimoPranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            secondoContorno = menuPranzo["secondoContorno"]  #ottenere sottodizionario
            for k, v in secondoContorno.items():
                self.treewidgetSecondoContornoPranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            dolciBevande = menuPranzo["dolciBevande"]  #ottenere sottodizionario
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

    def _fillTreeWidgetCena(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuCena = GestoreFile.leggiDictPickle(Path(paths['menuCena']))
        self.treewidgetAntipastiCena.clear() #Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimiCena.clear() #ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondiContorniCena.clear() #che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandeCena.clear() #uguale a come era prima
        if menuCena != {}:
            antipasti = menuCena["antipasto"]  #ottenere sottodizionario
            for k, v in antipasti.items():
                self.treewidgetAntipastiCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            primo = menuCena["primo"]  #ottenere sottodizionario
            for k, v in primo.items():
                self.treewidgetPrimiCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            secondoContorno = menuCena["secondoContorno"] #ottenere sottodizionario
            for k, v in secondoContorno.items():
                self.treewidgetSecondiContorniCena.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            dolciBevande = menuCena["dolciBevande"] #ottenere sottodizionario
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
        self.btnInserisciSceltaPastiPranzo.clicked.connect(self._btnInserisciSceltaPastiPranzoClicked)
        self.btnInserisciSceltaPastiCena.clicked.connect(self._btnInserisciSceltaPastiCenaClicked)
        self.btnVisualizzaSceltaPastiPranzo.clicked.connect(self._btnVisualizzaSceltaPastiPranzoClicked)
        self.btnVisualizzaSceltaPastiCena.clicked.connect(self._btnVisualizzaSceltaPastiCenaClicked)
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnAnnulla.clicked.connect(self._btnAnnullaClicked)
        self.btnAvanti_2.clicked.connect(self._btnAvanti_2Clicked)
        self.btnAnnulla_2.clicked.connect(self._btnAnnulla_2Clicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self._btnTornarePaginaPrecedente_2Clicked)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self._btnTornarePaginaPrecedente_3Clicked)

    def _btnInserisciSceltaPastiPranzoClicked(self):
        self.btnInserisciSceltaPastiPranzo.hide()
        self.widgetSceltaPastiPranzo.show()
        self.labelIntroduzione_2.setText('Inserire il numero di camera e scegliere quali piatti desidera prenotare il cliente per il pranzo di domani.')
        self.comboboxPranzo.show()
        self.btnVisualizzaSceltaPastiPranzo.hide()
        self.treewidgetAntipastiPranzo.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetPrimoPranzo.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetSecondoContornoPranzo.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetDolciBevandePranzo.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    def _btnAvantiClicked(self):
        numeroCamera = int(self.comboboxPranzo.currentText())

        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            camere: dict[int, Camera] = GestoreFile.leggiDictPickle(Path(paths['camere']))
        except CorruptedFileError:
            self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.",
                                       QMessageBox.Icon.Warning, 'Errore')
            self.close()
            self.previous.close()
            raise

        camera = camere[numeroCamera]

        if not camera.isAssegnato():
            self._showMessage('Non esiste nessuna vacanza in corso nella camera selezionata.', QMessageBox.Icon.Warning)
            return

        dataDomani = date.today() + timedelta(days=1)
        if dataDomani in camera.getVacanzaAttuale().getSceltePastiPranzo(): # type: ignore
            self._showMessage(f"La prenotazione per la camera {numeroCamera} ?? stata gia effettuata per domani! ",
                              QMessageBox.Icon.Warning)
            return

        itemAntipasti = self.treewidgetAntipastiPranzo.selectedItems()
        itemPrimi = self.treewidgetPrimoPranzo.selectedItems()
        itemSecondiContorni = self.treewidgetSecondoContornoPranzo.selectedItems()
        itemDolciBevande = self.treewidgetDolciBevandePranzo.selectedItems()

        if itemAntipasti == [] and itemPrimi == [] and itemSecondiContorni == [] and itemDolciBevande == []:
            self._showMessage("Seleziona almeno un piatto per continuare", QMessageBox.Icon.Warning)
            return

        sceltePastiPranzo = {
            "antipasti": [item.text(0) for item in itemAntipasti],
            "primi" : [item.text(0) for item in itemPrimi],
            "secondiContorni": [item.text(0) for item in itemSecondiContorni],
            "dolciBevande": [item.text(0) for item in itemDolciBevande]
        }

        self.widgetConfermaSceltaPastiPranzo = ConfermaSceltaPastiPranzoUI(sceltePastiPranzo, numeroCamera, self)
        self.widgetConfermaSceltaPastiPranzo.show()
        self._btnAnnullaClicked()

    def _btnAnnullaClicked(self):
        self.btnInserisciSceltaPastiPranzo.show()
        self.labelIntroduzione_2.setText(" Benvenuto, di seguito il men?? dell'hotel per il pranzo:")
        self._hideWidget()
        self.btnVisualizzaSceltaPastiPranzo.show()
        self.treewidgetAntipastiPranzo.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetPrimoPranzo.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetSecondoContornoPranzo.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetDolciBevandePranzo.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.comboboxPranzo.setCurrentText("1")

        for item in self.treewidgetAntipastiPranzo.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetPrimoPranzo.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetSecondoContornoPranzo.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetDolciBevandePranzo.selectedItems():
            item.setSelected(False)

    def _btnVisualizzaSceltaPastiPranzoClicked(self):
        self.close()
        self.widgetVisualizzaSceltaPasti = VisualizzaSceltaPastiPranzoUI(self)
        self.widgetVisualizzaSceltaPasti.show()


    def _btnInserisciSceltaPastiCenaClicked(self):
        self.btnInserisciSceltaPastiCena.hide()
        self.widgetSceltaPastiCena.show()
        self.labelIntroduzione_3.setText('Inserire il numero di camera e scegliere quali piatti desidera prenotare il cliente per la cena di domani.')
        self.comboboxCena.show()
        self.btnVisualizzaSceltaPastiCena.hide()
        self.treewidgetAntipastiCena.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetPrimiCena.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetSecondiContorniCena.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetDolciBevandeCena.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    def _btnAvanti_2Clicked(self):
        numeroCamera = int(self.comboboxCena.currentText())

        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            camere: dict[int, Camera] = GestoreFile.leggiDictPickle(Path(paths['camere']))
        except CorruptedFileError:
            self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.",
                                       QMessageBox.Icon.Warning, 'Errore')
            self.close()
            self.previous.close()
            raise

        camera = camere[numeroCamera]

        if not camera.isAssegnato():
            self._showMessage('Non esiste nessuna vacanza in corso nella camera selezionata.', QMessageBox.Icon.Warning)
            return

        dataDomani = date.today() + timedelta(days=1)
        if dataDomani in camera.getVacanzaAttuale().getSceltePastiCena(): # type: ignore
            self._showMessage(f"La prenotazione per la camera {numeroCamera} ?? stata gia effettuata per domani! ",
                              QMessageBox.Icon.Warning)
            return

        itemAntipasti = self.treewidgetAntipastiCena.selectedItems()
        itemPrimi = self.treewidgetPrimiCena.selectedItems()
        itemSecondiContorni = self.treewidgetSecondiContorniCena.selectedItems()
        itemDolciBevande = self.treewidgetDolciBevandeCena.selectedItems()

        if itemAntipasti == [] and itemPrimi == [] and itemSecondiContorni == [] and itemDolciBevande == []:
            self._showMessage("Seleziona almeno un piatto per continuare", QMessageBox.Icon.Warning)
            return

        sceltePastiCena = {
            "antipasti": [item.text(0) for item in itemAntipasti],
            "primi": [item.text(0) for item in itemPrimi],
            "secondiContorni": [item.text(0) for item in itemSecondiContorni],
            "dolciBevande": [item.text(0) for item in itemDolciBevande]
        }

        self.widgetConfermaSceltaPastiCena = ConfermaSceltaPastiCenaUI(sceltePastiCena, numeroCamera, self)
        self.widgetConfermaSceltaPastiCena.show()
        self._btnAnnulla_2Clicked()

    def _btnAnnulla_2Clicked(self):
        self.btnInserisciSceltaPastiCena.show()
        self.labelIntroduzione_3.setText("Benvenuto, di seguito il men?? dell'hotel per la cena:")
        self._hideWidget()
        self.btnVisualizzaSceltaPastiCena.show()
        self.treewidgetAntipastiCena.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetPrimiCena.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetSecondiContorniCena.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetDolciBevandeCena.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        for item in self.treewidgetAntipastiCena.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetPrimiCena.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetSecondiContorniCena.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetDolciBevandeCena.selectedItems():
            item.setSelected(False)

    def _btnVisualizzaSceltaPastiCenaClicked(self):
        self.close()
        self.widgetVisualizzaSceltaPasti = VisualizzaSceltaPastiCenaUI(self)
        self.widgetVisualizzaSceltaPasti.show()

    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()
    def _btnTornarePaginaPrecedente_2Clicked(self):
        self.close()
        self.previous.show()
    def _btnTornarePaginaPrecedente_3Clicked(self):
        self.close()
        self.previous.show()

    def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()
