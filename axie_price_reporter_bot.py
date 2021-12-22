#!/usr/bin/env python

import time

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

urls = [
  ### TEAM ELO 1500 200slp
  # Rep 1 stun >300
  "https://axie.zone/finder?search=class:reptile;part:tail-iguana,horn-scaly-spoon,back-bone-sail,mouth-tiny-turtle;view_genes",
  # Rep heal   >380
  "https://axie.zone/finder?search=class:reptile;part:tail-iguana,horn-scaly-spoon,back-bone-sail,mouth-razor-bite;view_genes",
  # Beast RIMP >185
  "https://axie.zone/finder?search=class:beast;part:mouth-nut-cracker,horn-imp,back-ronin,tail-nut-cracker;purity:6;view_genes",
  # Plant gain E>230
  "https://axie.zone/finder?search=class:plant;part:mouth-serious,horn-cactus,back-pumpkin,tail-carrot;view_genes",
  
  ### TEAM POISON BLACKMAIL 250slp 22tr5
  # Rep black mail   >330
  # "https://axie.zone/finder?search=class:reptile;part:mouth-tiny-turtle,horn-wing-horn,back-pigeon-post,tail-grass-snake;view_genes",
  # Rep counter crit >250
  # "https://axie.zone/finder?search=class:reptile;part:mouth-toothless-bite,horn-cerastes,back-hermit,tail-grass-snake;view_genes",
  # Plant poison steal E >340
  # "https://axie.zone/finder?search=part:mouth-herbivore,horn-leaf-bug,back-pumpkin,tail-yam;hp:59;speed:31;skill:31;morale:43;view_genes",

  # ### TEAM DUSK SERIOUS 220slp 19tr5
  # # Plant > 300
  # "https://axie.zone/finder?search=part:mouth-serious,horn-cactus,back-pumpkin,tail-cattail;hp:61;speed:31;skill:31;morale:41;view_genes",
  # # Dusk moc ko co hang
  # "https://axie.zone/finder?search=part:back-tri-spikes,mouth-tiny-turtle,horn-oranda,tail-snake-jar",
  # # Dusk hp 51 sp 45 $180
  # "https://axie.zone/finder?search=class:dusk;part:mouth-serious,horn-lagging,back-snail-shell,tail-thorny-caterpillar;hp:51;speed:45;view_genes",

  # Plant max E gain > ~300
  "https://axie.zone/finder?search=part:mouth-serious,horn-leaf-bug,back-pumpkin,tail-carrot;hp:59;speed:31;skill:31;morale:43;view_genes",
  
  ### PURE 
  # Bird Risky feather >230
  # "https://axie.zone/finder?search=class:bird;part:mouth-little-owl,horn-eggshell,back-pigeon-post,tail-post-fight;purity:6;view_genes",
  # Standard >290
  # "https://axie.zone/finder?search=class:bird;part:mouth-little-owl,horn-eggshell,back-pigeon-post,tail-post-fight;purity:6;view_genes"
  # Fish 
  # Rep
  # Plant
  # Beast
  # Bug
]

response = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
ETH_PRICE = int(response.json()['USD'])

import telebot
bot = telebot.TeleBot("1939855644:AAEj5LsBCUEJ31ON0ACDkDasfImBMqT_d9U")

def main() -> None:
  last_price = []
  for idx in range(len(urls)):
    last_price.append(1000)
  while (True):
    msg = ''
    for idx, url in enumerate(urls):
      driver.get(url)
      driver.implicitly_wait(20)
      
      try:
        # search_result_wrappers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search_result_wrapper>a")))
        search_result_wrapper = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search_result_wrapper>a")))
      
        link = search_result_wrapper
        # for link in search_result_wrapper:
        price = link.find_element(By.CLASS_NAME, "ui.teal.tag.label.price")
        price_eth = float(price.text.split()[1])
        price_usd = round(price_eth * ETH_PRICE, 2)
        
        if (price_usd < last_price[idx] - 0.1):
          msg = '🆘 '
          msg += str(price_usd) + ' '
          msg += url.split('=')[1] + ' '
          msg += link.get_attribute("href").split('?')[0] + '\n'
          bot.send_message('@TradingDowSignal',msg)
        
        last_price[idx] = price_usd
        # break
      except TimeoutException:
        print("Element not properly loaded")

    # print(msg)
    # time.sleep(1)

if __name__ == '__main__':
  main()