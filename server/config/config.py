import os

DB_HOST = "mongodb://" + os.environ["db_host"] + ":" + os.environ["db_port"] + "/"
DB_NAME = "behaworks_logger_v7"
DB_PORT = ""
URL_PREFIX = "/api"
METRIX_CHUNKS = 3
NEIGHBOURS = 3
