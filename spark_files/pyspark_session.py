import os
import time
from pyspark.sql.utils import AnalysisException
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

class Session():
    """
    Clase que se encarga de levantar una sesion de Spark.
    Ademas provee distintos metodos, load_data que permite
    cargar un df desde una losta de diccionarios
    y save_data que la guarda en .tsv.
    """
    def __init__(self, mode):
        self.spark = SparkSession \
                .builder \
                .appName("spark_scraping_data") \
                .config('spark.driver.memory', '6g') \
                .getOrCreate()
        self.mode = mode
        self._created_at = time.strftime("%Y-%m-%d")
        self.list_dicts = []
    
    def __del__(self):
        try:
            self.spark.stop()
        except:
            pass
        finally:
            print('Spark stopped')
    
    def load_data(self):
        """
        Metodo para crear un pyspark dataframe
        en base a la lista de diccionarios scrapeada.
        """
        print('\n\x1b[1;33;40mLOADING DATA...\x1b[0m\n')
        sparkContext = self.spark.sparkContext
        _jsons = sparkContext.parallelize(self.list_dicts)
        df = self.spark.read.json(_jsons)
        print('\n\x1b[1;33;40mSHOWING DATA...\x1b[0m\n')
        if df.count() > 20:
            print('\x1b[1;33;40mTOP 10:\x1b[0m')
            df.show(10)
        else:
            df.collect()
        if self.mode == 'production':
            self.save_to_tsv(df)
    
    def save_to_tsv(self, df:DataFrame):
        """
        Metodo que guarda el df en formato tsv.
        Si no esta el directorio output, lo crea con os.
        Al file le asigna una fecha para evitar duplicados.
        """
        actual_path = os.getcwd()
        directory = 'tsv_files'
        folder = os.path.join(actual_path, directory)
        if not os.path.exists(folder):
            print(f'### Folder {directory} not found, creating... ###')
            os.makedirs(folder)
            print('### Folder created! ###')
        try:
            filename = f"{folder}/presencia_jugadores_{self._created_at}.tsv"
            df.write. \
            option("header", "true"). \
            option("delimiter", "\t"). \
            csv(filename)
            print('\x1b[1;33;40mTSV FILE SAVED\x1b[0m')
        except AnalysisException:
            print('\x1b[1;33;40mTSV ALREADY EXISTS!\x1b[0m')


