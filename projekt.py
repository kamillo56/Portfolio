from bs4 import BeautifulSoup
from requests import get
import sqlite3

strona = 'https://www.olx.pl/d/elektronika/komputery/drukarki-i-skanery/drukarki-3d/?search%5Bfilter_float_price:from%5D=500'

#sqlite 
db = sqlite3.connect('dane.db')
cursor = db.cursor()

#Tworzenie bazy danych
try:
    cursor.execute('CREATE TABLE offers (name TEXT, city TEXT, price REAL, negotiation TEXT, data TEXT)')
except:
    print(':)')

def parse_page(number):
    print(f'Getting info from page {number}')
    page = get(f'{strona}&page={number}')
    bs = BeautifulSoup(page.content, 'html.parser')

    #Wyszukiwanie oferty
    for offer in bs.find_all('div', class_='css-qfzx1y'):

        #Miejscowość i data
        dataMiejscowosc = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').getText()
        listaDM = dataMiejscowosc.split(' - ')
        miejscowosc = listaDM[0].split(',')[0]
        data = listaDM[1]

        #Tytuł i cena
        tytul = offer.find('h6', class_='css-v3vynn-Text eu5v0x0').getText()
        cenaNego = offer. find('p', class_='css-wpfvmn-Text eu5v0x0').getText()
        nego = cenaNego.split('zł')[1]
        cena = cenaNego.split('zł')[0]
        cena = cena.replace(' ','')

        #Gdy cena zawiera przecinek, który psuje sortowanie w bazie danych.
        if "," in cena:
            cena = cena.split(',')
            if int(cena[1]) >= 50:
               cena = int(cena[0]) + 1
            else: cena = cena[0]

        #Negocjacja
        if nego == 'do negocjacji':
            nego = 'Tak'
        else:
            nego = 'Nie'
        caloscCena = [cena, nego]

        #Zapisywanie w bazie danych i commit zmian
        cursor.execute('INSERT INTO offers VALUES (?, ?, ?, ?, ?)', (tytul, miejscowosc, cena, nego, data))
    db.commit()

for page in range(1, 11):
    parse_page(page)


#Zamknięcie połączenia
db.close()
        
    
    
    

