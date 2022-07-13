import sys
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Persona import Persona
from src.GUI.Dipendenti.HomeReceptionist.GestireClienti.RicercaClienteUI import RicercaClienteUI
from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza
from src.GestioneVacanza.Soggiorno import Soggiorno
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.customQtClasses import MyTreeWidgetItem
from src.Utilities.exceptions import CorruptedFileError


class RicercaPrenotazioneVacanzaUI(QTabWidget):
    
    prenotazioneSelezionata = QtCore.pyqtSignal(PrenotazioneVacanza)
    
    def __init__(self, previous: QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('RicercaPrenotazioneVacanza.ui', Path.cwd()), self)

        self.previous = previous
        self.groupbox.hide()
        self.treewidget.header().resizeSection(0, 70)
        self.treewidget.header().resizeSection(1, 150)
        self._connectButtons()


    def _connectButtons(self):
        self.btnRicerca.clicked.connect(self._btnRicercaClicked)
        self.btnOk.clicked.connect(self._btnOkClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)


    def _btnRicercaClicked(self):
        self.widgetRicercaCliente = RicercaClienteUI(self)
        self.widgetRicercaCliente.clienteTrovato.connect(self._onClienteTrovato)
        self.widgetRicercaCliente.show()


    def _onClienteTrovato(self, cliente : Persona):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            camere = GestoreFile.leggiDictPickle(Path(paths['camere']))
        except CorruptedFileError:
            self.previous._showMessage(f"{Path(paths['camere'])} has been corrupted. To fix the issue, delete it.", QMessageBox.Icon.Warning, 'Errore')
            self.close()
            self.previous.close()
            raise
        prenotazioni : list[PrenotazioneVacanza] = []
        for camera in camere.values():
            for prenotazione in camera.getPrenotazioni():
                if prenotazione.getNominativo().getId() == cliente.getId():
                    prenotazioni.append(prenotazione)
        
        if len(prenotazioni) == 0:
            self.previous._showMessage(f'Nessuna prenotazione associata a {cliente.getCognome()} {cliente.getNome()}', QMessageBox.Icon.Warning, 'Errore')
            return
        if len(prenotazioni) == 1:
            self._onPrenotazioneSelected(prenotazioni[0])
        else:
            self.treewidget.clear() # svuoto il tree widget da eventuali item precedenti
            for prenotazione in prenotazioni:
                tipoSoggiorno = str(prenotazione.getTipoSoggiorno())
                periodo = prenotazione.getPeriodo()
                self.treewidget.addTopLevelItem(MyTreeWidgetItem(self.treewidget,
                                                [str(prenotazione.getCamera().getNumero()), tipoSoggiorno, 
                                                periodo.getInizio().strftime('%d/%m/%Y'), periodo.getFine().strftime('%d/%m/%Y')],
                                                prenotazione))
            self.treewidget.itemDoubleClicked.connect(self._onPrenotazioneSelected) # col doppio cick viene selezionata la prenotazione
            if self.groupbox.isHidden():
                self.groupbox.show()


    def _btnOkClicked(self): # anche col bottone ok viene scelta la prenotazione selezionata dal tree widget
        if self.treewidget.currentItem() == None:
            self.previous._showMessage('Selezionare prima la prenotazione di interesse, o fare doppio click su di essa', QMessageBox.Icon.Warning, 'Errore')
            return
        self._onPrenotazioneSelected(self.treewidget.currentItem().connectedObject)


    def _onPrenotazioneSelected(self, prenotazione : PrenotazioneVacanza):
        self.prenotazioneSelezionata.emit(prenotazione) 
        self.close()
        self.previous.show()


    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = RicercaPrenotazioneVacanzaUI(QWidget())
    mainWidget.show()
    sys.exit(app.exec_())