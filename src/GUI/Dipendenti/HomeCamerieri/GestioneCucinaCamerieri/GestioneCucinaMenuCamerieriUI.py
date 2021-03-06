from datetime import date, timedelta

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.GUI.Dipendenti.HomeCamerieri.GestioneCucinaCamerieri.ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI import \
    ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI
from src.GUI.VisualizzaPrenotazioneColazioneUI import VisualizzaPrenotazioneColazioneUI
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.exceptions import CorruptedFileError


class GestioneCucinaMenuCamerieriUI(QTabWidget):
    
    def __init__(self, previous: QWidget):
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('GestioneCucinaMenu.ui', Path.cwd()), self)

        self.previous = previous

        self._connectButtons()
        self._hideWidget()
        self._resizeColumns()
        self._fillTreeWidgetColazioneInCamera()
        self._fillTreeWidgetPranzo()
        self._fillTreeWidgetCena()

        self.msg = QMessageBox()


    def _hideWidget(self):
        self.widgetColazioneInCamera.hide()
        self.widgetAnnullaAvanti.hide()
        self.comboboxColazioneInCamera.hide()
    

    def _resizeColumns(self):
        # colazione
        self.treewidgetDolceColazioneInCamera.header().resizeSection(0, 200)
        self.treewidgetSalatoColazioneInCamera.header().resizeSection(0, 200)
        self.treewidgetBevandeColazioneInCamera.header().resizeSection(0, 200)
        # pranzo
        self.treewidgetAntipastiPranzo.header().resizeSection(0, 200)
        self.treewidgetPrimiPranzo.header().resizeSection(0, 200)
        self.treewidgetSecondiContorniPranzo.header().resizeSection(0, 200)
        self.treewidgetDolciBevandePranzo.header().resizeSection(0, 200)
        # cena
        self.treewidgetAntipastiCena.header().resizeSection(0, 200)
        self.treewidgetPrimiCena.header().resizeSection(0, 200)
        self.treewidgetSecondiContorniCena.header().resizeSection(0, 200)
        self.treewidgetDolciBevandeCena.header().resizeSection(0, 200)


    def _fillTreeWidgetColazioneInCamera(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuColazione = GestoreFile.leggiDictPickle(Path(paths['menuColazione']))
        self.treewidgetDolceColazioneInCamera.clear()  # Queste tre righe che richiamano il metodo clear del treeWidget
        self.treewidgetSalatoColazioneInCamera.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetBevandeColazioneInCamera.clear()  # che se clicchiamo annulla il treeWidget torna come era prima
        if menuColazione != {}:
            dolci = menuColazione["dolce"] #ottenere sottodizionario
            for k,v in dolci.items():
                self.treewidgetDolceColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k,v], 0))
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


    def _fillTreeWidgetPranzo(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuPranzo = GestoreFile.leggiDictPickle(Path(paths['menuPranzo']))
        self.treewidgetAntipastiPranzo.clear()  # Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimiPranzo.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondiContorniPranzo.clear()  # che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandePranzo.clear()  # uguale a come era prima
        if menuPranzo != {}:
            antipasti = menuPranzo["antipasto"] #ottenere sottodizionario
            for k,v in antipasti.items():
                self.treewidgetAntipastiPranzo.addTopLevelItem(QTreeWidgetItem([k,v], 0))
            primo = menuPranzo["primo"]  # ottenere sottodizionario
            for k, v in primo.items():
                self.treewidgetPrimiPranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            secondoContorno = menuPranzo["secondoContorno"]  # ottenere sottodizionario
            for k, v in secondoContorno.items():
                self.treewidgetSecondiContorniPranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            dolciBevande = menuPranzo["dolciBevande"]  # ottenere sottodizionario
            for k, v in dolciBevande.items():
                self.treewidgetDolciBevandePranzo.addTopLevelItem(QTreeWidgetItem([k, v], 0))
        else:
            i = 0
            while i < 3:
                self.treewidgetAntipastiPranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetPrimiPranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetSecondiContorniPranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetDolciBevandePranzo.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                i += 1

   
    def _fillTreeWidgetCena(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuCena = GestoreFile.leggiDictPickle(Path(paths['menuCena']))
        self.treewidgetAntipastiCena.clear()  # Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimiCena.clear()  # ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondiContorniCena.clear()  # che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandeCena.clear()  # uguale a come era prima
        if menuCena != {}:
            antipasti = menuCena["antipasto"] #ottenere sottodizionario
            for k,v in antipasti.items():
                self.treewidgetAntipastiCena.addTopLevelItem(QTreeWidgetItem([k,v], 0))
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
        self.btnPrenotaColazioneInCameraGiornoSuccessivo.clicked.connect(self._btnPrenotaColazioneInCameraGiornoSuccessivoClicked)
        self.btnVisualizzaPrenotazioni.clicked.connect(self._btnVisualizzaPrenotazioniClicked)
        self.btnAvanti.clicked.connect(self._btnAvantiClicked)
        self.btnAnnulla.clicked.connect(self._btnAnnullaClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self._btnTornarePaginaPrecedente_2Clicked)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self._btnTornarePaginaPrecedente_3Clicked)


    def _btnPrenotaColazioneInCameraGiornoSuccessivoClicked(self):
        self.btnPrenotaColazioneInCameraGiornoSuccessivo.hide()
        self.widgetColazioneInCamera.show()
        self.widgetAnnullaAvanti.show()
        self.labelIntroduzionePagina.setText("Inserire la scelta del menu del cliente per la colazione in camera e inserire la camera del cliente.")
        self.comboboxColazioneInCamera.show()
        self.treewidgetDolceColazioneInCamera.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetSalatoColazioneInCamera.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treewidgetBevandeColazioneInCamera.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

   
    def _btnAvantiClicked(self):

        numeroCamera = int(self.comboboxColazioneInCamera.currentText())

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
        if dataDomani in camera.getVacanzaAttuale().getColazioniInCamera(): # type: ignore
            self._showMessage(f"La prenotazione per la camera {numeroCamera} ?? stata gia effettuata per domani! ",
                              QMessageBox.Icon.Warning)
            return

        itemDolci = self.treewidgetDolceColazioneInCamera.selectedItems()
        itemSalati = self.treewidgetSalatoColazioneInCamera.selectedItems()
        itemBevande = self.treewidgetBevandeColazioneInCamera.selectedItems()

        if itemDolci == [] and itemSalati == [] and itemBevande == []:
            self._showMessage("Seleziona almeno un piatto per continuare", QMessageBox.Icon.Warning)
            return

        sceltePasti = {
            "dolce": [item.text(0) for item in itemDolci],
            "salato": [item.text(0) for item in itemSalati],
            "bevande": [item.text(0) for item in itemBevande]
        }

        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo = ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI(sceltePasti, numeroCamera, self)
        self.widgetConfermaPrenotazioneColazioneInCameraGiornoSuccessivo.show()
        self._btnAnnullaClicked()

   
    def _btnAnnullaClicked(self):
        self.btnPrenotaColazioneInCameraGiornoSuccessivo.show()
        self.labelIntroduzionePagina.setText("Benvenuto, di seguito il men?? dell'hotel per la colazione in camera:")
        self._hideWidget()
        self.treewidgetDolceColazioneInCamera.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetSalatoColazioneInCamera.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.treewidgetBevandeColazioneInCamera.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.comboboxColazioneInCamera.setCurrentText("1")

        for item in self.treewidgetDolceColazioneInCamera.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetSalatoColazioneInCamera.selectedItems():
            item.setSelected(False)
        for item in self.treewidgetBevandeColazioneInCamera.selectedItems():
            item.setSelected(False)

   
    def _btnVisualizzaPrenotazioniClicked(self):
        self.close()
        self.widgetVisualizzaPrenotazioneColazione = VisualizzaPrenotazioneColazioneUI(self)
        self.widgetVisualizzaPrenotazioneColazione.show()

    
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
