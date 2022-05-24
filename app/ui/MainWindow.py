
import math
import multiprocessing
import threading

import mplcursors
import pandas
from app.model.kmeans import KMeans
from app.ui.SplashScreen import SplashScreen
from app.utils.files import filesInDirectory
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtGui, QtWidgets


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.processes = []
        self.finishedProcesses = 0
        
        self.splashScreen = SplashScreen()
        self.clusteringThread = None
        self.setWindowTitle("PyQt5 Matplotlib example")
        self.setGeometry(5, 30, 1920, 1080)

        # Create matplotlib figure and axes
        self.figure = Figure()
        self.figure.patch.set_facecolor('#376E6F')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QtWidgets.QPushButton('Start')
        self.button.clicked.connect(self.__experimentsControl)
        self.button.setFont(QtGui.QFont("Arial", 18))

        dataSetFiles = [file.removesuffix(".csv") for file in sorted(filesInDirectory('dataset/csv/')) if file.endswith('.csv')]
        self.selectDataSetFile = QtWidgets.QComboBox()
        self.selectDataSetFile.addItems(dataSetFiles)
        self.selectDataSetFile.setCurrentIndex(2)
        self.selectDataSetFile.setFont(QtGui.QFont("Arial", 18))
        

        self.clusterCount = QtWidgets.QSpinBox()
        self.clusterCount.setValue(3)
        self.clusterCount.setFont(QtGui.QFont("Arial", 18))

        self.experimentsCount = QtWidgets.QSpinBox()
        self.experimentsCount.setValue(5)
        self.experimentsCount.setFont(QtGui.QFont("Arial", 18))


        self.statusLabel = QtWidgets.QLabel("Status:")
        self.statusLabel.setFont(QtGui.QFont("Arial", 18))

        # Top Control bar layout =================================================
        topControlsBox = QtWidgets.QHBoxLayout()
        topControlsBox.addWidget(self.selectDataSetFile, 1)
        topControlsBox.addWidget(self.clusterCount, 1)
        topControlsBox.addWidget(self.experimentsCount, 1)
        topControlsBox.addWidget(self.button)
        # Top Control bar layout =================================================
        

        # Canvas Box =============================================================
        canvasBox = QtWidgets.QHBoxLayout()
        canvasBox.addWidget(self.canvas)
        # Canvas Box =============================================================

        # Main Layout =============================================================
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(topControlsBox)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(canvasBox, 1)
        mainLayout.addWidget(self.toolbar)
        # Main Layout =============================================================

        # Main Frame =============================================================
        # Set the layout to the main window
        self.mainFrame = QtWidgets.QWidget()
        self.mainFrame.setLayout(mainLayout)
        self.setCentralWidget(self.mainFrame)
        # Main Frame =============================================================


        self.setStyleSheet('''
            QMainWindow {
                background-color: #2F4454;
            }
            
            QPushButton {
                background-color: #376E6F;
                color: #FFFFFF;
            }

            QPushButton:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }

            QComboBox {
                background-color: #376E6F;
                color: #FFFFFF;
            }

            QSpinBox {
                background-color: #376E6F;
                color: #FFFFFF;
            }

            QSpinBox:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }

            QLabel {
                background-color: #2F4454;
                color: #FFFFFF;
            }
            QStatusBar {
                background-color: #2F4454;
                color: #FFFFFF;
            }

            QStatusBar:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }

            QMenuBar {
                background-color: #2F4454;
                color: #FFFFFF;
            }

            QMenuBar:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }

            QMenuBar::item {
                background-color: #2F4454;
                color: #FFFFFF;
            }

            QMenuBar::item:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }

            QMenuBar::item:selected {
                background-color: #376E6F;
                color: #FFFFFF;
            }

            QMenuBar::item:selected:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }

            QMenu {
                background-color: #2F4454;
                color: #FFFFFF;
            }

            QMenu:hover {
                background-color: #FFFFFF;
                color: #2F4454;
            }
        ''')
    def __experimentsControl(self):
        self.splashScreen.show()
        self.splashScreen.progressBar.setValue(0)
        
        self.clusteringThread = threading.Thread(target=self.clusteringThreadFunction)
        self.clusteringThread.start()

        self.splashScreen.show()
        self.splashScreen.progressBar.setValue(0)
        QtWidgets.QApplication.processEvents()

    def clusteringThreadFunction(self):
        dataSetFile = pandas.read_csv(f'dataset/csv/{self.selectDataSetFile.currentText()}.csv')
        # Extract the tweets from the data set
        tweets = [tweet.split() for tweet in dataSetFile['tweet'].astype(str)]
        # default number of experiments to be performed
        experiments = self.experimentsCount.value()
        # default value of K for K-means
        clustersCount = self.clusterCount.value()
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        for i in range(experiments):
            process = multiprocessing.Process(target=self.__performClustering, args=(clustersCount + i, return_dict, tweets))
            self.processes.append(process)
            process.start()

        for process in  self.processes:
            process.join()

        print(return_dict)
        self.splashScreen.close()
        self.__plot(sorted(list(return_dict.keys())), [return_dict[key] for key in sorted(list(return_dict.keys()))])

    def __performClustering(self, clustersCount, sses, tweets):
        model = KMeans(clustersCount)
        model.fit(tweets)
        sses[clustersCount] = model.getSSE()

    def __plot(self, xData=[], yData=[]):
        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(xData, yData, marker='o', color='b', linestyle='--', label='SSE', linewidth=2)
        ax.set_xlabel('Experiment')
        ax.set_ylabel('SSE')
        mplcursors.cursor(hover=True)
        # refresh canvas
        self.canvas.draw()

    def __updateStatus(self, status: str) -> None:
        self.statusLabel.setText(f"Status: {status}")
        self.statusLabel.repaint()

    def closeEvent(self, event):
        self.splashScreen.close()
        for process in  self.processes:
            process.terminate()
        event.accept()
