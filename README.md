# Wiki_ETL (Yuno Test)
ETL que utiliza BeautifulSoup, PyMongo y PySpark.

GUIDE:
docker build --rm -t etl_image . (sobre el directorio del repo)
docker-compose up -d (para levantar contenedores)
docker exec -it etl_container bash (para ejecutar un bash dentro del contenedor de spark)
python main.py --mode testing/production --mongo True (para correr el ETL)
jupyter lab --ip 0.0.0.0 --no-browser --port 57000 --allow-root (para correr un servidor de jupyter en caso de querer)

## 🚀 Lista de mejoras
La comunidad **open-source** puede mantener este proyecto como desee. Algunas features que se podrían agregar:

- [ ] SparkStreaming en caso de querer las estadisticas en tiempo real.
- [ ] Obtener mas datos y realizar un analisis mas profundo con pypsark, visualizaciones.
- [ ] Servir datos con API sencilla en Flask.

Thanks!
