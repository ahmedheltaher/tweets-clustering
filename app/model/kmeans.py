import random
from typing import List


class KMeans:
    '''
        This Class is used to Perform K-Means Clustering on a given set of tweets
        The tweets are represented as a list of lists of strings

        Methods:
        --------
            fit:
                This method takes a list of tweets as input and performs k-means clustering on it
            getCentroids:
                This method returns the centroids of the clusters formed
            getClusters:
                This method returns the clusters formed
            getSSE:
                This method returns the sum of squared errors of the clusters formed


        Attributes:
        -----------
            __clustersCount:
                The number of clusters to be formed
            __maxIterations:
                The maximum number of iterations to be performed
            __centroids:
                The centroids of the clusters formed
            __previousCentroids:
                The centroids of the clusters formed in the previous iteration
            __clusters:
                The clusters formed
            __indicesTable:
                A dictionary that keeps track of the indices of the tweets that have been assigned to a centroid
            __iterationCount:
                The number of iterations performed
            __sse:
                The sum of squared errors of the clusters formed


        Example:
        --------
            >>> tweets = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]

             >>> kmeans = KMeans(clustersCount=2)
             >>> kmeans.fit(tweets)
             >>> centroids = kmeans.getCentroids()
             >>> clusters = kmeans.getClusters()
             >>> sse = kmeans.getSSE()

    '''
    
    def __init__(self, clustersCount=4, maxIterations=50):
        self.__clustersCount = clustersCount
        self.__maxIterations = maxIterations
        self.__centroids = []
        self.__previousCentroids = []
        self.__clusters = {}
        self.__indicesTable = {}
        self.__iterationCount = 0
        self.__sse = 0

    def fit(self, tweets: List[List[str]]) -> None:
        '''
            This method takes a list of tweets as input and performs k-means clustering on it

            Parameters:
            -----------
                tweets:
                    A list of tweets represented as a list of lists of strings

            Returns:
            --------
                None

            Example:
            --------

                >>> tweets = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]

                >>> kmeans = KMeans(clustersCount=2)
                >>> kmeans.fit(tweets)
        '''
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
        '''
            This method checks if k-means converged

            Parameters:
            -----------
                None

            Returns:
            --------
                True if converged, False otherwise

            Example:
            --------

                >>> tweets = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]

                >>> kmeans = KMeans(clustersCount=2)
                >>> kmeans.fit(tweets)
                >>> kmeans.__isConverged()
                True
        '''
        if len(self.__centroids) == 0:
            return False

        for index, centroid in enumerate(self.__centroids):
            if centroid != self.__previousCentroids[index]:
                return False
        return True


    def __assignCluster(self, tweets: List[List[str]]):
        '''
            This method assigns tweets to the closest centroids

            Parameters:
            -----------
                tweets:
                    A list of tweets represented as a list of lists of strings

            Returns:
            --------
                None
        '''
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
        '''
            This method updates the centroids based on the clusters formed

            Parameters:
            -----------
                None

            Returns:
            --------
                None
        '''
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

    def __getDistance(self, tweet1: list[List[str]], tweet2: list[List[str]]) -> float:
        '''
            This method calculates the distance between two tweets

            Parameters:
            -----------
                tweet1:
                    A list of strings representing a tweet

                tweet2:
                    A list of strings representing a tweet

            Returns:
            --------
                The distance between the two tweets

            Example:
            --------

                >>> tweets = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]

                >>> kmeans = KMeans(clustersCount=2)
                >>> kmeans.fit(tweets)
                >>> kmeans.__getDistance(tweets[0], tweets[1])
                1.0
        '''
        # return the jaccard distance
        return 1 - (len(set(tweet1).intersection(tweet2)) / len(set().union(tweet1, tweet2)))

    def getSSE(self):
        '''
            This method calculates the sum of squared errors

            Parameters:
            -----------
                None

            Returns:
            --------
                The sum of squared errors

            Example:
            --------

                >>> tweets = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]

                >>> kmeans = KMeans(clustersCount=2)
                >>> kmeans.fit(tweets)
                >>> kmeans.getSSE()
                0.0
        '''
        if self.__sse == 0:
            self.__calculateSSE()
        return self.__sse

    def __calculateSSE(self):
        for cluster in self.__clusters.keys():
            for tweet in self.__clusters[cluster]:
                self.__sse += tweet[1] ** 2

    def getCentroids(self):
        return self.__centroids

    def getClusters(self):
        return self.__clusters
