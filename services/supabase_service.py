import os

from dotenv import load_dotenv
from supabase import Client, create_client

class SupabaseService:

    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:

        if cls._client is None:

            load_dotenv()

            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                raise Exception("Supabase configuration not found.")

            cls._client = create_client(url, key)

        return cls._client