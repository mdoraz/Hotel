import sys
from datetime import date
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src.GestioneVacanza.PrenotazioneVacanza import PrenotazioneVacanza

from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.PeriodoConData import PeriodoConData
from src.Utilities.exceptions import CorruptedFileError


class SelezionaCameraUI(QTabWidget):
    
    cameraSelezionata = QtCore.pyqtSignal(Camera, PeriodoConData)
    
    def __init__(self, previous: QWidget, prenotazioneDaModificare : PrenotazioneVacanza = None): # type: ignore
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('SelezionaCamera.ui', Path.cwd()), self)
        
        self.previous = previous
        self.prenotazioneDaModificare = prenotazioneDaModificare

        self.groupboxCamere.hide() # inizialmente la lista di camere
        self.btnConferma.hide() # e il bottone di conferma non sono visibili
        
        self._setupDateEdits() # imposta i limiti di scelta delle due date edit e le collega tra loro
        self._connectButtons()

        self.msg = QMessageBox() 


    def _setupDateEdits(self):
        self.dateeditDa.setMinimumDate(date.today())
        self.dateeditA.setMinimumDate(date.today())
        self.dateeditDa.dateChanged.connect(self.dateeditA.setMinimumDate) # il limite inferiore della data di partenza è sempre aggiornato alla data di arrivo


    def _connectButtons(self):
        self.btnRicercaCamere.clicked.connect(self._btnRicercaCamereClicked)
        self.btnConferma.clicked.connect(self._btnConfermaClicked)
        self.btnIndietro.clicked.connect(self.close)


    def _btnRicercaCamereClicked(self):    
        self.periodo = PeriodoConData(self.dateeditDa.date().toPyDate(), self.dateeditA.date().toPyDate()) # periodo selezionato
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try :
            self.camere : dict[int, Camera] = GestoreFile.leggiDictPickle(Path(paths['camere']))
        except CorruptedFileError:
            self._showMessage(f"{Path('paths.json').name} has been corrupted. To fix the issue, delete it.",
                              QMessageBox.Icon.Warning, 'Errore')
            return

        # se la ricerca della camera sta avvenendo per modificare una prenotazione, allora dalla camera associata a quella prenotazione viene
        # rimossa la prenotazione in questione, in modo che la camera risulti disponibile nel periodo della prenotazione che si sta modificando
        if self.prenotazioneDaModificare != None:
            for prenotazione in self.camere[self.prenotazioneDaModificare.getCamera().getNumero()].getPrenotazioni():
                if prenotazione == self.prenotazioneDaModificare:
                    self.camere[self.prenotazioneDaModificare.getCamera().getNumero()].eliminaPrenotazione(prenotazione)
        
        self.treeWidgetCamere.clear() # svuoto il tree widget
        # aggiungo al tree widget le camere disponibili nel periodo inserito
        for camera in self.camere.values():
            if camera.isDisponibile(self.periodo):
                self.treeWidgetCamere.addTopLevelItem(QTreeWidgetItem([str(camera.getNumero()), str(camera.getNumeroPersone())], 0))

        if self.groupboxCamere.isHidden(): # se nascosti, mostro la lista di camere e il bottone di conferma
            self.groupboxCamere.show()
            self.btnConferma.show()

        if self.treeWidgetCamere.topLevelItemCount() == 0:
            self._showMessage('Nessuna camera disponibile nel periodo di ricerca, provare con un altro periodo.', QMessageBox.Icon.Warning, 'Errore')
    

    def _btnConfermaClicked(self):
        if self.treeWidgetCamere.currentItem() == None:
            self._showMessage('Non è stata selezionata nessuna camera. Per procedere selezionarne una.', QMessageBox.Icon.Warning, 'Errore')
            return
        numeroCamera = int(self.treeWidgetCamere.currentItem().text(0))
        self.cameraSelezionata.emit(self.camere[numeroCamera], self.periodo) # lancio il segnale per il widget principale della classe HomeGestioneVacanzeUI
        self.close()


    def _showMessage(self, text : str, icon : QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle : str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = SelezionaCameraUI(QWidget())
    mainWidget.show()
    sys.exit(app.exec_())