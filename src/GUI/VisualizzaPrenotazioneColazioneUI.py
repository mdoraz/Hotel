import sys
from datetime import date, timedelta

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.Gestori.GestoreFile import GestoreFile
from src.Servizi.Camera import Camera
from src.Utilities.exceptions import CorruptedFileError


class VisualizzaPrenotazioneColazioneUI(QWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('VisualizzaPrenotazioneColazione.ui', Path.cwd()), self)
        self._connectButtons()
        self.previous = previous
        self.msg = QMessageBox

        self.dateEditColazione.setMinimumDate(date.today())
        self.dateEditColazione.setMaximumDate(date.today() + timedelta(days=1))

    def _connectButtons(self):
        self.btnCerca.clicked.connect(self._btnCercaClicked)
        self.btnEliminaPrenotazione.clicked.connect(self._btnEliminaPrenotazioneClicked)
        self.btnTornarePaginaPrecedente.clicked.connect(self._btnTornarePaginaPrecedenteClicked)

    def _btnCercaClicked(self):
        camere = self._readCamere()
        numeroCamera = int(self.comboboxColazioneInCamera.currentText())
        camera = camere[numeroCamera]
        if not camera.isAssegnato():
            self.previous._showMessage(
                f"La camera {self.comboboxColazioneInCamera.currentText()} non è attualmente assegnata.",
                QMessageBox.Icon.Warning)
            return
        try:
            global colazioneInCamera
            colazioneInCamera = camera.getVacanzaAttuale().getColazioniInCamera()[self.dateEditColazione.date().toPyDate()]
        except:
            self.previous._showMessage(f"Per la camera {self.comboboxColazioneInCamera.currentText()} non esiste alcuna prenotazione nella data inserita", QMessageBox.Icon.Warning)
            return

        dolci = colazioneInCamera['dolce']
        salato = colazioneInCamera['salato']
        bevande = colazioneInCamera['bevande']

        self.treewidgetDolce.clear()#permette di svuotare il treewidget di interesse
        for k, v in dolci.items():
            self.treewidgetDolce.addTopLevelItem(QTreeWidgetItem([k, v]))
        self.treewidgetSalato.clear()
        for k, v in salato.items():
            self.treewidgetSalato.addTopLevelItem(QTreeWidgetItem([k, v]))
        self.treewidgetBevande.clear()
        for k, v in bevande.items():
            self.treewidgetBevande.addTopLevelItem(QTreeWidgetItem([k, v]))

    def _btnEliminaPrenotazioneClicked(self):
        data = self.dateEditColazione.date().toPyDate()
        numeroCamera = int(self.comboboxColazioneInCamera.currentText())
        del camere[numeroCamera].getVacanzaAttuale().getColazioniInCamera()[data]
        camere[numeroCamera].getVacanzaAttuale().setColazioniInCamera(colazioneInCamera)
        GestoreFile.salvaPickle(camere, Path(paths['camere']))
        self.previous._showMessage(
            f"La prenotazione della camera {self.comboboxColazioneInCamera.currentText()} per la data {data.strftime('%d/%m/%Y')} è stata eliminata correttamente", QMessageBox.Icon.Information)
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
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = VisualizzaPrenotazioneColazioneUI(QWidget)
    mainWidget.show()
    sys.exit(app.exec_())