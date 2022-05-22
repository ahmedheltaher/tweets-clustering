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

import csv
import math
import random as rd
import re
import string
from typing import List

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


def k_means(tweets, clustersCount=4, max_iterations=50):
    centroids = []


    # initialization, assign random tweets as centroids
    indicesTable = {}
    for _ in range(clustersCount):
        randomIndex = rd.randint(0, len(tweets) - 1)
        if indicesTable.get(randomIndex) is None:
            indicesTable[randomIndex] = True
            centroids.append(tweets[randomIndex])



    iter_count = 0
    prev_centroids = []

    # run the iterations until not converged or until the max iteration in not reached
    while (not(is_converged(prev_centroids, centroids)) and (iter_count < max_iterations)) :

        print("running iteration " + str(iter_count))

        # assignment, assign tweets to the closest centroids
        clusters = assign_cluster(tweets, centroids)

        # to check if k-means converges, keep track of prev_centroids
        prev_centroids = centroids

        # update, update centroid based on clusters formed
        centroids = update_centroids(clusters)
        iter_count = iter_count + 1

    if (iter_count == max_iterations):
        print("max iterations reached, K means not converged")
    else:
        print("converged")

    sse = compute_SSE(clusters)

    return clusters, sse, centroids


def is_converged(prev_centroid, new_centroids):
    return prev_centroid == new_centroids


def assign_cluster(tweets, centroids):
    clusters = dict()

    # for every tweet iterate each centroid and assign closest centroid to a it
    for t in range(len(tweets)):
        min_dis = math.inf
        cluster_idx = -1;
        for c in range(len(centroids)):
            dis = getDistance(centroids[c], tweets[t])
            # look for a closest centroid for a tweet

            if centroids[c] == tweets[t]:
                # print("tweet and centroid are equal with c: " + str(c) + ", t" + str(t))
                cluster_idx = c
                min_dis = 0
                break

            if dis < min_dis:
                cluster_idx = c
                min_dis = dis

        # randomise the centroid assignment to a tweet if nothing is common
        if min_dis == 1:
            cluster_idx = rd.randint(0, len(centroids) - 1)

        # assign the closest centroid to a tweet
        clusters.setdefault(cluster_idx, []).append([tweets[t]])
        # print("tweet t: " + str(t) + " is assigned to cluster c: " + str(cluster_idx))
        # add the tweet distance from its closest centroid to compute sse in the end
        last_tweet_idx = len(clusters.setdefault(cluster_idx, [])) - 1
        clusters.setdefault(cluster_idx, [])[last_tweet_idx].append(min_dis)

    return clusters


def update_centroids(clusters):
    centroids = []

    # iterate each cluster and check for a tweet with closest distance sum with all other tweets in the same cluster
    # select that tweet as the centroid for the cluster
    for c in range(len(clusters)):
        min_dis_sum = math.inf
        centroid_idx = -1

        # to avoid redundant calculations
        min_dis_dp = []

        for t1 in range(len(clusters[c])):
            min_dis_dp.append([])
            dis_sum = 0
            # get distances sum for every of tweet t1 with every tweet t2 in a same cluster
            for t2 in range(len(clusters[c])):
                if t2 < t1:
                    dis = min_dis_dp[t2][t1]
                else:
                    dis = getDistance(clusters[c][t1][0], clusters[c][t2][0])

                min_dis_dp[t1].append(dis)
                dis_sum += dis

            # select the tweet with the minimum distances sum as the centroid for the cluster
            if dis_sum < min_dis_sum:
                min_dis_sum = dis_sum
                centroid_idx = t1

        # append the selected tweet to the centroid list
        centroids.append(clusters[c][centroid_idx][0])

    return centroids

def getDistance(list1: List[any], list2: List[any]) -> float:
    return 1 - (len(list(set(list1).intersection(set(list2)))) / len(list(set(list1).union(set(list2)))))

def compute_SSE(clusters):
    sse = 0
    for index, cluster in enumerate(clusters):
        for tweet in clusters[cluster]:
            sse += tweet[1] ** 2
    return sse

def read_csv(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:  # Open the text file

        reader = csv.reader(file)
        next(reader)  # Skip the first line
        data = [row[3].split(" ") for row in reader]  # Read the file as a list of lists

    return data


if __name__ == '__main__':

    data_url = 'dataset/original/everydayhealth.txt'

    #csv_tweets = read_csv(data_url)

    tweets = pre_process_tweets(data_url)

    # default number of experiments to be performed
    experiments = 3

    # default value of K for K-means
    clustersCount = 5
    sses = []
    # for every experiment 'e', run K-means
    for e in range(experiments):

        print("------ Running K means for experiment no. " + str((e + 1)) + " for k = " + str(clustersCount))

        clusters, sse, centroids = k_means(tweets, clustersCount)
        size = [len(cluster) for cluster in clusters.values()]
        sses.append(sse)
        
        print("--> SSE : " + str(sse))
        print('\n')


        # increment k after every experiment
        clustersCount += 1

    # scatter plot of tweets with their respective centroid
    plt.figure(figsize=(10, 10))


    plt.plot([i for i in range(experiments)], sses, marker='o', color='b', linestyle='--', label='SSE', linewidth=2)
    plt.xlabel('Experiment')
    plt.ylabel('SSE')
    plt.title('SSE vs Experiment')
    mplcursors.cursor(hover=True)

    plt.show()
