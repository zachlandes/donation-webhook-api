import os

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

if not SECRET_TOKEN:
    raise ValueError("SECRET_TOKEN environment variable is not set")
