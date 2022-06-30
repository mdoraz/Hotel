import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class LoginProgrammaUI(QTabWidget):
    def __init__(self, pathFile:Path):
        super().__init__()
        self.page1 = QWidget()
        loadUi('ui/Titolare/login.ui', self.page1)
        self.addTab(self.page1, 'Login Programma')

        eyeBtn = QToolButton()  # creati i bottoni per mostrare/nascondere la password
        self._connectEye(eyeBtn, self.page1.lineeditPassword) # collega eyeBtn alla line edit corrispondente

        self.pathFile = pathFile




    def _connectEye(self, eyeButton: QToolButton, lineEdit: QLineEdit):
        def showHidePassword(checked):
            if checked:
                lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
                eyeButton.setIcon(QtGui.QIcon('files/icons/eye-close.jpg'))
            else:
                lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
                eyeButton.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))

        eyeButton.setIcon(QtGui.QIcon('files/icons/eye-open.jpg'))
        eyeButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        eyeButton.setCheckable(True)
        eyeButton.clicked.connect(showHidePassword)
        widgetAction = QWidgetAction(lineEdit)
        widgetAction.setDefaultWidget(eyeButton)
        lineEdit.addAction(widgetAction, QLineEdit.ActionPosition.TrailingPosition)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = LoginProgrammaUI()
    mainWidget.show()
    sys.exit(app.exec_())