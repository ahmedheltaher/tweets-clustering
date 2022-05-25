import random
from typing import List

import numpy


class KMeans:
    def __init__(self, clustersCount=4, maxIterations=50):
        self.__clustersCount = clustersCount
        self.__maxIterations = maxIterations
        self.__centroids = []
        self.__previousCentroids = []
        self.__clusters = {}
        self.__indicesTable = {}
        self.__iterationCount = 0
        self.__sse = 0

    def fit(self, tweets: List[any]):
        # initialization, assign random tweets as centroids

        for _ in range(self.__clustersCount):
            randomIndex = random.randint(0, len(tweets) - 1)
            if self.__indicesTable.get(randomIndex) is None:
                self.__indicesTable[randomIndex] = True
                self.__centroids.append(tweets[randomIndex])

        # run the iterations until not converged or until the max iteration in not reached
        while not self.__isConverged() and self.__iterationCount < self.__maxIterations:

            print("running iteration " + str(self.__iterationCount + 1))

            # assignment, assign tweets to the closest centroids
            self.__assignCluster(tweets)

            # to check if k-means converges, keep track of previousCentroids
            self.__previousCentroids = self.__centroids.copy()

            # update, update centroid based on clusters formed
            self.__updateCentroids()
            self.__iterationCount += 1

        if (self.__iterationCount == self.__maxIterations):
            print("max iterations reached, K means not converged")
        else:
            print("converged")

    def __isConverged(self) -> bool:
        # false if lengths are not equal
        if len(self.__previousCentroids) != len(self.__centroids):
            return False

        for current, previous in zip(self.__centroids, self.__previousCentroids):
            if current != previous:
                return False

        return True

    def __assignCluster(self, tweets: List[any]):
        self.__clusters = {}
        # for every tweet iterate each centroid and assign closest centroid to a it
        for tweet in tweets:
            minDistance = float('inf')
            closestCentroid = None

            for index, centroid in enumerate(self.__centroids):
                if centroid == tweet:
                    closestCentroid = index
                    minDistance = 0
                    break

                distance = self.__getDistance(centroid, tweet)
                if distance < minDistance:
                    minDistance = distance
                    closestCentroid = index

            if minDistance == 1:
                closestCentroid = random.randint(0, len(self.__centroids) - 1)

            if self.__clusters.get(closestCentroid) is None:
                self.__clusters[closestCentroid] = []
            self.__clusters[closestCentroid].append([tweet])
            lastTweetIndex = len(self.__clusters[closestCentroid]) - 1
            self.__clusters[closestCentroid][lastTweetIndex].append(minDistance)

    def __updateCentroids(self):
        self.__centroids = []
        for cluster in self.__clusters.keys():
            minDistanceSum = float('inf')
            closestTweet = -1

            distanceMemory = []

            for index, tweet in enumerate(self.__clusters[cluster]):
                distanceMemory.append([])
                distanceSum = 0
                for otherIndex, otherTweet in enumerate(self.__clusters[cluster]):
                    if index != otherIndex:

                        if otherIndex < index:
                            distance = distanceMemory[otherIndex][index]
                        else:
                            distance = self.__getDistance(tweet[0], otherTweet[0])
                    else:
                        distance = 0

                    distanceMemory[index].append(distance)
                    distanceSum += distance


                if distanceSum < minDistanceSum:
                    minDistanceSum = distanceSum
                    closestTweet = index

            self.__centroids.append(self.__clusters[cluster][closestTweet][0])

    def __getDistance(self, tweet1: list[any], tweet2: list[any]) -> float:
        # return the jaccard distance
        return 1 - (len(set(tweet1).intersection(tweet2)) / len(set().union(tweet1, tweet2)))

    def getSSE(self):
        if self.__sse == 0:
            self.__calculateSSE()
        return self.__sse

    def __calculateSSE(self):
        for cluster in self.__clusters.keys():
            for tweet in self.__clusters[cluster]:
                self.__sse += tweet[1] ** 2

    def setClustersCount(self, clustersCount):
        self.__clustersCount = clustersCount

    def setMaxIterations(self, maxIterations):
        self.__maxIterations = maxIterations

    def getCentroids(self):
        return self.__centroids

    def getClusters(self):
        return self.__clusters

    def reset(self):
        self.__centroids = []
        self.__previousCentroids = []
        self.__clusters = {}
        self.__sse = 0
        self.__iterationCount = 0
        self.__indicesTable = {}



