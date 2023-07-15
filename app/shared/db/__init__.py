import shared.config as config
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists

conn_url = f"postgresql+psycopg2://postgres:postgres@{config.dbhost}/{config.postgresdb}"  # noqa
print(conn_url)
engine = db.create_engine(conn_url)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
