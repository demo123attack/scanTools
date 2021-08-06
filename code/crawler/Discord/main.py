from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
browser.get("https://discord.com/developers/docs/resources/channel#embed-limits")

des = browser.find_elements(By.CSS_SELECTOR,".paragraph-mttuxw")
for d in des:
    print(d.text)

browser.close()