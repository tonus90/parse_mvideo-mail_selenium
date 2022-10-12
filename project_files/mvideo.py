from xml.etree.ElementPath import xpath_tokenizer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.mvideo.ru/'
driver.get(url)
time.sleep(9)

a = '//div[@class="gallery-title-wrapper"]/div[contains(text(),"Хиты продаж")][1]/../../..'


block_hit = driver.find_element(By.XPATH, '/html/body/mvid-root/div/mvid-primary-layout/mvid-layout/div/main/ng-component/div/mvid-simple-product-collection-mp[1]/mvid-simple-product-collection/mvid-carousel/div[1]/div/mvid-product-cards-group')
urls = set()
while True:
    button = block_hit.find_element(By.XPATH, '/html/body/mvid-root/div/mvid-primary-layout/mvid-layout/div/main/ng-component/div/mvid-simple-product-collection-mp[1]/mvid-simple-product-collection/mvid-carousel/div[2]/button[2]/mvid-icon')
    hits_test = block_hit.find_elements(By.CLASS_NAME, 'img-with-badge')
    button.click()
    time.sleep(2)
    hits = block_hit.find_elements(By.CLASS_NAME, 'img-with-badge')
    if len(hits_test) < len(hits):
        button.click()
        hits = block_hit.find_elements(By.CLASS_NAME, 'img-with-badge')
    else:
        for good in hits:
            # tag = good.find_element(By.TAG_NAME, '')
            href = good.get_property('href')
            urls.add(href)
        break

client = MongoClient()
db = client['mvideo']
db.drop_collection('hits')
hits_coll = db['hits']
data = {}
# connect to db in terminal - mongod --dbpath ./mongo_data/ -> mongo db_name (mvideo)

for link in urls:
    driver.get(link)
    time.sleep(3)
    data['name'] = driver.find_element(By.TAG_NAME, 'h1').text
    data['price'] = driver.find_element(By.CLASS_NAME, 'price__main-value').text
    data['count_reviews'] = driver.find_element(By.XPATH, '/html/body/mvid-root/div/mvid-primary-layout/mvid-layout/div/main/mvid-pdp/mvid-pdp-general/div/mvid-general-details/section/div[2]/div[2]/mvid-preorder-v2-wrapper/div/mvideo-product-rating/div/a/meta[2]').text
    data['rating'] = driver.find_element(By.XPATH, '/html/body/mvid-root/div/mvid-primary-layout/mvid-layout/div/main/mvid-pdp/mvid-pdp-general/div/mvid-general-details/section/div[2]/div[2]/mvid-preorder-v2-wrapper/div/mvideo-product-rating/div/a/meta[2]').text
    data['url'] = [link]
    hits_coll.insert_one(data)
    data = {}