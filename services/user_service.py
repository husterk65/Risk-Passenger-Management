from services.supabase_service import SupabaseService
from models.current_user import CurrentUser

class UserService:

    @staticmethod
    def find_by_username(username):

        client = SupabaseService.get_client()

        response = (
            client.table("app_users")
            .select("*")
            .eq("username", username)
            .eq("active", True)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]