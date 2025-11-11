import os
from pathlib import Path
from dotenv import (
    load_dotenv,
    find_dotenv
)

ROOT_PATH = Path(__file__).parent
print("ROOT_PATH:", ROOT_PATH)
load_dotenv(find_dotenv(str(ROOT_PATH / '.env')))


IP = os.environ.get("IP")
PORT = os.environ.get("PORT")
MODEL_PATH = os.environ.get("MODEL_PATH")
