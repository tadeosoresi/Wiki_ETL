import pymongo
from pprint import pprint
from pymongo import InsertOne
from typing import get_type_hints
from pymongo.errors import ConnectionFailure

class PyMongoConnection():
    """
    Clase principal que instancia la conexion a mongo.
    No requiere user ni pass, la ip es la seteada en el compose.
    """
    def __init__(self):
        try:
            self.server = pymongo.MongoClient("mongodb://172.100.0.2:27017")
            print('\nConnected to MongoDB :)\n')
        except ConnectionFailure:
            print('Error de conexión, verificar si IP concuerda o si MongoDB esta corriendo\n')
            raise 

class PyMongoOperations(PyMongoConnection):
    """
    Clase hija que hereda de PyMongoConnection
    la conexion.
    Tiene distintos metodos para operar con pymongo
    """
    def __init__(self):
         super().__init__()

    def insertOne(self, db:str, collection:str, dict_data:dict):
        """
        Metodo reutilizable para insertar en mongo}
        Args: db -> nombre database
              collection -> nombre collecion
              dict_data -> diccionario
        """
        db = self.server[db]
        collection = db[collection]
        collection.insert_one(dict_data)
        print('\n\x1b[1;33;40mInserted dict in MongoDB\x1b[0m\n')
    
    def insertMany(self, db:str, collection:str, data:list):
        """
        Metodo reutilizable para hacer un bulk insert de datos
        Args: db -> nombre database
              collection -> nombre collecion
              data -> lista de diccionarios
        """
        db = self.server[db]
        collection = db[collection]
        result = collection.test.bulk_write([InsertOne(_dict) for _dict in data])
        print('\n\x1b[1;33;40mBulk write done, data inserted in MongoDB\x1b[0m\n')
        pprint(result.bulk_api_result)
    
