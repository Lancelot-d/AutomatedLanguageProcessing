import sqlite3
import numpy as np
import operator


PRAGMAFK = 'PRAGMA foreign_keys = 1'

CREATE_DB_MATRIX = '''
CREATE TABLE IF NOT EXISTS coocurrence
(
	id_word INT NOT NULL,
	id_coocurrence  INT NOT NULL,
	windowLength  INT NOT NULL,
	frequency INT NOT NULL,
	PRIMARY KEY(id_word,id_coocurrence,windowLength)
)
'''
CREATE_DB_DICT = '''
CREATE TABLE IF NOT EXISTS dict
(
	word CHAR(25) NOT NULL,
	id INT NOT NULL
)
'''

CREER_BD_LengthInfo = '''
CREATE TABLE IF NOT EXISTS LengthInfo 
(
	LengthInfo INT NOT NULL
)
'''


INSERT_coocurrence = 'INSERT INTO coocurrence VALUES (?,?,?,?)'
INSERT_dict = 'INSERT INTO dict VALUES (?,?)'
INSERT_LengthInfo= 'INSERT INTO LengthInfo VALUES (?)'

UPDATE_coocurrence = 'UPDATE coocurrence SET frequency=(?) WHERE(id_word =(?) AND id_coocurrence =(?) AND windowLength =(?))'
UPDATE_LengthInfo = 'UPDATE LengthInfo SET LengthInfo=(?)'

SELECT_coocurrence = 'SELECT * FROM coocurrence'
SELECT_dict ='SELECT * FROM dict'
SELECT_id = 'SELECT id FROM dict WHERE id=?'
SELECT_id_word = 'SELECT id_word FROM coocurrence WHERE id_word=?'
SELECT_LengthInfo = 'SELECT LengthInfo FROM LengthInfo'


INDEX_id_word ='CREATE INDEX index_word ON coocurrence(id_word)'
INDEX_id_coocurrence = 'CREATE INDEX index_coocurrence ON coocurrence(id_coocurrence)'
INDEX_windowLength = 'CREATE INDEX index_windowLength ON coocurrence(windowLength)'
INDEX_frequency = 'CREATE INDEX index_frequency ON coocurrence(frequency)'


def disconnect(connexion, cursor):
    cursor.close()
    connexion.close()

def connect(bd):
    connexion = sqlite3.connect(bd)
    cursor = connexion.cursor()
    cursor.execute(PRAGMAFK)
    return connexion, cursor

def create_tables(cursor,dbExist):
    cursor.execute(CREATE_DB_DICT)
    cursor.execute(CREATE_DB_MATRIX)
    cursor.execute(CREER_BD_LengthInfo)

    if not dbExist:
        cursor.execute(INDEX_id_word)
        cursor.execute(INDEX_id_coocurrence)
        cursor.execute(INDEX_windowLength)
        cursor.execute(INDEX_frequency)


def insert_dict(connexion, cursor, dict):
    cursor.execute(SELECT_dict)
    dictDB = {}
    for word, id in cursor.fetchall():
        dictDB[word] = id

    for word in dict:
        if word not in dictDB:
            dictDB[len(dictDB) + 1] = word
            cursor.execute(INSERT_dict, (word, len(dictDB),))

    connexion.commit()


def insert_coocurrence(connexion, cursor, text, dict, windowLength):
    dictCoocurrenceBD = {}
    cursor.execute(SELECT_coocurrence)
    for id_word, id_coocurrence, windowLength,frequency in cursor.fetchall():
        dictCoocurrenceBD[(id_word,id_coocurrence,windowLength)]=frequency
    dictCoocurrence = {}

    for i in range(len(text)):
        minT = int(np.floor(windowLength / 2))
        maxT = int(np.ceil(windowLength / 2))
        middle = int(np.floor(windowLength / 2))

        while i < minT:
            minT = i
            middle = i
        while i > (len(text) - maxT):
            maxT -= 1

        listWindow = text[i - minT:i + maxT]
        index = operator.itemgetter(*listWindow)(dict)

        if type(index) is not int:
            indexList = list(index)
            actualIndex = indexList[middle]
            del indexList[middle]
            for k in indexList:
                if (actualIndex, k, windowLength) not in dictCoocurrence:
                    dictCoocurrence[(actualIndex, k, windowLength)] = 1
                else:
                    dictCoocurrence[(actualIndex, k, windowLength)] += 1

    for i in dictCoocurrence:
        id_word = i[0]
        id_coocurrence = i[1]
        windowLength = i[2]
        frequency = dictCoocurrence[i]

        if (id_word, id_coocurrence, windowLength) in dictCoocurrenceBD:
            cursor.execute(UPDATE_coocurrence,(frequency, id_word,id_coocurrence,windowLength,))
        else:
            cursor.execute(INSERT_coocurrence,(id_word,id_coocurrence,windowLength,frequency,))

    connexion.commit()


def insert_lengthInfo(connexion, cursor):
    cursor.execute(SELECT_dict)
    dict = cursor.fetchall()
    LengthInfo = len(dict)

    cursor.execute(SELECT_LengthInfo)
    LengthInfoEnBD = cursor.fetchall()

    if len(LengthInfoEnBD)==0 :
        cursor.execute(INSERT_LengthInfo,(LengthInfo,))
    elif LengthInfoEnBD != LengthInfo:
        cursor.execute(UPDATE_LengthInfo,(LengthInfo,))

    connexion.commit()

def get_matrix(cursor):
    cursor.execute(SELECT_LengthInfo)
    LengthInfo = cursor.fetchall()

    if len(LengthInfo)!=0:
        LengthInfo= LengthInfo[0][0]

    matrix = np.zeros((LengthInfo, LengthInfo), dtype=np.int8)

    cursor.execute(SELECT_coocurrence)

    for word, coocurrence, windowLength, frequency in cursor.fetchall():
        if windowLength == windowLength:
            matrix[word][coocurrence]=frequency

    return matrix

def get_dict(cursor):
    cursor.execute(SELECT_dict)
    dict = {}
    for word, id in cursor.fetchall():
        dict[word] = id

    return dict
