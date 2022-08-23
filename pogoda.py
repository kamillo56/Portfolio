from requests import get
from json import loads

cities = ['Kalisz', 'Warszawa', 'Wrocław', 'Bielsko Biała']

def main():
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = get(url)
    print('Stacja, Temp, Godzina, Data')

    for row in loads(response.text):
        if row['stacja'] in cities:
            print(row['stacja'], row['temperatura']+"C", row['godzina_pomiaru']+':00', row['data_pomiaru'])

if __name__ == '__main__':
    main()