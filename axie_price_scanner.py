import pandas as pd
import numpy as np
import requests

from lxml import html
from lxml.cssselect import CSSSelector

# Create the web driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import sys
#sys.path.insert(0,'d:\d_workspace\axieinfinity\axie-infinity-leaderboard-axie-scraper')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome('d:/d_workspace/axieinfinity/axie-infinity-leaderboard-axie-scraper/chromedriver',options=chrome_options)



###########################
urls = [
  # Reptile
  "https://axie.zone/finder?search=class:reptile;part:tail-iguana,horn-scaly-spoon,back-bone-sail,mouth-tiny-turtle;view_genes",
  "https://axie.zone/finder?search=class:reptile;part:tail-iguana,horn-scaly-spoon,back-bone-sail,mouth-kotaro;view_genes",
  "https://axie.zone/finder?search=class:reptile;part:tail-iguana,horn-scaly-spoon,back-bone-sail,mouth-razor-bite;view_genes",
  # Beast
  "https://axie.zone/finder?search=class:beast;part:mouth-nut-cracker,horn-imp,back-ronin,tail-nut-cracker;purity:6;view_genes",
  # Plant
  "https://axie.zone/finder?search=class:plant;part:mouth-serious,horn-cactus,back-pumpkin,tail-carrot;purity:6;view_genes"
]

response = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
ETH_PRICE = int(response.json()['USD'])

selling_axies = []
for url in urls:
  driver.get(url)
  driver.implicitly_wait(20)

  found = '-'
  while (found == '-'):
    search_result_count = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search_result_count")))
    found = search_result_count[0].text
  print("Axies found: ", found)
  page = round(int(found) / 12)
  if (page > 2):
    page = 2

  for i in range(page):
    paged_url = url + ";page:%d" % (i+1)
    print(paged_url)
    driver.get(paged_url)
    driver.implicitly_wait(20)
    try:
      search_result_wrappers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search_result_wrapper>a")))

      for idx, link in enumerate(search_result_wrappers):
        selling_axie = { 
          'Marketplace' : '',
          'ETH' : '',
          'USD' : '',
          'Class' : '',
          'Breed' : '',
          'Nrg' : '',
          'Atk' : '',
          'Def' : '',
          'Pureness' : '',
          'Eyes' : '',
          'Ears' : '',
          'Back' : '',
          'Mouth' : '',
          'Horn' : '',
          'Tail' : '',
          'Hp' : '',
          'Speed' : '',
          'Skill' : '',
          'Morale' : ''
        }
        # print(link.get_attribute("href"))
        selling_axie['Marketplace'] = link.get_attribute("href").split('?')[0] + ' '

        # print("ID = ", link.get_attribute("href").split('/')[4].split('?')[0])

        # print(link.get_attribute("class").split()[1].upper())
        selling_axie['Class'] = link.get_attribute("class").split()[1].capitalize()

        breed = link.find_element(By.CLASS_NAME,"subcaption")
        # print(breed.text)
        selling_axie['Breed'] = breed.text.split(':')[1]

        card_stats = link.find_element(By.CLASS_NAME, "card_stats")
        stats = card_stats.find_elements(By.TAG_NAME, 'span')
        for stat in stats:
          # print(stat.get_attribute('class').capitalize(), stat.text)
          selling_axie[stat.get_attribute('class').capitalize()] = stat.text

        tbl_genes = link.find_element(By.CLASS_NAME, "genes")
        tbody = tbl_genes.find_element(By.TAG_NAME, 'tbody')
        tr_parts = tbody.find_elements(By.TAG_NAME, 'tr')
        pure_cnt = 0
        for tr_part in tr_parts:
          if (tr_part.get_attribute('class') != ''):
            part          = tr_part.get_attribute('class')

            td_part       = tr_part.find_elements(By.TAG_NAME, 'td')[1]
            part_class    = td_part.get_attribute('class')
            part_name     = td_part.text

            # print(part.capitalize(), part_class, part_name)
            if (selling_axie['Class'] == part_class.capitalize()):
              pure_cnt += 1
            selling_axie[part.capitalize()] = '(' + part_class.capitalize() + ') ' + part_name
        if (pure_cnt == 6):
          selling_axie['Pureness'] = 'Pure'

        stats = link.find_element(By.CLASS_NAME, "stats")
        spans = stats.find_elements(By.TAG_NAME, 'span')
        for span in spans:
          # print(span.get_attribute('class').capitalize(), span.text)
          selling_axie[span.get_attribute('class').capitalize()] = span.text

        price = link.find_element(By.CLASS_NAME, "ui.teal.tag.label.price")
        price_eth = float(price.text.split()[1])
        price_usd = price_eth * ETH_PRICE
        # print(price_eth, "ETH = ", price_usd, "USD")
        selling_axie['ETH'] = round(price_eth, 5)
        selling_axie['USD'] = round(price_usd, 2)

        selling_axies.append(selling_axie)
    except TimeoutException:
      print("Element not properly loaded")

  selling_axies.append({ 
    'Marketplace' : '',
    'ETH' : '',
    'USD' : '',
    'Class' : '',
    'Breed' : '',
    'Nrg' : '',
    'Atk' : '',
    'Def' : '',
    'Pureness' : '',
    'Eyes' : '',
    'Ears' : '',
    'Back' : '',
    'Mouth' : '',
    'Horn' : '',
    'Tail' : '',
    'Hp' : '',
    'Speed' : '',
    'Skill' : '',
    'Morale' : ''
  }) 

# print(selling_axies)
# Convert the python list into a dataframe
df_res = pd.DataFrame(selling_axies)
df_res.head()

# Export the dataframe into a csv file
df_res.to_csv("selling_axies.csv", index=False)