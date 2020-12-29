import os
from selenium import webdriver

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

if os.name == 'nt':
    GOOGLE_CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    CHROMEDRIVER_PATH = 'C:\chromedriver\chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH

BROWSER = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
