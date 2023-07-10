import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import shared.config as config

conn_url = f"postgresql+psycopg2://postgres:postgres@{config.dbhost}/{config.postgresdb}" # noqa
print(conn_url)
engine = db.create_engine(
    conn_url
)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
