import sys
from datetime import date, timedelta

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile
from src.Utilities.exceptions import CorruptedFileError


class ConfermaSceltaPastiPranzoUI(QTabWidget):
    def __init__(self, sceltePasti: dict, numeroCamera: int, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ConfermaSceltaPastiPranzo.ui', Path.cwd()), self)
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

        for nomeAntipasto in sceltePasti["antipasti"]:
            self.formLayoutAntipasti.addRow(nomeAntipasto, self._createComboBox(numeroClienti))
        for nomePrimo in sceltePasti["primi"]:
            self.formLayoutPrimi.addRow(nomePrimo, self._createComboBox(numeroClienti))
        for nomeSecondoContorno in sceltePasti["secondiContorni"]:
            self.formLayoutSecondiContorni.addRow(nomeSecondoContorno, self._createComboBox(numeroClienti))
        for nomeDolciBevande in sceltePasti["dolciBevande"]:
            self.formLayoutDolciBevande.addRow(nomeDolciBevande, self._createComboBox(numeroClienti))

    def _connectButtons(self):
        self.btnConfermaPrenotazione.clicked.connect(self._btnConfermaPrenotazioneClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnConfermaPrenotazioneClicked(self):
        i = 0
        antipasti = {}
        while i < self.formLayoutAntipasti.rowCount():
            nome = self.formLayoutAntipasti.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutAntipasti.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            antipasti[nome] = quantita
            i += 1

        i = 0
        primi = {}
        while i < self.formLayoutPrimi.rowCount():
            nome = self.formLayoutPrimi.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutPrimi.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            primi[nome] = quantita
            i += 1

        i = 0
        secondiContorni = {}
        while i < self.formLayoutSecondiContorni.rowCount():
            nome = self.formLayoutSecondiContorni.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutSecondiContorni.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            secondiContorni[nome] = quantita
            i += 1

        i = 0
        dolciBevande= {}
        while i < self.formLayoutDolciBevande.rowCount():
            nome = self.formLayoutDolciBevande.itemAt(i, QFormLayout.ItemRole.LabelRole).widget().text()
            quantita = self.formLayoutDolciBevande.itemAt(i, QFormLayout.ItemRole.FieldRole).widget().currentText()
            dolciBevande[nome] = quantita
            i += 1

        sceltaPastiPranzo = {"antipasti": antipasti, "primo": primi, "secondiContorni": secondiContorni, "dolciBevande": dolciBevande}
        camera = camere[self.numeroCamera]
        sceltePastiPranzoVacanza = camera.getVacanzaAttuale().getSceltePastiPranzo()
        dataDomani = date.today() + timedelta(days=1)
        sceltePastiPranzoVacanza[dataDomani] = sceltaPastiPranzo
        camera.getVacanzaAttuale().setSceltePastiPranzo(sceltePastiPranzoVacanza)
        GestoreFile.salvaPickle(camere, Path(paths['camere']))
        self.close()
        self._showMessage(
            f"La scelta dei pasti per il pranzo di domani è stata inserita correttamente per la camera {self.numeroCamera}",
            QMessageBox.Icon.Information)

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
    mainWidget = ConfermaSceltaPastiPranzoUI()
    mainWidget.show()
    sys.exit(app.exec_())