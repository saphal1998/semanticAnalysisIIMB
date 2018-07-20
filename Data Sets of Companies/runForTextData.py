# Imports
from functions import *
from listofwords import *
import textract
import os
import datetime
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import glob
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Declaration of Objects

analyzer = SentimentIntensityAnalyzer()
current_dir = os.getcwd()
print("Current directory is: ", current_dir)
CompanyData = pd.ExcelFile(current_dir + '/Company List.xlsx')
aspects = pd.read_excel(CompanyData, '2001', skiprows=0)
# print("Aspects are : ", aspects.columns)
namesOfCompanies = list(aspects['Companies'])
namesOfCompanies = [str(x) for x in namesOfCompanies]
print("Names of Companies are: ", namesOfCompanies)
words = [str(x) for x in list(aspects.columns[1:])]
synonyms.columns = words
print("Words to be examined are: ", words)
years = ['2001', '2005', '2009']
rows = len(namesOfCompanies)
cols = len(words)

company_df = pd.DataFrame(np.empty((rows, cols), dtype=str), index=namesOfCompanies, columns=words)
sentence_rating = pd.DataFrame(np.empty((rows, cols), dtype=str), index=namesOfCompanies, columns=words)

for company in namesOfCompanies:
    os.chdir(company)
    print("Company being processed right now is: ", company, "and the current directory is: ", os.getcwd())
    files = getFiles(os.getcwd())
    print("Files found for the company are: ", files)
    company_text = ''
    for file in files:
        if file == '2001.pdf' or file == '2005.pdf' or file == '2009.pdf':
            company_text += extract_txt(file)
    company_text = company_text.encode('utf-8', 'ignore')
    sentences = sent_tokenize(company_text)
    print("Number of sentences found on combining all the documents are: ", len(sentences))
    for sent in sentences:
        scores = analyzer.polarity_scores(sent)
        sentence = sent
        sent = sent.lower()
        for word in words:
            if (synonyms[word].any() in sent) and len(sent) > 10:
                company_df[word][company] += ('<begin>' + sentence + '<end>')
                sentence_rating[word][company] += ('<begin>' + str(scores["compound"]) + '<end>')
    print(company, " has been processed! Changing directory to original directory!")
    os.chdir(current_dir)


company_df.to_csv("CompanySentences.csv")
sentence_rating.to_csv("SentenceRating.csv")
