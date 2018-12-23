import os
import numpy as np
import pandas as pd
import glob
import textract


def getstring(list):
    mes = ''
    for i in range(len(list)):
        mes += (str(list[i]) + ' ')
    return mes


def iscomp(list, comp):
    for i in range(len(list)):
        if list[i] in comp:
            return True
    return False


def listtoString(list):
    string = ''
    for i in range(len(list)):
        if str(type(list[i])) == "<type 'NoneType'>" or len(list[i]) <= 0:
            continue
        elif len(list[i]) > 1 or str(type(list[i])) == "<type 'list'>":
            for j in range(len(list[i])):
                string += (str(list[i][j]) + ' ')
        else:
            string += (str(list[i]) + ' ')
    return string


def getWords(list):
    words = []
    for i in range(len(list)):
        words.append(list[i][0])
    return words


def getFiles(dir):
    os.chdir(dir)
    fn = []
    for file in glob.glob("*.pdf"):
        fn.append(file)
    for file in glob.glob("*.txt"):
        fn.append(file)
    return fn


def extract_txt(file):
    txt = ''
    try:
        txt = textract.process(file).decode()
        print ('File ', file, 'was extracted!')
    except:
        print ('File ', file, 'cannot be extracted! - skipped')
    return txt
