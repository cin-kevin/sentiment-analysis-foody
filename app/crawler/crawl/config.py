import os

from dotenv import load_dotenv

load_dotenv()


# Creates a config object to be used in the config generator.
# It is the responsibility of the caller to ensure that the config is valid
class Config:
    username: str = None
    password: str = None


def parse_config() -> Config:
    """
    Parse environment variables to create a : class : ` Config ` object.
    @return : class : ` Config ` object with parsed environment
    """
    config: Config = Config()
    config.username = os.getenv("USERNAME", "hunggs.no7@gmail.com")
    config.password = os.getenv("PASSWORD", "P@ssword1")
    return config


cfg = parse_config()
