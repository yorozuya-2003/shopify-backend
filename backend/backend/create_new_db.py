from os import environ
from dotenv import load_dotenv

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from aws_secrets_manager import get_secret

load_dotenv()
aws_secret = get_secret()

db_name = environ.get('DB_NAME')

con = psycopg2.connect(
    dbname=db_name,
    host=environ.get('DB_HOST'),
    user=aws_secret['username'],
    password=aws_secret['password'],
    port=environ.get('DB_PORT'),
)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

cur.execute(sql.SQL("CREATE DATABASE {}").format(
    sql.Identifier(db_name))
)
