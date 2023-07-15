import os

from dotenv import load_dotenv

load_dotenv()

LOGLEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
dbhost = os.getenv("DB_HOST", "localhost")
postgresuser = os.getenv("POSTGRES_USER", "postgres")
postgrespassword = os.getenv("POSTGRES_PASSWORD", "postgres")
postgresdb = os.getenv("POSTGRES_DB", "sentiment_analysis")
schedule = os.getenv("SCHEDULE", "60")
redis_url = os.getenv("REDIS_URL")
