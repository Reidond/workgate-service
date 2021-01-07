from selenium import webdriver
from sys import platform as _platform
from pathlib import Path

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

if _platform == "win64":
    GOOGLE_CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    CHROMEDRIVER_PATH = 'C:\chromedriver\chromedriver.exe'
elif _platform == 'darwin':
    GOOGLE_CHROME_PATH = ''
    CHROMEDRIVER_PATH = str(
        Path.joinpath(Path.home(), '.local/bin/chromedriver'))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

if GOOGLE_CHROME_PATH:
    chrome_options.binary_location = GOOGLE_CHROME_PATH

BROWSER = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
