import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pathlib import Path
from src.Gestori.GestoreFile import GestoreFile

class graficoStatisticheUI(QMainWindow):
    def __init__(self, previous : QWidget, nomeStatistica : str):
        super().__init__()
        loadUi(GestoreFile.absolutePath('graficoStatistiche.ui', Path.cwd()), self)
        self.setMinimumSize(700,200)
        self.setFont(QtGui.QFont('Arial', 10))
        self.previous = previous
        self._connectButtons()

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)#creato un horizontal Layout
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")#dato un nome all'Horizontal layout creato in precedenza
        self.figure = plt.figure()##tramite metodo di matplotlib, Canvas inserito un widget all'interno del frame (all'interno del widget andra il grafico)
        self.canvas = FigureCanvas(self.figure) # fine della greazione del canvas
        self.horizontalLayout_4.addWidget(self.canvas) #aggiunta alla canvas l'horizontal layout creato in precedenza

        if nomeStatistica == 'Colazione':    #A seconda della statistica ottengo un grafico diverso
            self.graficoStatistiche1()
        elif nomeStatistica == 'Noleggio Bici':
            self.graficoStatistiche2()
        elif nomeStatistica == 'Assenze':
            self.graficoStatistiche3()
        elif nomeStatistica == 'Tipo Soggiorno':
            self.graficoStatistiche4()

    def _connectButtons(self):
        self.btnIndietro.clicked.connect(self._btnIndietroClicked)

    def _btnIndietroClicked(self):
        self.close()
        self.previous.show()

    def graficoStatistiche1(self):
        self.figure.clear()
        plt.style.use("ggplot")
        labels = ['Giugno', 'Luglio', 'Agosto', 'Settembre']
        slices = [64, 673, 1890, 345]
        explode = [0.2, 0, 0, 0.2]
        plt.pie(slices, labels=labels, explode=explode, wedgeprops={'edgecolor': '#000000'}, startangle=180,
                autopct='%1.1f%%')
        plt.title('Statistiche Colazione In camera')
        self.canvas.draw()

    def graficoStatistiche2(self):
        self.figure.clear()
        plt.style.use("ggplot")
        indexs = np.arange(4)
        width = 0.3
        x = ['Giugno', 'Luglio', 'Agosto', 'Settembre']
        y1 = [30, 50, 80, 10]
        y2 = [10, 30, 70, 20]

        plt.bar(indexs, y1, label="Bici Uomo", width=width, color="purple")
        plt.bar(indexs + width, y2, label="Bici Donna Seggiolino", width=width, color="yellow")
        plt.title('Statistiche Utilizzo Bici')
        plt.xlabel("Mesi")
        plt.ylabel("Numero Utilizzo")
        plt.legend()
        plt.xticks(indexs + width / 2, x)
        self.canvas.draw()

    def graficoStatistiche3(self):
        self.figure.clear()
        plt.style.use("ggplot")
        indexs = np.arange(4)
        width = 0.3
        x = ['Giugno', 'Luglio', 'Agosto', 'Settembre']
        y1 = [30, 50, 80, 10]
        y2 = [10, 30, 70, 20]

        plt.bar(indexs, y1, label="Assenze Camerieri", width=width, color="red")
        plt.bar(indexs+width, y2, label="Assenze Receptionist", width=width, color="green")
        plt.title('Statistiche Assenze Dipendenti')
        plt.xlabel("Mesi")
        plt.ylabel("Numero Assenze")
        plt.legend()
        plt.xticks(indexs+width/2, x)
        self.canvas.draw()

    def graficoStatistiche4(self):
        self.figure.clear()
        labels = ['B&B', 'Mezza Pensione', 'Pensione Completa']
        slices = [64, 1670, 340]
        explode = [0.2, 0, 0.2]
        colors = ['lawngreen', 'chocolate', 'lightcoral']
        plt.pie(slices, labels=labels, explode=explode, colors=colors, startangle=180, autopct='%1.1f%%')
        plt.title('Statistiche Tipologia Soggiorno')
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = graficoStatisticheUI()
    mainWidget.show()
    sys.exit(app.exec_())