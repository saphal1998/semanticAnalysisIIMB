#  Input : Text of all annual reports in PDF ; Output : This file averages the emotional rating of all the sentences of a particular aspect (Eg : 'risk', 'investment', 'entrepreneurship' etc.)for a particular company.

# Imports
from math import *
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
# To extend this to other companies, add the company name (without spaces) in the '2001' worksheet of the excel workook 'CompanyList.xlsx'
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

company_df_calc = pd.DataFrame(np.zeros((rows, cols)), index=namesOfCompanies, columns=words)
word_count = pd.DataFrame(np.zeros((rows, cols)), index=namesOfCompanies, columns=words)
company_df_final = pd.DataFrame(np.zeros((rows, cols)), index=namesOfCompanies, columns=words)


# Doing complete company analysis of emotions in a numeric way

for company in namesOfCompanies:
    os.chdir(company)
    print("Company being processed right now is: ", company, "and the current directory is: ", os.getcwd())
    files = getFiles(os.getcwd())
    print("Files found for the company are: ", files)
    company_text = ''
    for file in files:
        # To add more years of data, add it to the list below.
        if file in ['2001.pdf', '2005.pdf', '2009.pdf']:
            company_text += extract_txt(file)
    company_text = company_text.encode('utf-8', 'ignore')
    sentences = sent_tokenize(company_text)
    print("Number of sentences found on combining all the documents are: ", len(sentences))
    for sent in sentences:
        scores = analyzer.polarity_scores(sent)
        # As Vader considers punctuation and capitalisation, convert to lower only after calculating sentiment score
        sentence = sent
        sent = sent.lower()
        for word in words:
            if synonyms[word].any() in sent:
                company_df_calc[word][company] += scores["compound"]
                word_count[word][company] += 1
    print(company, " has been processed! Changing directory to original directory!")
    os.chdir(current_dir)

for company in company_df_calc.index:
    for word in company_df_calc.columns:
        if word_count[word][company] != 0:
            company_df_final[word][company] = company_df_calc[word][company] / word_count[word][company]


# Saving files as CSV
company_df_calc.to_csv("EmotionCount.csv", encoding='utf-8')
word_count.to_csv("WordCount.csv", encoding='utf-8')
company_df_final.to_csv("FinalSummaryOfEmotions.csv", encoding='utf-8')
