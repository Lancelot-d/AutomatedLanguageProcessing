import re
import DAO

class Training():

    def __init__(self, encode, path):
        self.path = path
        self.encode = encode
        self.stopListPath = "..\Text\stopListe.txt"
        self.readStopList()

    def readText(self):
        
        with open(self.path, 'r', encoding=self.encode) as f:
            self.text = re.findall(r'\w+', f.read().lower())

    def readStopList(self):
        with open(self.stopListPath, 'r', encoding=self.encode) as f:
            self.stopList = re.findall(r'\w+', f.read().lower())


    def createDict(self, connexion, cursor):
        self.res_list = []
        for i in range(len(self.text)):
            if self.text[i] not in self.res_list:
                self.res_list.append(self.text[i])
        self.dict = {self.res_list[i]: i for i in range(0, len(self.res_list))}
        DAO.insert_dict(connexion, cursor, self.dict)

    def coach(self, connexion, curseur, fenetre):
        self.readText()
        self.createDict(connexion, curseur)
        DAO.insert_coocurrence(connexion, curseur, self.text, self.dict, fenetre)
        DAO.insert_lengthInfo(connexion, curseur)