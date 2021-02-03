class Display():

    def inputUser(self):
        print("\nEnter a word, the number of synonyms you want and the method of distanceCalculation,\n")
        print("i.e. scalar product  :0, least-squares: 1, city-block: 2 \n")
        print("\nType q to exit.\n")
        answer = input("")
        print("\n")
        answerArray = answer.split(" ")
        return answerArray

    def resultDisplay(self, length, dict, stopList, word):
    
        i = 0
        for key, value in dict:
            if i < length and key not in stopList and key not in word and value>0 :
                print(f'{key} --> {value}\n')
                i+=1

        if i ==0:
            print("no synonym at this window length")

class Output():

    def __init__(self,t,k,n):
        self.windowLength = t
        self.clusterCount = k
        self.wordCount = n
        path = "../Output/"
        fileName = path + "answer_t" + str(self.windowLength) + "_k" + str(self.clusterCount) + "_n" + str(self.wordCount) + ".txt"
        self.file = open(fileName, "w", encoding="utf8")


    def sortieIteration(self, iterationCount, changeCount, wordCountPerCentroid, executionTime):
        for iteration in range(iterationCount):
            stringPresentation = "\n=================================================="
            self.file.write(stringPresentation)
            stringIteration = "\nIteration " + str(iteration) +"\n"
            self.file.write(stringIteration)
            stringInfo = str(changeCount[iteration]) + " cluster changes in " + str(executionTime[iteration]) + " seconds.\n\n"
            self.file.write(stringInfo)
            for centroid in range(self.clusterCount):
                stringCentroide = "There are " + str(wordCountPerCentroid[iteration][centroid]) + \
                                  " points (words) grouped around the centroid no. " + str(centroid) + ".\n"
                self.file.write(stringCentroide)

    def outputCentroid(self, wordScores):
        stringPresentation = "\n******************************************************"
        self.file.write(stringPresentation)

        for i in range(len(wordScores)):
            stringGroupe = "\nGroup " + str(i) + "\n\n"
            self.file.write(stringGroupe)
            for score, word in wordScores[i][:self.wordCount]:
                stringWord = word + " --> " + str(score) + "\n"
                self.file.write(stringWord)

    def closeFile(self):
        self.file.close()


