import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import whois
from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings()
from urllib3 import request
from csv import writer

def is_registered(domain_name):
    """A function that returns a boolean indicating whether a `domain_name` is registered"""
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return w.domain_name, w.creation_date, w.expiration_date

openPhishURL="https://www.openphish.com/"
openPhishSoup = BeautifulSoup(requests.get(openPhishURL).content,'html.parser')
df = pd.read_csv("data.csv", index_col=0)
count2= len(df['URL'])
for tr in openPhishSoup.findAll('td',class_= "url_entry"):
  url = tr.text
  if(url not in list(df['URL'])):
    w = is_registered(url)
    if (w and w[0]!=None):
      try :
        page = requests.get(url, verify=False, timeout=15)
        soup = BeautifulSoup(page.content, 'html.parser')
        if (page and page.status_code == 200 and soup):
          df.loc[count2, 'URL'] = url
          fileName = "f"+str (count2)+'.html'
          df.loc[count2, 'Filename'] = fileName
          my_data_file = open(fileName, 'w')
          my_data_file.writelines("<!-- URL ="+url+"-->")
          my_data_file.writelines("<!-- w ="+str (w)+"-->")
          my_data_file.writelines(str (soup.prettify()))
          my_data_file.close()
          count2+=1
      except requests.exceptions.RequestException:
        continue

print("Success")
df.to_csv("data.csv")
