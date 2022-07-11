from pathlib import Path
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from src.Gestori.GestoreFile import GestoreFile


class SelezionaDaLista(QWidget):

	def __init__(self):
		super().__init__()

		loadUi(GestoreFile.absolutePath('selezionaDaLista.ui', Path.cwd()), self)
