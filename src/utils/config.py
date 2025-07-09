import os
from dotenv import load_dotenv

load_dotenv() 

REDIS_URL = os.getenv("REDIS_URL",  "redis://localhost:6379/0")
OPEN_ROUTER_API_KEY=os.getenv("OPEN_ROUTER_API_KEY", None)
