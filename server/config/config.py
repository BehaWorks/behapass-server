import os

DB_HOST = "mongodb://" + os.environ["db_host"] + ":" + os.environ["db_port"] + "/"
DB_NAME = "behaworks_behapass_v9"
DB_PORT = ""
URL_PREFIX = "/api"
MINIMUM_RECORDS = 10
try:
    METRIX_CHUNKS = int(os.environ["metrix_chunks"])
except (ValueError, KeyError):
    METRIX_CHUNKS = 3

try:
    NEIGHBOURS = int(os.environ["neighbours"])
except (ValueError, KeyError):
    NEIGHBOURS = 1
