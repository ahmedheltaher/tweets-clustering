from PyQt5 import QtCore, QtWidgets


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
