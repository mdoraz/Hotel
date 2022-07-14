import sys
from datetime import date, timedelta

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.exceptions import CorruptedFileError


class ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI(QTabWidget):
    def __init__(self, sceltePasti: dict, numeroCamera: int, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ConfermaPrenotazioneColazioneInCameraGiornoSuccessivo.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous
        self.numeroCamera = numeroCamera
        self._addRowsComboBox(sceltePasti)
        self.msg = QMessageBox()

    def _createComboBox(self, numeroClienti: int):#Funzione che crea una combo box da affiancare al nome del piatto per sceglierne la quantità
        comboBox = QComboBox()
        i = 1
        while i <= numeroClienti:
            comboBox.addItem(str(i))
            i += 1
        return comboBox

    def _addRowsComboBox(self, sceltePasti: dict): # aggiunge a runtime i piatti selezionati e le combo box per scegliere le quantita di tale piatto
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

        camera = camere[self.numeroCamera]
        numeroClienti = len(camera.getVacanzaAttuale().getClienti())

        for nomeDolce in sceltePasti["dolce"]:
            self.formLayoutDolce.addRow(nomeDolce,self._createComboBox(numeroClienti))
        for nomeSalato in sceltePasti["salato"]:
            self.formLayoutSalato.addRow(nomeSalato, self._createComboBox(numeroClienti))
        for nomeBevande in sceltePasti["bevande"]:
            self.formLayoutBevande.addRow(nomeBevande, self._createComboBox(numeroClienti))


    def _connectButtons(self):
        self.btnConfermaPrenotazione.clicked.connect(self._btnConfermaPrenotazioneClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnConfermaPrenotazioneClicked(self):
        camera = camere[self.numeroCamera]
        prenotazioneColazioneVacanza = camera.getVacanzaAttuale().getColazioniInCamera()
        dataDomani = date.today() + timedelta(days=1)

        i = 0
        dolce = {}
        while i < self.formLayoutDolce.rowCount():
            nome = self.formLayoutDolce.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutDolce.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            dolce[nome] = quantita
            i += 1

        i = 0
        salato = {}
        while i < self.formLayoutSalato.rowCount():
            nome = self.formLayoutSalato.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutSalato.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            salato[nome] = quantita
            i += 1

        i = 0
        bevande = {}
        while i < self.formLayoutBevande.rowCount():
            nome = self.formLayoutBevande.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutBevande.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            bevande[nome] = quantita
            i += 1

        prenotazioneColazione = {"dolce": dolce, "salato": salato, "bevande": bevande}
        prenotazioneColazioneVacanza[dataDomani] = prenotazioneColazione
        camera.getVacanzaAttuale().setColazioniInCamera(prenotazioneColazioneVacanza)
        GestoreFile.salvaPickle(camere, Path(paths['camere']))
        self.close()
        self._showMessage(f"La prenotazione della colazione di domani è stata effettuatata correttamente per la camera {self.numeroCamera}", QMessageBox.Icon.Information)

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

    def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ConfermaPrenotazioneColazioneInCameraGiornoSuccessivoUI()
    mainWidget.show()
    sys.exit(app.exec_())



