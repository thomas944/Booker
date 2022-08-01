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

def getData(bookName):
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  driver.get("https://www.gutenberg.org/ebooks/")

  driver.implicitly_wait(5)

  try:
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "book-search"))
    )
    element.clear()
    element.send_keys(bookName)
    element.send_keys(Keys.RETURN)
      
    element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "booklink"))
    ) 
    element.click()

    element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "link"))
    )
    element.click()
      
    chapters = driver.find_elements(By.CLASS_NAME,"chapter")

    myFile = open("temp.txt", "a")
    print(type(chapters))
    i = 0
    while(i<len(chapters)):
      myFile.write(chapters[i].text)
      i+=1
      
      
    myFile.close()
    
  finally:
    driver.quit()

def createDF():
  sia = SIA()
  results = []
  
  myFile = open("temp.txt", "r")
  for paragraph in myFile:
    if(paragraph.find("Chapter") != -1):
      continue 
    pol_score = sia.polarity_scores(paragraph)
    pol_score['paragraph'] = paragraph
    results.append(pol_score)
     
  df = pd.DataFrame.from_records(results)
  df['label'] = 0
  df.loc[df['compound'] > 0.2, 'label'] = 1
  df.loc[df['compound'] < -0.2, 'label'] = -1
  df.to_csv('book.csv', encoding='utf-8')
  return df

def showPercentage():
  df = pd.read_csv('book.csv')
  print(df.label.value_counts(normalize=True) * 100)

  fig, ax = plt.subplots(figsize=(8, 8))
  counts = df.label.value_counts(normalize=True) * 100

  sns.barplot(x=counts.index, y=counts, ax=ax)

  ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
  ax.set_ylabel("Percentage")
  plt.show()

def process_text(sentence):
  tokenizer = tokenizer = RegexpTokenizer(r'\w+')
  stop_words = stopwords.words('english')
  lowercase = sentence.lower()
  toks = tokenizer.tokenize(lowercase)
  tokens = []
  for letter in toks :
    if letter not in stop_words:
      tokens.append(letter)

  return tokens


def best(choice):
  df = pd.read_csv('book.csv')
  if (choice == 'positive'):
    bestParagraph = (df['compound'].idxmax())
  else:
    bestParagraph = (df['compound'].idxmin())
  print(df.at[bestParagraph,'paragraph'])

def createDict(lines,n):
  tokens = []
  myDict = {}
  for line in lines:
    tokens.extend(process_text(line))
    freq = nltk.FreqDist(tokens)
    most_common = freq.most_common(n)
  for i in range(0,n):
    myDict.update({most_common[i][0]:most_common[i][1]})
  return myDict

def wordCloud(choice):
  _choice = ''
  if (choice == "positive"):
    _choice = 1
  else:
    _choice = -1  
  df = pd.read_csv('book.csv')
  lines = list(df[df.label == _choice].paragraph)
  tokens = []
  for line in lines:
    tokens.extend(process_text(line))
    

  freq = nltk.FreqDist(tokens)
  print(freq.most_common(20))
  myWordCloud = wc(background_color="white").generate_from_frequencies(createDict(lines,30))
  plt.imshow(myWordCloud, interpolation="bilinear")
  plt.axis("off")
  plt.show()

def happinessOverTime():
  df = pd.read_csv('book.csv')
  plt.figure(figsize=(12, 6))
  sns.scatterplot(data=df, y = df['compound'], x= df['compound'].index.values,hue=df['compound'].rename('rating'))
  plt.xlabel('sentence')
  plt.ylabel('rating')
  plt.show()


