# -*- coding: utf-8 -*-
"""
@author: raul
"""

import nltk
import os
import logging
from xml.dom.minidom import parse
import xml.dom.minidom

#globals
path = os.path.dirname(__file__)

def main():
    #InvertedIndexGenerator config file
    configFile = path+'/InvertedIndexGenerator/gli.cfg'
    #log
    log(path+'/InvertedIndexGenerator/invertedIndexGenerator.log')
    #process all data based on config file
    processData(configFile)
    
    
def processData(configFile):
    dictionary = {}
    invertedIndex = {}
    i=0
    directory = open(configFile, 'r')
    lines=[]
    
    #read filename from config file    
    for line in directory:
        line = line.strip().replace(" ","")
        lines.append(line.split('='))
        
        #read xml file and returns a dictionary
        if str(lines[i][0]) == 'LEIA':
            dictionary=readData(path+str(lines[i][1]))
            invertedIndex=invertedIndexGenerator(dictionary, [])
            #print(dictionary)    
        elif str(lines[i][0]) == 'ESCREVA':
            #test
            print (readData(path+str(lines[i-1][1])))
            #end test
            #writeData(dictionary)
            
        i+=1
     
    directory.close()
    print(invertedIndex)
 

def readData(filename):
    dictionary = {}
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    
    records = collection.getElementsByTagName("RECORD")
    
    for record in records:
        recordNumber = record.getElementsByTagName('RECORDNUM')[0].childNodes[0].data
        
        try:
            dictionary[recordNumber] = record.getElementsByTagName('ABSTRACT')[0].childNodes[0].data
        except IndexError:
            try:
                dictionary[recordNumber] = record.getElementsByTagName('EXTRACT')[0].childNodes[0].data
            except IndexError:
                print("Document["+recordNumber+"] don't have abstract neither extract. Going to the next!")
    
    return dictionary
    

def writeData():
    return 0        
    

def invertedIndexGenerator(dictionaries, stopWords):
    invertedIndex = {}
    
    for key in dictionaries.keys():
        for token in nltk.word_tokenize(dictionaries[key]):
            tokenList = []
            if token not in stopWords:
                try:
                    invertedIndex[token].append(key)
                    invertedIndex.update({token:invertedIndex[token]})
                except KeyError:
                    tokenList.append(key)
                    invertedIndex.update({token:tokenList})
                    
    return invertedIndex

    
def log(logFile):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler(logFile)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info('Logging iniated')

                      
main() 