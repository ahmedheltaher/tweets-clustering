
import sys

from PyQt5 import QtWidgets

from app.ui.MainWindow import Window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
