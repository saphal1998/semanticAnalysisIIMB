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
CompanyData = pd.ExcelFile('/Users/saphalpatro/Desktop/Data Sets of Companies/Company List.xlsx')
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
    for file in files:
        company_text = ''
        if file in ['2001.pdf', '2005.pdf', '2009.pdf']:
            company_df = pd.DataFrame(np.empty((rows, cols), dtype=str), index=namesOfCompanies, columns=words)
            sentence_rating = pd.DataFrame(np.empty((rows, cols), dtype=str), index=namesOfCompanies, columns=words)
            company_text += extract_txt(file)
            company_text = company_text.encode('utf-8', 'ignore')
            sentences = sent_tokenize(company_text)
            print("Number of sentences found in", file, company, "combining all the documents are: ", len(sentences))
            for sent in sentences:
                scores = analyzer.polarity_scores(sent)
                sentence = sent
                sent = sent.lower()
                for word in words:
                    if (synonyms[word].any() in sent) and len(sent) > 10:
                        company_df[word][company] += ('<begin>' + sentence + '<end>')
                        sentence_rating[word][company] += ('<begin>' + str(scores["compound"]) + '<end>')
            os.chdir(current_dir + '/Results')
            company_df.to_csv((file[:4] + company + 'Sentences.csv'))
            sentence_rating.to_csv((file[:4] + company + 'SentenceRating.csv'))
            os.chdir(current_dir + '/' + company)
    print(company, " has been processed! Changing directory to original directory!")
    os.chdir(current_dir)
