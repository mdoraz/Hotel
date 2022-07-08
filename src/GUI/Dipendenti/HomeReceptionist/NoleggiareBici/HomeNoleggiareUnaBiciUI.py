import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.AssegnaBiciPrenotateUI import AssegnaBiciPrenotateUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.AssegnaBiciSenzaPrenotazioneUI import AssegnaBiciSenzaPrenotazioneUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.ConfermaTerminareNoleggioUI import ConfermaTerminareNoleggioUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.EliminaPrenotazioneBiciUI import EliminaPrenotazioneBiciUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.ModificaPrenotazioneBiciUI import ModificaPrenotazioneBiciUI
from src.GUI.Dipendenti.HomeReceptionist.NoleggiareBici.RicercaPrenotazioneBiciUI import RicercaPrenotazioneBiciUI


class HomeNoleggiareUnaBiciUI(QTabWidget):
    def __init__(self, previous: QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('HomeNoleggiareUnaBici.ui', Path.cwd()), self)
        self.setMinimumSize(1000,600)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnRicercaOrarioRicercato.clicked.connect(self._btnRicercaOrarioRicercatoClicked)
        self.btnAssociaBiciSelezionataAllaPrenotazione.clicked.connect(self._btnAssociaBiciSelezionataAllaPrenotazioneClicked)
        self.btnAssociaCameraAllaPrenotazione.clicked.connect(self._btnAssociaCameraAllaPrenotazioneClicked)
        self.btnEffettuaPrenotazione.clicked.connect(self._btnEffettuaPrenotazioneClicked)
        self.btnRicercaPrenotazioneBici.clicked.connect(self._btnRicercaPrenotazioneBiciClicked)
        self.btnModificaPrenotazione.clicked.connect(self._btnModificaPrenotazioneClicked)
        self.btnEliminaPrenotazione.clicked.connect(self._btnEliminaPrenotazioneClicked)
        self.btnNo.clicked.connect(self._btnNoClicked)
        self.btnSi.clicked.connect(self._btnSiClicked)
        self.btnRicercaNoleggiAssociati.clicked.connect(self._btnRicercaNoleggiAssociatiClicked)
        self.btnConfermaTerminareNoleggio.clicked.connect(self._btnConfermaTerminareNoleggioClicked)
        self.btnTornareHomeReceptionist.clicked.connect(self._btnTornareHomeReceptionistClicked)

    def _btnRicercaOrarioRicercatoClicked(self):
        #vedere a schermo messaggio di errore se non ci sono bici nell'orario inserito
        pass

    def _btnAssociaBiciSelezionataAllaPrenotazioneClicked(self):
        pass

    def _btnAssociaCameraAllaPrenotazioneClicked(self):
        pass

    def _btnEffettuaPrenotazioneClicked(self):
        pass

    def _btnRicercaPrenotazioneBiciClicked(self):
        self.close()
        self.widgetRicercaPrenotazioneBici = RicercaPrenotazioneBiciUI(self)
        self.widgetRicercaPrenotazioneBici.show()

    def _btnModificaPrenotazioneClicked(self):
        self.close()
        self.widgetModificaPrenotazioneBici = ModificaPrenotazioneBiciUI(self)
        self.widgetModificaPrenotazioneBici.show()

    def _btnEliminaPrenotazioneClicked(self):
        self.close()
        self.widgetEliminaPrenotazioneBici = EliminaPrenotazioneBiciUI(self)
        self.widgetEliminaPrenotazioneBici.show()

    def _btnNoClicked(self):
        self.close()
        self.widgetAssegnaBiciSenzaPrenotazione = AssegnaBiciSenzaPrenotazioneUI(self)
        self.widgetAssegnaBiciSenzaPrenotazione.show()

    def _btnSiClicked(self):
        self.close()
        self.widgetAssegnaBiciPrenotate = AssegnaBiciPrenotateUI(self)
        self.widgetAssegnaBiciPrenotate.show()

    def _btnRicercaNoleggiAssociatiClicked(self):
        pass

    def _btnConfermaTerminareNoleggioClicked(self):
        self.close()
        self.widgetConfermaTerminareNoleggio = ConfermaTerminareNoleggioUI(self)
        self.widgetConfermaTerminareNoleggio.show()

    def _btnTornareHomeReceptionistClicked(self):
        self.close()
        self.previous.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomeNoleggiareUnaBiciUI()
    mainWidget.show()
    sys.exit(app.exec_())