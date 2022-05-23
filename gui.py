## Only needed for access to command line arguments
#import sys
#from typing import List

#import numpy as np
#import pandas as pd
#from PyQt5.QtCore import QSize, Qt
#from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMessageBox,
#                             QPushButton)

## You need one (and only one) QApplication instance per application.
## Pass in sys.argv to allow command line arguments for your app.
## If you know you won't use command line arguments QApplication([]) works too.
#app = QApplication(sys.argv)

## Subclass QMainWindow to customize your application's main window
#class MainWindow(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.setWindowTitle("PyQt5 button")
#        self.setGeometry(100, 100, 300, 200)
#        self.setFixedSize(QSize(300, 200))
#        self.setStyleSheet("border: 1px solid #000000; border-radius: 5px; padding: 5px; background-color: #f4511e;")
#        self.initUI()

#        # Create a QPushButton
#        button = QPushButton("PyQt5 button", self)
#        button.setGeometry(100, 100, 100, 50)
#        button.setStyleSheet("border: 1px solid #000000; border-radius: 5px; padding: 5px;")
#        button.clicked.connect(self.on_click)


#    def on_click(self):
#        print("PyQt5 button was clicked")


#    def initUI(self):
#        # Create a QAction
#        exitAction = QAction("Exit", self)
#        exitAction.setShortcut("Ctrl+Q")
#        exitAction.setStatusTip("Exit application")
#        exitAction.triggered.connect(self.close)

#        # Create a QMenu
#        fileMenu = self.menuBar().addMenu("&File")
#        fileMenu.addAction(exitAction)


#    def closeEvent(self, event):
#        reply = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#        if reply == QMessageBox.Yes:
#            event.accept()
#        else:
#            event.ignore()


## Create a QMainWindow
#window = MainWindow()
#window.show()


import random as rd
import re
import string

import mplcursors
from matplotlib import pyplot as plt


def pre_process_tweets(url):

    f = open(url, "r", encoding="utf8")
    tweets = list(f)
    list_of_tweets = []

    for i in range(len(tweets)):

        # remove \n from the end after every sentence
        tweets[i] = tweets[i].strip('\n')

        # Remove the tweet id and timestamp
        tweets[i] = tweets[i][50:]

        # Remove any word that starts with the symbol @
        tweets[i] = " ".join(filter(lambda x: x[0] != '@', tweets[i].split()))

        # Remove any URL
        tweets[i] = re.sub(r"http\S+", "", tweets[i])
        tweets[i] = re.sub(r"www\S+", "", tweets[i])

        # remove colons from the end of the sentences (if any) after removing url
        tweets[i] = tweets[i].strip()
        tweet_len = len(tweets[i])
        if tweet_len > 0:
            if tweets[i][len(tweets[i]) - 1] == ':':
                tweets[i] = tweets[i][:len(tweets[i]) - 1]

        # Remove any hash-tags symbols
        tweets[i] = tweets[i].replace('#', '')

        # Convert every word to lowercase
        tweets[i] = tweets[i].lower()

        # remove punctuations
        tweets[i] = tweets[i].translate(str.maketrans('', '', string.punctuation))

        # trim extra spaces
        tweets[i] = " ".join(tweets[i].split())

        # convert each tweet from string type to as list<string> using " " as a delimiter
        list_of_tweets.append(tweets[i].split(' '))

    f.close()
    return list_of_tweets

if __name__ == '__main__':
    from app.model.kmeans import KMeans
    data_url = 'dataset/original/cnnhealth.txt'


    tweets = pre_process_tweets(data_url)

    # default number of experiments to be performed
    experiments = 5

    # default value of K for K-means
    clustersCount = 5
    sses = []
    # for every experiment 'e', run K-means

    model = KMeans(clustersCount)

    for e in range(experiments):

        print("------ Running K means for experiment no. " + str((e + 1)) + " for k = " + str(clustersCount))

        model.fit(tweets);
        sses.append(model.getSSE())
        
        print("--> SSE : " + str(model.getSSE()))
        print('\n')


        # increment k after every experiment
        clustersCount += 1
        model.reset()
        model.setClustersCount(clustersCount)

    # scatter plot of tweets with their respective centroid
    plt.figure(figsize=(10, 10))


    plt.plot([i + 1 for i in range(experiments)], sses, marker='o', color='b', linestyle='--', label='SSE', linewidth=2)
    plt.xlabel('Experiment')
    plt.ylabel('SSE')
    plt.title('SSE vs Experiment')
    mplcursors.cursor(hover=True)
    plt.legend()

    plt.show()
