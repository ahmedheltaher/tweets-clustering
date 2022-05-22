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

import collections
import csv
import math
import random as rd
import re
import string
from typing import List

import mplcursors
import numpy as np
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


def k_means(tweets, clustersCount=4, maxIterations=50):
    centroids = []
    interactionNumber = 0
    previousCentroids = []

    # initialization, assign random tweets as centroids
    indicesTable = {}
    for _ in range(clustersCount):
        randomIndex = rd.randint(0, len(tweets) - 1)
        if indicesTable.get(randomIndex) is None:
            indicesTable[randomIndex] = True
            centroids.append(tweets[randomIndex])

    # run the iterations until not converged or until the max iteration in not reached
    while not is_converged(previousCentroids, centroids) and interactionNumber < maxIterations:

        print("running iteration " + str(interactionNumber))

        # assignment, assign tweets to the closest centroids
        clusters = assign_cluster(tweets, centroids)

        # to check if k-means converges, keep track of previousCentroids
        previousCentroids = centroids.copy()

        # update, update centroid based on clusters formed
        centroids = update_centroids(clusters)
        interactionNumber += 1

    if (interactionNumber == maxIterations):
        print("max iterations reached, K means not converged")
    else:
        print("converged")

    sse = compute_SSE(clusters)

    return clusters, sse


def is_converged(previousCentroid: List[any], newCentroids: List[any]) -> bool:
    previousCentroid = np.array(previousCentroid, dtype=object)
    newCentroids = np.array(newCentroids, dtype=object)
    return np.array_equal(previousCentroid, newCentroids)

def assign_cluster(tweets, centroids):
    clusters = {}

    # for every tweet iterate each centroid and assign closest centroid to a it
    for tweet in tweets:
        minDistance = float('inf')
        closestCentroid = None

        for index, centroid in enumerate(centroids):
            if centroid == tweet:
                closestCentroid = index
                minDistance = 0
                break

            distance = getDistance(centroid, tweet)
            if distance < minDistance:
                minDistance = distance
                closestCentroid = index

        if minDistance == 1:
            closestCentroid = rd.randint(0, len(centroids) - 1)

        if clusters.get(closestCentroid) is None:
            clusters[closestCentroid] = []
        clusters[closestCentroid].append([tweet])
        lastTweetIndex = len(clusters[closestCentroid]) - 1
        clusters[closestCentroid][lastTweetIndex].append(minDistance)

    return clusters

def update_centroids(clusters):
    centroids = []

    # iterate each cluster and check for a tweet with closest distance sum with all other tweets in the same cluster
    # select that tweet as the centroid for the cluster
    for cluster in clusters.keys():
        minDistanceSum = float('inf')
        closestTweet = -1

        distanceMemory = []

        for index, tweet in enumerate(clusters[cluster]):
            distanceMemory.append([])
            distanceSum = 0
            for otherIndex, otherTweet in enumerate(clusters[cluster]):
                if otherIndex < index:
                    distance = distanceMemory[otherIndex][index]
                else:
                    distance = getDistance(tweet[0], otherTweet[0])

                distanceMemory[index].append(distance)
                distanceSum += distance


            if distanceSum < minDistanceSum:
                minDistanceSum = distanceSum
                closestTweet = index

        centroids.append(clusters[cluster][closestTweet][0])

    return centroids

def getDistance(list1: List[any], list2: List[any]) -> float:
    return 1 - (len(list(set(list1).intersection(set(list2)))) / len(list(set(list1).union(set(list2)))))

def compute_SSE(clusters):
    sse = 0
    for index, cluster in enumerate(clusters):
        for tweet in clusters[cluster]:
            sse += tweet[1] ** 2
    return sse

if __name__ == '__main__':

    data_url = 'dataset/original/everydayhealth.txt'


    tweets = pre_process_tweets(data_url)

    # default number of experiments to be performed
    experiments = 3

    # default value of K for K-means
    clustersCount = 5
    sses = []
    # for every experiment 'e', run K-means
    for e in range(experiments):

        print("------ Running K means for experiment no. " + str((e + 1)) + " for k = " + str(clustersCount))

        clusters, sse = k_means(tweets, clustersCount)
        sses.append(sse)
        
        print("--> SSE : " + str(sse))
        print('\n')


        # increment k after every experiment
        clustersCount += 1

    # scatter plot of tweets with their respective centroid
    plt.figure(figsize=(10, 10))


    plt.plot([i + 1 for i in range(experiments)], sses, marker='o', color='b', linestyle='--', label='SSE', linewidth=2)
    plt.xlabel('Experiment')
    plt.ylabel('SSE')
    plt.title('SSE vs Experiment')
    mplcursors.cursor(hover=True)
    plt.legend()

    plt.show()
