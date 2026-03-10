import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
assert DATABASE_URL, "DATABASE_URL is not set in .env"
