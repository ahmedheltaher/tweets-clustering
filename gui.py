import math
import sys
import threading
import time

import pandas
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

from app.model.kmeans import KMeans
from app.utils.files import filesInDirectory

app = QtWidgets.QApplication(sys.argv)

class SplashScreen(QtWidgets.QDialog):
    def __init__(self):
        self.i = 1
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        self.initUI()
        self.oldPos = self.pos()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.frame = QtWidgets.QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QtWidgets.QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)  # x, y
        self.labelTitle.setText('Splash Screen')
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.labelDescription = QtWidgets.QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Working on Task #1</strong>')
        self.labelDescription.setAlignment(QtCore.Qt.AlignCenter)

        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(20)

        self.labelLoading = QtWidgets.QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLoading.setText('loading...')

        self.setStyleSheet('''
            #LabelTitle {
                font-size: 60px;
                color: #93deed;
            }

            #LabelDesc {
                font-size: 30px;
                color: #c2ced1;
            }

            #LabelLoading {
                font-size: 30px;
                color: #e8e8eb;
            }

            QFrame {
                background-color: #2F4454;
                color: rgb(220, 220, 220);
            }

            QProgressBar {
                background-color: #DA7B93;
                color: rgb(200, 200, 200);
                border-style: none;
                border-radius: 10px;
                text-align: center;
                font-size: 30px;
            }

            QProgressBar::chunk {
                border-radius: 10px;
                background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
            }
        ''')


        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        if self.i >= 5:
            self.i = 0;
        self.labelLoading.setText(f'loading{self.i * "."}')
        self.labelLoading.repaint()
        self.i += 1

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.splashScreen = SplashScreen()
        self.clusteringThread = None
        self.setWindowTitle("PyQt5 Matplotlib example")
        self.setGeometry(5, 30, 1920, 1080)

        # Create matplotlib figure and axes
        self.figure = Figure()
        self.figure.patch.set_facecolor('white')
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

    def __experimentsControl(self):
        self.splashScreen.show()
        self.splashScreen.progressBar.setValue(0)
        
        self.clusteringThread = threading.Thread(target=self.clusteringThreadFunction)
        self.clusteringThread.start()

        self.splashScreen.show()
        self.splashScreen.progressBar.setValue(0)
        app.processEvents()

    def clusteringThreadFunction(self):
        dataSetFile = pandas.read_csv(f'dataset/csv/{self.selectDataSetFile.currentText()}.csv')
        # Extract the tweets from the data set
        tweets = [tweet for tweet in dataSetFile['tweet'].astype(str)]
        # default number of experiments to be performed
        experiments = self.experimentsCount.value()
        # default value of K for K-means
        clustersCount = self.clusterCount.value()
        sses = []
        model = KMeans(clustersCount)
        for e in range(experiments):
            self.__updateStatus(f"Running experiment {e + 1} for k = {clustersCount}")
            model.fit(tweets)
            sses.append(model.getSSE())

            # increment k after every experiment
            clustersCount += 1

            model.reset()
            model.setClustersCount(clustersCount)
            self.splashScreen.progressBar.setValue(math.floor(100 / experiments * (e + 1)))

        self.splashScreen.close()
        self.__plot([i + 1 for i in range(abs(experiments - clustersCount + 1), clustersCount - 1)], sses)

    def __plot(self, xData=[], yData=[]):
        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(xData, yData, '*-')

        # refresh canvas
        self.canvas.draw()

    def __updateStatus(self, status: str) -> None:
        self.statusLabel.setText(f"Status: {status}")
        self.statusLabel.repaint()

    def closeEvent(self, event):
        self.splashScreen.close()
        self.clusteringThread.raise_exception()
        event.accept()


if __name__ == '__main__':

    main = Window()
    main.show()

    sys.exit(app.exec_())
