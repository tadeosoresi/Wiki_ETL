import sys
import argparse
from spark_files.pyspark_session import Session
from scrappers.wiki_scrapper import WikiScrapper

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

if __name__ == '__main__':
    """
    Ejemplo: python3 main.py --mode production --mongo True
    main.py ---> Desde aca corremos el script y ponemos a funcionar el ETL
    Argumentos:
    --mode: testing/production, dependiendo el argumento guarda el dataframe en .tsv o no.
    --mongo: True/False, por defecto esta en False, si especificamos True guardara la data
                MongoDB tambien.
    Posteriormente incia una SparkSession, llama al scrapper y va pasando cada dato,
    a la sesion de spark para que las cargue en un df y ejecute las distintas
    operaciones.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', help='modo testing/production, guarda tsv file o no.', 
                        type=str)
    parser.add_argument('--mongo', help='True guarda data en mongo, dafult esta en False', 
                        type=bool, default=False)
    args = parser.parse_args()
    modes = ['testing', 'production']
    args.mode = args.mode.strip().lower()
    if not args.mode or args.mode not in(modes):
        raise argparse.ArgumentError('Specify correct mode in str format (testing/production)!')
    pyspark_session = Session(args.mode)
    scrapper = WikiScrapper(args.mongo)
    scraping_data = scrapper.scraping()
    for data in scraping_data:
        pyspark_session.list_dicts.append(data)
    pyspark_session.load_data()
    