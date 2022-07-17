from PyQt5 import QtGui
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile
from src.GUI.HomeTitolare.VisualizzaStatistiche.graficoStatisticheUI import graficoStatisticheUI



class VisualizzaStatisticheUI(QTabWidget):
    def __init__(self, previous : QWidget):
        super().__init__()
        loadUi(GestoreFile.absolutePath('VisualizzaStatistiche.ui', Path.cwd()), self)
        self.setMinimumSize(700,200)
        self.setFont(QtGui.QFont('Arial', 10))
        self._connectButtons()
        self.previous = previous

    def _connectButtons(self):
        self.btnStatisticheColazioneInCamera.clicked.connect(self._btnStatisticheColazioneInCameraClicked)
        self.btnStatisticheNoleggioBici.clicked.connect(self._btnStatisticheNoleggioBiciClicked)
        self.btnStatisticheAssenzeDipendenti.clicked.connect(self._btnStatisticheAssenzeDipendentiClicked)
        self.btnStatisticheTipologiaSoggiorno.clicked.connect(self._btnStatisticheTipologiaSoggiornoClicked)
        self.btnTornareIndietro.clicked.connect(self._btnTornareIndietroClicked)


    def _btnStatisticheColazioneInCameraClicked(self):
        self.close()
        self.widgetgraficoStatistiche = graficoStatisticheUI(self, 'Colazione')
        self.widgetgraficoStatistiche.show()

    def _btnStatisticheNoleggioBiciClicked(self):
        self.close()
        self.widgetgraficoStatistiche = graficoStatisticheUI(self, 'Noleggio Bici')
        self.widgetgraficoStatistiche.show()

    def _btnStatisticheAssenzeDipendentiClicked(self):
        self.close()
        self.widgetgraficoStatistiche = graficoStatisticheUI(self, 'Assenze')
        self.widgetgraficoStatistiche.show()

    def _btnStatisticheTipologiaSoggiornoClicked(self):
        self.close()
        self.widgetgraficoStatistiche = graficoStatisticheUI(self, 'Tipo Soggiorno')
        self.widgetgraficoStatistiche.show()

    def _btnTornareIndietroClicked(self):
        self.close()
        self.previous.show()
