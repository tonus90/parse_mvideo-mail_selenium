# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import time
from pymongo import MongoClient
# from selenium.webdriver.common.by import By

# chrome_options = Options()
# chrome_options.add_argument('start-maximized')

# driver = webdriver.Chrome(options=chrome_options)

# url = 'https://www.mvideo.ru/'
# driver.get(url)
# time.sleep(6)

# hits = driver.find_element(By.XPATH, '/html/body/mvid-root/div/mvid-primary-layout/mvid-layout/div/main/ng-component/div/mvid-simple-product-collection-mp[1]/mvid-simple-product-collection/mvid-carousel')
# a=1
client = MongoClient()

data = {}
data['name'] = ['emile']

db = client.themap
places = db.places
places.insert_one(data)
a=1