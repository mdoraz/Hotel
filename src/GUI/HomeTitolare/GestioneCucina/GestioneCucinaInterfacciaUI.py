from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Gestori.GestoreFile import GestoreFile


class GestioneCucinaInterfacciaUI(QTabWidget):
    
    def __init__(self, previous: QWidget):
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('GestioneCucinaInterfaccia.ui', Path.cwd()), self)

        self.previous = previous
        self._connectButtons()

        self.widgetModificaMenu.hide()
        self.widgetModificaMenu_2.hide()
        self.widgetModificaMenu_3.hide()

        self._resizeColumns()
        self._fillTreeWidgetColazioneInCamera()
        self._fillTreeWidgetPranzo()
        self._fillTreeWidgetCena()

    
    def _resizeColumns(self):
        # colazione
        self.treewidgetDolceColazioneInCamera.header().resizeSection(0, 200)
        self.treewidgetSalatoColazioneInCamera.header().resizeSection(0, 200)
        self.treewidgetBevandeColazioneInCamera.header().resizeSection(0, 200)
        # primi
        self.treewidgetAntipastiPranzo.header().resizeSection(0, 200)
        self.treewidgetPrimoPranzo.header().resizeSection(0, 200)
        self.treewidgetSecondoContornoPranzo.header().resizeSection(0, 200)
        self.treewidgetDolciBevandePranzo.header().resizeSection(0, 200)
        # secondi
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
            for k, v in dolci.items():
                self.treewidgetDolceColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k, v], 0))
            salato = menuColazione["salato"] #ottenere sottodizionario
            for k, v in salato.items():
                self.treewidgetSalatoColazioneInCamera.addTopLevelItem(QTreeWidgetItem([k, v], 0))
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
        self.treewidgetAntipastiPranzo.clear()#Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimoPranzo.clear()#ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondoContornoPranzo.clear()#che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandePranzo.clear()# uguale a come era prima
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


    def _fillTreeWidgetCena(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        menuCena = GestoreFile.leggiDictPickle(Path(paths['menuCena']))
        self.treewidgetAntipastiCena.clear() #Queste quattro righe che richiamano il metodo clear del treeWidget
        self.treewidgetPrimiCena.clear() #ci permettono di partire sempre con il treeWidget vuoto in modo tale
        self.treewidgetSecondiContorniCena.clear() #che se clicchiamo annulla il treeWidget torna
        self.treewidgetDolciBevandeCena.clear()# uguale a come era prima
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
            while i < 3 :
                self.treewidgetAntipastiCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetPrimiCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetSecondiContorniCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                self.treewidgetDolciBevandeCena.addTopLevelItem(QTreeWidgetItem([f"Nome{i+1}", "Ingredienti"], 0))
                i += 1

    def _connectButtons(self):
        self.btnModificaMenuColazioneInCamera.clicked.connect(self._btnModificaMenuColazioneInCameraClicked)
        self.btnModificaMenuPranzo.clicked.connect(self._btnModificaMenuPranzoClicked)
        self.btnModificaMenuCena.clicked.connect(self._btnModificaMenuCenaClicked)
        self.btnConfermaModifiche.clicked.connect(self._btnConfermaModificheClicked)
        self.btnConfermaModifiche_2.clicked.connect(self._btnConfermaModifiche_2Clicked)
        self.btnConfermaModifiche_3.clicked.connect(self._btnConfermaModifiche_3Clicked)
        self.btnAnnullaModifiche.clicked.connect(self._btnAnnullaModificheClicked)
        self.btnAnnullaModifiche_2.clicked.connect(self._btnAnnullaModifiche_2Clicked)
        self.btnAnnullaModifiche_3.clicked.connect(self._btnAnnullaModifiche_3Clicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)
        self.btnTornarePaginaPrecedente_2.clicked.connect(self._btnTornarePaginaPrecedente_2Clicked)
        self.btnTornarePaginaPrecedente_3.clicked.connect(self._btnTornarePaginaPrecedente_3Clicked)


    def _btnModificaMenuColazioneInCameraClicked(self):
        self.btnModificaMenuColazioneInCamera.hide()
        self.widgetModificaMenu.show()
        self.labelIntroduzione.setText("Quali piatti desidera modificare?")
        i = 0
        self.proprietaItemDolci = []
        while i < self.treewidgetDolceColazioneInCamera.topLevelItemCount():
            item = self.treewidgetDolceColazioneInCamera.topLevelItem(i)
            i += 1
            self.proprietaItemDolci.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i2 = 0
        self.proprietaItemSalato = []
        while i2 < self.treewidgetSalatoColazioneInCamera.topLevelItemCount():
            item = self.treewidgetSalatoColazioneInCamera.topLevelItem(i2)
            i2 += 1
            self.proprietaItemSalato.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i3 = 0
        self.proprietaItemBevande = []
        while i3 < self.treewidgetBevandeColazioneInCamera.topLevelItemCount():
            item = self.treewidgetBevandeColazioneInCamera.topLevelItem(i3)
            i3 += 1
            self.proprietaItemBevande.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())


    def _btnConfermaModificheClicked(self):
        i = 0
        dolce = {}
        while i < self.treewidgetDolceColazioneInCamera.topLevelItemCount():
            item = self.treewidgetDolceColazioneInCamera.topLevelItem(i)
            nome = item.text(0)
            ingredienti = item.text(1)
            dolce[nome] = ingredienti
            i += 1
        i2 = 0
        salato = {}
        while i2 < self.treewidgetSalatoColazioneInCamera.topLevelItemCount():
            item = self.treewidgetSalatoColazioneInCamera.topLevelItem(i2)
            nome = item.text(0)
            ingredienti = item.text(1)
            salato[nome] = ingredienti
            i2 += 1

        i3 = 0
        bevande = {}
        while i3 < self.treewidgetBevandeColazioneInCamera.topLevelItemCount():
            item = self.treewidgetBevandeColazioneInCamera.topLevelItem(i3)
            nome = item.text(0)
            ingredienti = item.text(1)
            bevande[nome] = ingredienti
            i3 += 1

        menuColazioneInCamera = {"dolce": dolce, "salato": salato, "bevande": bevande}
        paths = GestoreFile.leggiJson(Path('paths.json'))
        GestoreFile.salvaPickle(menuColazioneInCamera, Path(paths['menuColazione']))
        self.btnModificaMenuColazioneInCamera.show()
        self.widgetModificaMenu.hide()


    def _btnAnnullaModificheClicked(self):
        self.labelIntroduzione.setText("Benvenuto, di seguito il menù dell'hotel per la colazione in camera:")
        i = 0
        while i < self.treewidgetDolceColazioneInCamera.topLevelItemCount():
            item = self.treewidgetDolceColazioneInCamera.topLevelItem(i)
            item.setFlags(self.proprietaItemDolci[i])
            i += 1

        i2 = 0
        while i2 < self.treewidgetSalatoColazioneInCamera.topLevelItemCount():
            item = self.treewidgetSalatoColazioneInCamera.topLevelItem(i2)
            item.setFlags(self.proprietaItemSalato[i2])
            i2 += 1

        i3 = 0
        while i3 < self.treewidgetBevandeColazioneInCamera.topLevelItemCount():
            item = self.treewidgetBevandeColazioneInCamera.topLevelItem(i3)
            item.setFlags(self.proprietaItemBevande[i3])
            i3 += 1

        self._fillTreeWidgetColazioneInCamera()
        self.btnModificaMenuColazioneInCamera.show()
        self.widgetModificaMenu.hide()


    def _btnModificaMenuPranzoClicked(self):
        self.btnModificaMenuPranzo.hide()
        self.widgetModificaMenu_2.show()
        self.labelIntroduzione_2.setText("Quali piatti desidera modificare?")
        i = 0
        self.proprietaItemAntipasti = []
        while i < self.treewidgetAntipastiPranzo.topLevelItemCount():
            item = self.treewidgetAntipastiPranzo.topLevelItem(i)
            i += 1
            self.proprietaItemAntipasti.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i2 = 0
        self.proprietaItemPrimo = []
        while i2 < self.treewidgetPrimoPranzo.topLevelItemCount():
            item = self.treewidgetPrimoPranzo.topLevelItem(i2)
            i2 += 1
            self.proprietaItemPrimo.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i3 = 0
        self.proprietaItemSecondoContorno = []
        while i3 < self.treewidgetSecondoContornoPranzo.topLevelItemCount():
            item = self.treewidgetSecondoContornoPranzo.topLevelItem(i3)
            i3 += 1
            self.proprietaItemSecondoContorno.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i4 = 0
        self.proprietaItemDolciBevande = []
        while i4 < self.treewidgetDolciBevandePranzo.topLevelItemCount():
            item = self.treewidgetDolciBevandePranzo.topLevelItem(i4)
            i4 += 1
            self.proprietaItemDolciBevande.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())
    

    def _btnConfermaModifiche_2Clicked(self):
        i = 0
        antipasto = {}
        while i < self.treewidgetAntipastiPranzo.topLevelItemCount():
            item = self.treewidgetAntipastiPranzo.topLevelItem(i)
            nome = item.text(0)
            ingredienti = item.text(1)
            antipasto[nome] = ingredienti
            i += 1

        i2 = 0
        primo = {}
        while i2 < self.treewidgetPrimoPranzo.topLevelItemCount():
            item = self.treewidgetPrimoPranzo.topLevelItem(i2)
            nome = item.text(0)
            ingredienti = item.text(1)
            primo[nome] = ingredienti
            i2 += 1

        i3 = 0
        secondoContorno = {}
        while i3 < self.treewidgetSecondoContornoPranzo.topLevelItemCount():
            item = self.treewidgetSecondoContornoPranzo.topLevelItem(i3)
            nome = item.text(0)
            ingredienti = item.text(1)
            secondoContorno[nome] = ingredienti
            i3 += 1

        i4 = 0
        dolciBevande = {}
        while i4 < self.treewidgetDolciBevandePranzo.topLevelItemCount():
            item = self.treewidgetDolciBevandePranzo.topLevelItem(i4)
            nome = item.text(0)
            ingredienti = item.text(1)
            dolciBevande[nome] = ingredienti
            i4 += 1

        menuPranzo = {"antipasto": antipasto, "primo": primo, "secondoContorno": secondoContorno, "dolciBevande": dolciBevande}
        paths = GestoreFile.leggiJson(Path('paths.json'))
        GestoreFile.salvaPickle(menuPranzo, Path(paths['menuPranzo']))
        self.btnModificaMenuPranzo.show()
        self.widgetModificaMenu_2.hide()
    

    def _btnAnnullaModifiche_2Clicked(self):
        self.labelIntroduzione_2.setText("Benvenuto, di seguito il menù dell'hotel per il pranzo:")
        i = 0
        while i < self.treewidgetAntipastiPranzo.topLevelItemCount():
            item = self.treewidgetAntipastiPranzo.topLevelItem(i)
            item.setFlags(self.proprietaItemAntipasti[i])
            i += 1

        i2 = 0
        while i2 < self.treewidgetPrimoPranzo.topLevelItemCount():
            item = self.treewidgetPrimoPranzo.topLevelItem(i2)
            item.setFlags(self.proprietaItemPrimo[i2])
            i2 += 1

        i3 = 0
        while i3 < self.treewidgetSecondoContornoPranzo.topLevelItemCount():
            item = self.treewidgetSecondoContornoPranzo.topLevelItem(i3)
            item.setFlags(self.proprietaItemSecondoContorno[i3])
            i3 += 1

        i4 = 0
        while i4 < self.treewidgetDolciBevandePranzo.topLevelItemCount():
            item = self.treewidgetDolciBevandePranzo.topLevelItem(i4)
            item.setFlags(self.proprietaItemDolciBevande[i4])
            i4 += 1

        self._fillTreeWidgetPranzo()
        self.btnModificaMenuPranzo.show()
        self.widgetModificaMenu_2.hide()


    def _btnModificaMenuCenaClicked(self):
        self.btnModificaMenuCena.hide()
        self.widgetModificaMenu_3.show()
        self.labelIntroduzione_3.setText("Quali piatti desidera modificare?")
        i = 0
        self.proprietaItemAntipasti = []
        while i < self.treewidgetAntipastiCena.topLevelItemCount():
            item = self.treewidgetAntipastiCena.topLevelItem(i)
            i += 1
            self.proprietaItemAntipasti.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i2 = 0
        self.proprietaItemPrimo = []
        while i2 < self.treewidgetPrimiCena.topLevelItemCount():
            item = self.treewidgetPrimiCena.topLevelItem(i2)
            i2 += 1
            self.proprietaItemPrimo.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i3 = 0
        self.proprietaItemSecondoContorno = []
        while i3 < self.treewidgetSecondiContorniCena.topLevelItemCount():
            item = self.treewidgetSecondiContorniCena.topLevelItem(i3)
            i3 += 1
            self.proprietaItemSecondoContorno.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())

        i4 = 0
        self.proprietaItemDolciBevande = []
        while i4 < self.treewidgetDolciBevandeCena.topLevelItemCount():
            item = self.treewidgetDolciBevandeCena.topLevelItem(i4)
            i4 += 1
            self.proprietaItemDolciBevande.append(item.flags())
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable | item.flags())


    def _btnConfermaModifiche_3Clicked(self):
        i = 0
        antipasto = {}
        while i < self.treewidgetAntipastiCena.topLevelItemCount():
            item = self.treewidgetAntipastiCena.topLevelItem(i)
            nome = item.text(0)
            ingredienti = item.text(1)
            antipasto[nome] = ingredienti
            i += 1

        i2 = 0
        primo = {}
        while i2 < self.treewidgetPrimiCena.topLevelItemCount():
            item = self.treewidgetPrimiCena.topLevelItem(i2)
            nome = item.text(0)
            ingredienti = item.text(1)
            primo[nome] = ingredienti
            i2 += 1

        i3 = 0
        secondoContorno = {}
        while i3 < self.treewidgetSecondiContorniCena.topLevelItemCount():
            item = self.treewidgetSecondiContorniCena.topLevelItem(i3)
            nome = item.text(0)
            ingredienti = item.text(1)
            secondoContorno[nome] = ingredienti
            i3 += 1

        i4 = 0
        dolciBevande = {}
        while i4 < self.treewidgetDolciBevandeCena.topLevelItemCount():
            item = self.treewidgetDolciBevandeCena.topLevelItem(i4)
            nome = item.text(0)
            ingredienti = item.text(1)
            dolciBevande[nome] = ingredienti
            i4 += 1

        menuCena = {"antipasto": antipasto, "primo": primo, "secondoContorno": secondoContorno, "dolciBevande": dolciBevande}
        paths = GestoreFile.leggiJson(Path('paths.json'))
        GestoreFile.salvaPickle(menuCena, Path(paths['menuCena']))
        self.btnModificaMenuCena.show()
        self.widgetModificaMenu_3.hide()
    

    def _btnAnnullaModifiche_3Clicked(self):
        self.labelIntroduzione_3.setText("Benvenuto, di seguito il menù dell'hotel per la cena:")
        i = 0
        while i < self.treewidgetAntipastiCena.topLevelItemCount():
            item = self.treewidgetAntipastiCena.topLevelItem(i)
            item.setFlags(self.proprietaItemAntipasti[i])
            i += 1

        i2 = 0
        while i2 < self.treewidgetPrimiCena.topLevelItemCount():
            item = self.treewidgetPrimiCena.topLevelItem(i2)
            item.setFlags(self.proprietaItemPrimo[i2])
            i2 += 1

        i3 = 0
        while i3 < self.treewidgetSecondiContorniCena.topLevelItemCount():
            item = self.treewidgetSecondiContorniCena.topLevelItem(i3)
            item.setFlags(self.proprietaItemSecondoContorno[i3])
            i3 += 1

        i4 = 0
        while i4 < self.treewidgetDolciBevandeCena.topLevelItemCount():
            item = self.treewidgetDolciBevandeCena.topLevelItem(i4)
            item.setFlags(self.proprietaItemDolciBevande[i4])
            i4 += 1

        self._fillTreeWidgetCena()
        self.btnModificaMenuCena.show()
        self.widgetModificaMenu_3.hide()


    def _btnTornarePaginaPrecedenteClicked(self):
        self.close()
        self.previous.show()


    def _btnTornarePaginaPrecedente_2Clicked(self):
        self.close()
        self.previous.show()


    def _btnTornarePaginaPrecedente_3Clicked(self):
        self.close()
        self.previous.show()
