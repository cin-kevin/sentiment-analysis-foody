from dotenv import load_dotenv
import os

load_dotenv()

LOGLEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
dbhost = os.getenv("DB_HOST", "localhost")
postgresuser = os.getenv("POSTGRES_USER", "postgres")
postgrespassword = os.getenv("POSTGRES_PASSWORD", "postgres")
postgresdb = os.getenv("POSTGRES_DB", "sentiment_analysis")
