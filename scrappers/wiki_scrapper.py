import re
import time
import html
import requests
from bs4 import BeautifulSoup
from db_conexions.mongo_connection import PyMongoOperations

class WikiScrapper():
    """
    Clase del scrapper, recibe en el constructor
    el argumento mongo para ver si instanciar dicha db o no.
    Variable de clase: sesion de requests.
    Variables de instancia: url wikipedia, mongo arg, fecha y 
                            cursor de pymongo si --mongo == True
    """
    # class variables
    sesion = requests.session()
    def __init__(self, mongo):
        self.url = ('https://es.wikipedia.org/wiki/Anexo:'
                    'Estad%C3%ADsticas_de_la_Liga_de_Campeones_de_la_UEFA'
                    '#Tabla_hist%C3%B3rica_de_jugadores_con'
                    '_m%C3%A1s_presencias')
        self.mongo = mongo
        self._created_at = time.strftime("%Y-%m-%d")
        if self.mongo:
            self.pymongo_operations = PyMongoOperations()     
    
    def scraping(self):
        """
        Metodo principal que se encarga de scrapear la tabla desde wikipedia.
        Utiliza soup para encontrar el id de presencias, y con un next ubica la tabla.
        Se itera cada fila y se retorna como generador, para no excedernos del uso
        de memoria.
        Si --mongo == True, a su vez, inserta cada diccionario en mongo.
        """
        print('\n\x1b[1;33;40m<- SCRAPPING DATA FROM WIKIPEDIA ->\x1b[0m\n')
        soup = self.get_soup(self.url)
        table = soup.find(
            'span', id='Tabla_hist.C3.B3rica_de_jugadores_con_m.C3.A1s_presencias').findNext(
            'table')
        rows = table.find_all('tr')
        rows = [row for row in rows if row.find('th', text=re.compile("Jugador", re.IGNORECASE)) == None]
        rows = [row for row in rows if row.find('span', class_='flagicon') != None]
        for index, row in enumerate(rows):
            position = row.find('td').get_text()
            position = index + 1 if position.strip() == '=' else position
            flag_element = row.find('span', class_='flagicon')
            url_flag = flag_element.find('img')['src']
            name = flag_element.findNext('a').findNext('a')['title']
            data = {
                    'position': self.clean_data(position), 
                    'url_flag': self.clean_data(url_flag), 
                    'name': self.clean_data(name),
                    'created_at': self._created_at
                    }
            if self.mongo:
                self.pymongo_operations.insertOne('test_db', 'wiki_players', data)
                del data['_id']
            yield data

    @classmethod
    def get_soup(cls, url):
        """
        Metodo para hacer las requests, pude reutilizarse
        en caso de scrapings mas largos.
        Retorna: soup file
        """
        tries = 0
        banned_tries = 0
        wait = 0
        while True:
            try:
                response = cls.sesion.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            except ConnectionError:
                if tries > 5 and banned_tries < 3:
                    print(f'\nIp blocked {url} -> waiting {wait} seconds\n')
                    cls.sesion.close()
                    wait += 300
                    time.sleep(wait)
                    banned_tries += 1
                    cls.sesion = requests.session()
                    continue
                elif banned_tries > 3:
                    print("Couldn't unblock ip :(")
                    raise
                time.sleep(3)
                tries += 1
                continue

    @staticmethod
    def clean_data(string):
        """
        Metodo para normalizar los strings
        """
        string = re.sub(r'\n|\t|\r', '', str(string)).strip()
        string = html.unescape(string)
        return string
