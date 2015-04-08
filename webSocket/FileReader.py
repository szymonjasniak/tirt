'''
Created on 4 kwi 2015

@author: SZYMON
'''
import time
import random

class FileReader:
    
    def __init__(self, fileName):
        self.myFileName = fileName
        self.lines = []
        
    def readLineByLineInFile(self):
        self.openFile()
        self.lines = self.myFile.readlines()
        
    def openFile(self):
        self.myFile = open(self.myFileName) 
        
    def printReadLineInGaussTime(self, mu, sigma):
        self.readLineByLineInFile()
        for line in self.lines:
            time.sleep(random.gauss(mu,sigma))
            return line
        
    def readLine(self, numberOfLine):
        self.readLineByLineInFile()
        return str(self.lines[numberOfLine])
        
        