import sys
import clustering
from traceback import print_exc
from argumentParser import argParser
import DAO
from training import Training
from distancecalculation import distanceCalculation
from display import Display
from os import path

DB = "..\DataBase\DB"

SCALAR_PRODUCT = "0"
LEAST_SQUARE = "1"
CITY_BLOCK = "2"

QUITTER ="q"


def main():
    try:
        argparser = argParser()
        trainingLaunch = argparser.args.e
        searchLaunch = argparser.args.r
        clusteringLaunch = argparser.args.c
        windowLength = argparser.args.t
        centroidCount = argparser.args.k
        wordCountPerCluster = argparser.args.n
        enc = argparser.args.enc
        textPath = argparser.args.path


        connexion, cursor = DAO.connect(DB)
        DAO.create_tables(cursor, path.exists(DB))


        training = Training(enc, textPath)

        if trainingLaunch == True:
            training.coach(connexion, cursor, windowLength)
            DAO.disconnect(connexion, cursor)

        elif searchLaunch == True:
            answer = " "
            while answer != QUITTER:
                input = Display().inputUser()

                if input[0]==QUITTER:
                    answer = QUITTER
                    sys.exit()

                calculation = distanceCalculation(DAO.get_matrix(cursor), DAO.get_dict(cursor), input[0], int(input[1]))

                if input[2] == SCALAR_PRODUCT:
                    result = calculation.scalarProductsCalculation()
                elif input[2] == LEAST_SQUARE:
                    result = calculation.leastSquareCalculation()
                elif input[2] == CITY_BLOCK:
                    result = calculation.cityBlockCalculation()

                Display().resultDisplay(int(input[1]), result, training.stopList, input[0])
        elif clusteringLaunch == True:
            cluster = clustering.Clustering(cursor,connexion,windowLength,centroidCount)
            cluster.mainClustering(windowLength, centroidCount, wordCountPerCluster)

    except:
        if answer != QUITTER:
            print_exc()
        pass

if __name__ == "__main__":
    quit(main())