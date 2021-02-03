import operator
import numpy as np

class distanceCalculation():
    def __init__(self, matrix, dict, word, numberSynonyms):
        self.matrix = matrix
        self.dict = dict
        self.word = word
        self.numberSynonyms = numberSynonyms



    def leastSquareCalculation(self):
        sortedDict = []
        try:
            wordIndex = operator.itemgetter(self.word)(self.dict)

            wordVector = self.matrix[wordIndex]
            score = []

            keyList = list(self.dict.keys())

            for i in range(len(self.matrix)):
                if i != wordIndex:
                    comparatorVector = self.matrix[i]
                    sumDifference = np.sum((wordVector - comparatorVector) ** 2)
                    score.append(sumDifference)

            wordScoreDict = {}
            for key in keyList:
                for value in score:
                    if key != self.word:
                        wordScoreDict[key] = value
                        score.remove(value)
                        break
                    else:
                        wordScoreDict[key] = 0
                        break
            sortedDict = sorted(wordScoreDict.items(), key=operator.itemgetter(1), reverse=False)
        except:
            sortedDict =[]

        return sortedDict


    def scalarProductsCalculation(self):
        try:
            wordIndex = operator.itemgetter(self.word)(self.dict)
            wordVector = self.matrix[wordIndex]
            score = []
    
            keyList = list(self.dict.keys())
    
            for i in range(len(self.matrix)):
                if i != wordIndex:
                    comparatorVector = self.matrix[i]
                    sumDifference = np.dot(wordVector, comparatorVector)
                    score.append(sumDifference)
            wordScoreDict = {}
            for key in keyList:
                for value in score:
                    if key != self.word:
                        wordScoreDict[key] = value
                        score.remove(value)
                        break
                    else:
                        wordScoreDict[key] = 0
                        break
            sortedDict = sorted(wordScoreDict.items(), key=operator.itemgetter(1), reverse=True)
        except:
            sortedDict = []
            
        return sortedDict

    def cityBlockCalculation(self):
        try:
            indexMot = operator.itemgetter(self.word)(self.dict)
            wordVector = self.matrix[indexMot]
            score = []

            keyList = list(self.dict.keys())

            for i in range(len(self.matrix)):
                if i != indexMot:
                    comparatorVector = self.matrix[i]
                    sumDifference = np.sum(np.absolute(wordVector - comparatorVector))
                    score.append(sumDifference)

            wordScoreDict = {}
            for key in keyList:
                for value in score:
                    if key != self.word:
                        wordScoreDict[key] = value
                        score.remove(value)
                        break
                    else:
                        wordScoreDict[key] = 0
                        break
            sortedDict = sorted(wordScoreDict.items(), key=operator.itemgetter(1), reverse=False)
        except:
            sortedDict = []

        return sortedDict

