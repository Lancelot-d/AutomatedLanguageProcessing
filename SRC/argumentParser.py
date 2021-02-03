import argparse
class argParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-e",action="store_true")
        self.parser.add_argument("-c",action="store_true")
        self.parser.add_argument("-r", action="store_true")
        self.parser.add_argument("-t","-windowLength",type = int)
        self.parser.add_argument("-k","-Number of centroid",type = int)
        self.parser.add_argument("-n","-Number of word per centroid",type = int)
        self.parser.add_argument("--enc","-encode")
        self.parser.add_argument("--path","-path to text")
        self.args = self.parser.parse_args()


