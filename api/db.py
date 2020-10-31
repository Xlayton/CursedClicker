import psycopg2
from psycopg2.errors import SerializationFailure

conn = psycopg2.connect(
    database='defaultdb',
    user='zslocum',
    sslmode='require',
    sslrootcert='/home/joshuavanantwerp/Downloads/cursed-clicker-ca.crt',
    sslkey='/home/joshuavanantwerp/Downloads/cursed-clicker-ca.crt',
    sslcert='/home/joshuavanantwerp/Downloads/cursed-clicker-ca.crt',
    port=26257,
    host='cursed-clicker-5zg.gcp-us-west2.cockroachlabs.cloud'
)
