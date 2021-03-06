from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path

from src.Attori.Ruolo import Ruolo
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.Dipendenti.HomeCamerieri.HomeCamerieriUI import HomeCamerieriUI
from src.GUI.Dipendenti.HomeReceptionist.HomeReceptionistUI import HomeReceptionistUI
from src.GUI.HomeTitolare.HomeTitolareUI import HomeTitolareUI
from src.Utilities.encrypter import decrypt


class LoginProgrammaUI(QTabWidget):
    def __init__(self, previous: QWidget, pathFile:Path):
        super().__init__()
        self.page1 = QWidget()
        loadUi(GestoreFile.absolutePath('login.ui',Path.cwd()), self.page1)
        self.addTab(self.page1, 'Login Programma')
        self.setMinimumSize(500, 200)
        self.setFont(QtGui.QFont('Arial', 10))
        self.setWindowTitle('Struttura Alberghiera')

        eyeBtn = QToolButton()  # creati i bottoni per mostrare/nascondere la password
        self._connectEye(eyeBtn, self.page1.lineeditPassword) # collega eyeBtn alla line edit corrispondente

        self.pathFile = pathFile
        self._connectButtons()
        self.previous = previous
        self.msg = QMessageBox()  # per futuri messaggi


    def _connectButtons(self):
        self.page1.btnAccedi.clicked.connect(self._btnAccediClicked)
        self.page1.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnAccediClicked(self):

        if self.page1.lineeditUsername.text().strip() == '' or self.page1.lineeditPassword.text().strip == '': #Se lineeditUsername o lineeditPassword è vuota da errore e non conta gli spazi iniziali
            self._showMessage('Attenzione non hai riempito entrambi i campi richiesti!', QMessageBox.Icon.Warning)
            return
        username = self.page1.lineeditUsername.text()
        password = self.page1.lineeditPassword.text()
        dictionary = GestoreFile.leggiJson(Path('paths.json'))

        if self.pathFile == Path(dictionary['dipendenti']):
            dipendenti = self._readUtente('dipendenti')
            dipendenteUsername = None

            for dipendente in dipendenti.values():
                if dipendente.getUsername() == username:
                    dipendenteUsername = dipendente

            if dipendenteUsername == None:
                self._showMessage("Non esiste nessun dipendente con l'username ricercato", QMessageBox.Icon.Warning)
                return

            if decrypt(dipendenteUsername.getPassword()) != password:
                self._showMessage("La password non è corretta. Reinseriscila!", QMessageBox.Icon.Warning)
                return

            ruolo = dipendenteUsername.getAutorizzazione()
            if ruolo == Ruolo.RECEPTIONIST:
                self.close()
                self.widgetHomeReceptionist = HomeReceptionistUI(dipendenteUsername, self)
                self.widgetHomeReceptionist.show()
            else :
                self.close()
                self.widgetHomeCamerieri = HomeCamerieriUI(dipendenteUsername, self)
                self.widgetHomeCamerieri.show()

        elif self.pathFile == Path(dictionary['titolare']):
            titolare = self._readUtente('titolare')

            if username != titolare.getUsername() or password != decrypt(titolare.getPassword()):
                self._showMessage("Uno dei campi da te inseriti non è corretto. Riprova!", QMessageBox.Icon.Warning)
            else:
                self.close()
                self.mainwidgetHomeTitolare = HomeTitolareUI(titolare, self)
                self.mainwidgetHomeTitolare.show()

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()



    def _connectEye(self, eyeButton: QToolButton, lineEdit: QLineEdit):
        def showHidePassword(checked):
            if checked:
                lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
                eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-closed.png',Path.cwd())))
            else:
                lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
                eyeButton.setIcon(QtGui.QIcon((QtGui.QIcon(GestoreFile.absolutePath('eye-opened.png',Path.cwd())))))

        eyeButton.setIcon(QtGui.QIcon(GestoreFile.absolutePath('eye-opened.png',Path.cwd())))
        eyeButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        eyeButton.setCheckable(True)
        eyeButton.clicked.connect(showHidePassword)
        widgetAction = QWidgetAction(lineEdit)
        widgetAction.setDefaultWidget(eyeButton)
        lineEdit.addAction(widgetAction, QLineEdit.ActionPosition.TrailingPosition)

    def _showMessage(self, text: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon, windowTitle: str = 'Messaggio'):
        self.msg.setWindowTitle(windowTitle)
        self.msg.setIcon(icon)
        self.msg.setText(text)
        self.msg.show()

    def _readUtente(self, chiave):
        paths = GestoreFile.leggiJson(Path('paths.json'))
        try:
            if chiave == 'dipendenti':
                utenti = GestoreFile.leggiDictPickle(Path(paths[chiave]))
            elif chiave == 'titolare':
                try:
                    utenti = GestoreFile.leggiPickle(Path(paths[chiave]))
                except FileNotFoundError:
                    self._showMessage(f"{Path(paths[chiave]).name} non esiste, crearne uno.", QMessageBox.Icon.Critical, 'Errore')
                    self.close()
                    raise
            else:
                raise Exception("parametro 'chiave' non valido: deve essere o 'dipendenti' o 'titolare'")
        except TypeError:
            self._showMessage(
                f"{Path(paths[chiave]).name} è stato corrotto. Per far tornare il programma a funzionare correttamente, eliminare il file.",
                QMessageBox.Icon.Critical, 'Errore')
            self.close()
            raise

        return utenti
