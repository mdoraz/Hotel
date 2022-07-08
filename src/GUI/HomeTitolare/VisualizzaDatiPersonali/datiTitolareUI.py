import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.Attori.Amministratore import Amministratore
from src.GUI.HomeTitolare.GestioneDipendenti.InserimentoCredenzialiUI import InserimentoCredenzialiUI
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.HomeTitolare.GestioneDipendenti.FormUI import FormUI
from src.Utilities.GUIUtils import GUIUtils
from src.Utilities.encrypter import encrypt, decrypt


class datiTitolareUI(QTabWidget, FormUI):
    def __init__(self, titolare : Amministratore, previous: QWidget):
        super().__init__()
        
        loadUi(GestoreFile.absolutePath('datiTitolare.ui', Path.cwd()),self)
        
        self.titolare = titolare
        self.previous = previous
        
        self._fillFields()
        self._setValidators() # si impostano i validator per le line edit di email e cellulare
        self._setColorHints()
        self._connectButtons()


    def _fillFields(self):
        self.lineEditEmail.setText(self.titolare.getEmail())
        self.lineEditCellulare.setText(self.titolare.getCellulare())
        self.lineEditUsername.setText(self.titolare.getUsername())
        self.lineEditPassword.setText('password')


    def _setValidators(self):
        self.lineEditEmail.setValidator(GUIUtils.validators['email'])
        self.lineEditCellulare.setValidator(GUIUtils.validators['cellulare'])


    def _setColorHints(self):
        self.lineEditEmail.textChanged.connect(self._setColorHint)
        self.lineEditCellulare.textChanged.connect(self._setColorHint)


    def _connectButtons(self):
        self.btnEmail.clicked.connect(self._modificaEmailClicked)
        self.btnCellulare.clicked.connect(self._modificaCellulareClicked)
        self.btnUsername.clicked.connect(self._modificaUsernameClicked)
        self.btnPassword.clicked.connect(self._modificaPasswordClicked)
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    
    def _modificaEmailClicked(self):
        self.btnEmail.clicked.disconnect(self._modificaEmailClicked)
        self.btnEmail.clicked.connect(self._salvaEmailClicked)
        self.btnEmail.setText('Salva')

        self.lineEditEmail.setReadOnly(False)
        self.lineEditEmail.textChanged.connect(self._setColorHint)
    
    
    def _salvaEmailClicked(self):
        self.btnEmail.clicked.disconnect(self._salvaEmailClicked)
        self.btnEmail.clicked.connect(self._modificaEmailClicked)
        self.btnEmail.setText('Modifica')

        if self.lineEditEmail.validator().validate(self.lineEditEmail.text(), 0)[0] != QtGui.QValidator.State.Acceptable:
            self._showMessage('Email non valida.', QMessageBox.Icon.Warning, 'Errore')
            return

        self.titolare.setEmail(self.lineEditEmail.text())
        self._salvaTitolare()

        self.lineEditEmail.setReadOnly(True)
        self.lineEditEmail.textChanged.disconnect(self._setColorHint)
        font = self.lineEditEmail.font()
        # tolgo il colore della scritta dallo style sheet
        self.lineEditEmail.setStyleSheet(f'font-family: {font.family()}; font-size: {font.pointSize()}pt') # mettendo una stringa vuota si azzera il font
    
    
    def _modificaCellulareClicked(self):
        self.btnCellulare.clicked.disconnect(self._modificaCellulareClicked)
        self.btnCellulare.clicked.connect(self._salvaCellulareClicked)
        self.btnCellulare.setText('Salva')

        self.lineEditCellulare.setReadOnly(False)
        self.lineEditCellulare.textChanged.connect(self._setColorHint)
    

    def _salvaCellulareClicked(self):
        self.btnCellulare.clicked.disconnect(self._salvaCellulareClicked)
        self.btnCellulare.clicked.connect(self._modificaCellulareClicked)
        self.btnCellulare.setText('Modifica')

        if self.lineEditCellulare.validator().validate(self.lineEditCellulare.text(), 0)[0] != QtGui.QValidator.State.Acceptable:
            self._showMessage('Cellulare non valido.', QMessageBox.Icon.Warning, 'Errore')
            return

        self.titolare.setCellulare(self.lineEditCellulare.text())
        self._salvaTitolare()
        
        self.lineEditCellulare.setReadOnly(True)
        self.lineEditCellulare.textChanged.disconnect(self._setColorHint)
        font = self.lineEditCellulare.font()
        self.lineEditCellulare.setStyleSheet(f'font-family: {font.family()}; font-size: {font.pointSize()}pt')
    
    
    def _modificaUsernameClicked(self):
        self.btnUsername.clicked.disconnect(self._modificaUsernameClicked)
        self.btnUsername.clicked.connect(self._salvaUsernameClicked)
        self.btnUsername.setText('Salva')

        self.lineEditUsername.setReadOnly(False)
    

    def _salvaUsernameClicked(self):
        self.btnUsername.clicked.disconnect(self._salvaUsernameClicked)
        self.btnUsername.clicked.connect(self._modificaUsernameClicked)
        self.btnUsername.setText('Modifica')

        if self.lineEditUsername.text().strip() == '':
            self._showMessage('Username non valido.', QMessageBox.Icon.Warning, 'Errore')
            return
        
        self.titolare.setUsername(self.lineEditUsername.text())
        self._salvaTitolare()
        self.lineEditUsername.setReadOnly(True)
    
    
    def _modificaPasswordClicked(self):
        self.widgetPassword = InserimentoCredenzialiUI()
        self.widgetPassword.labelIntestazione.hide()
        self.widgetPassword.widgetUsername.deleteLater()
        del self.widgetPassword.lineEditLabelPairs[self.widgetPassword.lineEditUsername] # rimuovo dal dizionario di line edit e label l'entry dell'username
        
        self.widgetPassword.btnIndietro.setText('Annulla')
        self.widgetPassword.btnIndietro.clicked.connect(self.widgetPassword.close)

        self.widgetPassword.btnInserisci.setText('Salva')
        self.widgetPassword.btnInserisci.clicked.connect(self._salvaPasswordClicked)
        self.widgetPassword.show()
    

    def _salvaPasswordClicked(self):
        if not self.widgetPassword.fieldsFilled(self.widgetPassword.lineEditLabelPairs):
            return # il messaggio di erroreè è stato già mostrato
        if self.widgetPassword.lineEditVecchiaPassword.text() != decrypt(self.titolare.getPassword()):
            self._showMessage('La vecchia password non è corretta.', QMessageBox.Icon.Warning, 'Errore')
            return
        # se la password rispetta la struttura specificata e coincide con la conferma password
        if not self.widgetPassword.isPasswordCorrect():
            return # l'erorre opportuno è stato già mostrato dal metodo isPasswordCorrect
        
        self.titolare.setPassword(encrypt(self.widgetPassword.lineEditPassword.text()))
        self._salvaTitolare()
        self.widgetPassword.close()


    def _btnIndietroClicked(self):
        self.previous.show()
        self.close()
    

    def _salvaTitolare(self):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        GestoreFile.salvaPickle(self.titolare, Path(paths['titolare']))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    paths = GestoreFile.leggiJson(Path('paths.json'))
    titolare = GestoreFile.leggiPickle(Path(paths['titolare']))
    if isinstance(titolare, Amministratore):
        mainWidget = DatiTitolareUI(titolare, QWidget())  # type: ignore
        mainWidget.show()
        sys.exit(app.exec_())