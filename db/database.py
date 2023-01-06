from config import settings
from supabase import create_client, Client

supabase: Client = create_client(settings.url, settings.key)

def get_db():
    db = supabase
    try:
        yield db
    finally:
        pass