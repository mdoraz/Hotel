from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src.Gestori.GestoreFile import GestoreFile

class VisualizzaDatiPersonaliDipendenteUI(QTabWidget):

    def __init__(self, dipendente, previous: QWidget):
        super().__init__()

        loadUi(GestoreFile.absolutePath('VisualizzaDatiPersonaliDipendente.ui',Path.cwd()), self)

        self.previous = previous
        self.dipendente = dipendente

        self._fillFieldsDipendente()
        self._connectButtons()

    def _fillFieldsDipendente(self):
        self.lineeditNome.setText(self.dipendente.getNome())
        self.lineeditCognome.setText(self.dipendente.getCognome())
        self.lineeditLuogoDiNascitaProvincia.setText(self.dipendente.getLuogoNascita())
        self.dateeditDataDiNascita.setDate(self.dipendente.getDataNascita())
        self.lineeditTelefono.setText(self.dipendente.getCellulare())
        self.lineeditIndirizzoEmail.setText(self.dipendente.getEmail())
        self.lineeditIBAN.setText(self.dipendente.getIBAN())
        self.lineeditTurnoDiLavoro.setText('Mattina'if self.dipendente.getTurno() == True else 'Pomeriggio')
        self.lineeditRuolo.setText(self.dipendente.getAutorizzazione().name.capitalize())

    def _connectButtons(self):
        self.btnOk.clicked.connect(self._btnOkClicked)

    def _btnOkClicked(self):
        self.close()
        self.previous.show()

