import random
import time
import numpy as np
import DAO
import display


class Clustering():
    def __init__(self, cursor, connexion, windowSize, numberCentroid):
        self.windowSize = windowSize
        self.connexion = connexion
        self.cursor = cursor
        self.dict = DAO.get_dict(self.cursor)

        self.matrix = DAO.get_matrix(self.cursor)

        self.posCentroid = []

        for word in range(numberCentroid):
            randomWord = random.randint(0, len(self.dict) // 2)
            self.posCentroid.append(self.matrix[randomWord])

    def mainClustering(self, t, k, n):
        ligneCount = len(self.matrix)
        wordAndCentroid = np.zeros(ligneCount, dtype=int)
        iterationCount = 0
        changeCount = []
        executionTimes = []
        wordCountPerCentroid = []
        while True:
            loopStart = time.time()
            wordAndCentroid, nb = self.centroidAssignment(k, wordAndCentroid)
            changeCount.append(nb)
            self.posCentroid, decompte = self.centroidRecalculation(wordAndCentroid, k)
            wordCountPerCentroid.append(decompte)
            iterationCount += 1
            executionTimes.append(time.time() - loopStart)

            if changeCount[iterationCount - 1] == 0:
                break

        self.output = display.Output(t, k, n)
        self.output.sortieIteration(iterationCount, changeCount, wordCountPerCentroid, executionTimes)
        self.findWordsCloseToCentroid(n, k)
        self.output.closeFile()

    def distance(self, u, v):
        return np.sum((u - v) ** 2)

    def centroidAssignment(self, k, wordAndCentroid):
        wordAndCentroidTemp = np.zeros(len(self.matrix), dtype=int)
        for i in range(len(self.matrix)):
            scores = [self.distance(self.matrix[i], self.posCentroid[j]) for j in range(k)]
            centroid = scores.index(min(scores))
            wordAndCentroidTemp[i] = centroid
        changeCount = np.sum(np.not_equal(wordAndCentroid, wordAndCentroidTemp))

        return wordAndCentroidTemp, changeCount

    def centroidRecalculation(self, wordAndCentroid, k):
        centroid = np.zeros((k, len(self.matrix)))
        count = np.zeros(k)
        for i in range(len(self.matrix)):
            centroid[wordAndCentroid[i]] += self.matrix[i]
            count[wordAndCentroid[i]] += 1

        for i in range(k):
            if count[i] > 0:
                centroid[i] /= count[i]

        return centroid, count

    def findWordsCloseToCentroid(self, n, k):
        groups = [[] for i in range(k)]

        for word, index in self.dict.items():
            scores = [self.distance(self.matrix[index - 1], self.posCentroid[j]) for j in range(k)]
            scoreMin = min(scores)
            centroid = scores.index(scoreMin)
            groups[centroid].append((scoreMin, word))

        for i in range(k):
            groups[i] = sorted(groups[i])

        self.output.outputCentroid(groups)
