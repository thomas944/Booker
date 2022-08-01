# Booker
Search for a book to find out more about it 



imports needed:
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import nltk
from wordcloud import WordCloud as wc




functions.best('positive')  #negative/positive, finds and prints the most neg/pos paragraph in book

functions.showPercentage()  #creates bar graph with percentage of negative,neutral,and positive words
![summary](https://user-images.githubusercontent.com/72369993/182254435-3788c6b1-c72a-4585-bce8-3673b6ad3c52.PNG)



functions.happinessOverTime()  #creates scatter plot of each sentence in book
![hot](https://user-images.githubusercontent.com/72369993/182254452-c48e9a36-4983-4bd4-b7d7-588cb5531cc1.PNG)



functions.wordCloud('positive')   #negative/positive, creates word cloud using frequency of negative/positive words
![wc](https://user-images.githubusercontent.com/72369993/182254407-717dcc68-6459-4adc-975c-bcda3820b0c0.PNG)

