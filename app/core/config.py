import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
assert DATABASE_URL, "DATABASE_URL is not set in .env"
JWKS_URL: str = os.getenv("JWKS_URL", "")
assert JWKS_URL, "JWKS_URL is not set in .env"
PROJECT_URL: str = os.getenv("PROJECT_URL", "")
assert PROJECT_URL, "PROJECT_URL is not set in .env"
AUDIENCE: str = os.getenv("AUDIENCE", "")
assert AUDIENCE, "AUDIENCE is not set in .env"
ALGORITHM: str = os.getenv("ALGORITHM", "")
assert ALGORITHM, "ALGORITHM is not set in .env"
