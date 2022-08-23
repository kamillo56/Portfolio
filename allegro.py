from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sqlite3

db = sqlite3.connect('Domy.db')
cursor = db.cursor()

try:
    cursor.execute('CREATE TABLE Domy (Tytuł TEXT, Miasto TEXT, PowCałkowita TEXT, PowUżytkowa TEXT, cema REAL)')
except:
    print('Database is already created.')


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

wait = WebDriverWait(driver, 10)

URL = driver.get("https://allegro.pl/kategoria/domy-na-sprzedaz-112740?powierzchnia-dzialki-do=10000&powierzchnia-dzialki-od=1")
print(driver.title)

zgoda = driver.find_element(By.XPATH, '//*[@id="opbox-gdpr-consents-modal"]/div/div[2]/div/div[2]/button[2]')
zgoda.click()

kujPom = driver.find_element(By.XPATH, '//*[@id="filters"]/div[1]/div/div/div/section/div[2]/ul/li[2]/div/a')
kujPom.click()

pages = 10

for i in range(1, pages):
    for oferta in range(3, 58):
        tytul = wait.until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="search-results"]/div[6]/div/div/div/div/div/section[2]/article[{oferta}]/div/div/div[2]/div[1]/h2'))
        ).text

        cena = wait.until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="search-results"]/div[6]/div/div/div/div/div/section[2]/article[{oferta}]/div/div/div[2]/div[2]/div/div/span'))
        ).text
        cena = cena.replace(',', '').replace(' zł', '').replace(' ', '')

        powierzchniaC = wait.until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="search-results"]/div[6]/div/div/div/div/div/section[2]/article[{oferta}]/div/div/div[2]/div[1]/div[3]/div/dl/dd[2]'))
        ).text

        try:
            powierzchniaU = driver.find_element(By.XPATH, f'//*[@id="search-results"]/div[6]/div/div/div/div/div/section[2]/article[{oferta}]/div/div/div[2]/div[1]/div[3]/div/dl/dd[1]').text
        except: NoSuchElementException

        lokalizacja = wait.until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="search-results"]/div[6]/div/div/div/div/div/section[2]/article[{oferta}]/div/div/div[2]/div[3]/div[1]'))
        ).text
        lokalizacja = lokalizacja.split(': ')[1]

        cursor.execute('INSERT INTO Domy VALUES (?, ?, ?, ?, ?)', (tytul, lokalizacja, powierzchniaC, powierzchniaU, cena))
    db.commit()
    if i == 1:
        next = driver.find_element(By.XPATH, '//*[@id="search-results"]/div[7]/div[1]/div/div/div[2]/a')
    else:
        next = driver.find_element(By.XPATH, '//*[@id="search-results"]/div[7]/div[1]/div/div/div[2]/a[2]')
    next.click()

