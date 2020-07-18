# Form a table of all universities in India, source: wikipedia

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# central universities 
url_1 = r"https://en.wikipedia.org/wiki/Central_university_(India)"

resp = requests.get(url_1)
if resp.status_code != 200:
    print('Error in loading the page')
else:
    print('Successfully loaded the page')
    soup = BeautifulSoup(resp.text,'html.parser')
    l1 = soup.find_all('tbody')
    lr = l1[1].find_all('tr')
    len_r = len(lr)
    lh = lr[0].find_all('th')
    col_names = [re.search(r'[A-z]+.+', item.text)[0] 
                                            for item in lh]
    dat = pd.DataFrame(columns = col_names)
    for i in range(1,len_r):
        lc = lr[i].find_all('td')
        len_c = len(lc)
        for j in range(len_c):
            try:
                dat.loc[i-1,col_names[j]] = re.split(r'[\[(\])]',
                       re.search(r'[A-z]+.+|[0-9]+.',
                                 lc[j].text)[0])[0].strip()
            except TypeError:
                dat.loc[i-1,col_names[j]] = 0

# autonomous institutes
url_2 = "https://en.wikipedia.org/wiki/ \
        List_of_autonomous_higher_education_institutes_in_India"

resp = requests.get(url_2)
if resp.status_code != 200:
    print('Error in loading the page')
else:
    print('Successfully loaded the page')
    soup = BeautifulSoup(resp.text,'html.parser')
    l1 = soup.find('tbody')
    lr = l1.find_all('tr')
    len_r = len(lr)
    lh = lr[0].find_all('th')
    col_names = [re.search(r'[A-z]+.+', item.text)[0] 
                                            for item in lh]
    dat_a = pd.DataFrame(columns = col_names)
    for i in range(1,len_r):
        lc0 = lr[i].find('th')
        dat_a.loc[i-1,col_names[0]] = re.search(
                                r'[A-z]+.+',lc0.text)[0]
        lc1 = lr[i].find_all('td')
        len_c = len(lc1)
        if len_c == len(col_names)-1:
            j_a = 0
        else:
            j_a = 1
        for j in range(1,len_c+1):
            try:
                dat_a.loc[i-1,col_names[j+j_a]] = re.split(r'[\[(\])]',
                         re.search(r'[A-z]+.+|[0-9]+.',
                                   lc1[j-1].text)[0])[0].strip()
            except TypeError:
                dat_a.loc[i-1,col_names[j+j_a]] = 0
                
dat_a.loc[:,'State'] = dat_a.loc[:,'State'].fillna(method = 'ffill')
dat_a = dat_a.rename(columns = {'Institute': 'University'})

cols = ['University','State','Location','Specialization','Established']
dat_f = dat[cols].append(dat_a[cols])
dat_f = dat_f.sort_values(by = ['University'])

dat_f.to_csv(r"C:\Users\JJ\Desktop\Data Science Projects\Indian_Univ_Rank\univ_data.csv", 
             index = False, header=True)