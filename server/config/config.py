import os

DB_HOST = "mongodb://" + os.environ["db_host"] + ":" + os.environ["db_port"] + "/"
DB_NAME = "behaworks_logger_v8"
DB_PORT = ""
URL_PREFIX = "/api"
try:
    METRIX_CHUNKS = int(os.environ["metrix_chunks"])
except ValueError:
    METRIX_CHUNKS = 3

try:
    NEIGHBOURS = int(os.environ["neighbours"])
except ValueError:
    NEIGHBOURS = 3
