import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.exceptions import CorruptedFileError

class ConfermaSceltaPastiCenaUI(QTabWidget):
    def __init__(self, sceltePasti: dict, numeroCamera: int, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('ConfermaSceltaPastiCena.ui', Path.cwd()), self)
        self.setMinimumSize(600, 600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

        self._addRowsComboBox(sceltePasti, numeroCamera)

    def _addRowsComboBox(self, sceltaPasti: dict, numeroCamera: int): # aggiunge a runtime i piatti selezionati e le combo box per scegliere le quantita di tale piatto
        comboBox = QComboBox()

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
        numeroClienti = len(camera.getVacanzaAttuale().getClienti())

        for i in range(1, numeroClienti + 1):
            comboBox.addItem()
        for nomeAntipasto in sceltaPasti["antipasti"]:
            self.formLayoutAntipasti.addRow(nomeAntipasto, comboBox)
        for nomePrimo in sceltaPasti["primi"]:
            self.formLayoutPrimi.addRow(nomePrimo, comboBox)
        for nomeSecondoContorno in sceltaPasti["secondiContorni"]:
            self.formLayoutSecondiContorni.addRow(nomeSecondoContorno, comboBox)
        for nomeDolciBevande in sceltaPasti["dolciBevande"]:
            self.formLayoutDolciBevande.addRow(nomeDolciBevande, comboBox)

    def _connectButtons(self):
        self.btnConfermaPrenotazione.clicked.connect(self._btnConfermaPrenotazioneClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnConfermaPrenotazioneClicked(self):
        pass

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = ConfermaSceltaPastiCenaUI()
    mainWidget.show()
    sys.exit(app.exec_())