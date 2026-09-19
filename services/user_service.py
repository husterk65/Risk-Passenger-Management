from services.supabase_service import SupabaseService

class UserService:
# =====================================================
# Find user by username
# Used for login
# =====================================================

    @staticmethod
    def find_by_username(username):

        client = SupabaseService.get_client()

        response = (
            client
            .table("app_users")
            .select("*")
            .eq("username", username)
            .eq("active", True)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # =====================================================
    # Get all users
    # Used by Users Management page
    # =====================================================

    @staticmethod
    def get_all():

        client = SupabaseService.get_client()

        response = (
            client
            .table("app_users")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data

    # =====================================================
    # Check whether username already exists
    # =====================================================

    @staticmethod
    def username_exists(username):

        client = SupabaseService.get_client()

        response = (
            client
            .table("app_users")
            .select("id")
            .eq("username", username)
            .execute()
        )

        return bool(response.data)

    # =====================================================
    # Create user
    # =====================================================

    @staticmethod
    def create(
        username,
        password_hash,
        full_name,
        role,
        active=True
    ):

        client = SupabaseService.get_client()

        data = {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role,
            "active": active,
        }

        response = (
            client
            .table("app_users")
            .insert(data)
            .execute()
        )

        return response.data

    # =====================================================
    # Update user
    # =====================================================

    @staticmethod
    def update(
        user_id,
        full_name,
        role,
        active
    ):

        client = SupabaseService.get_client()

        data = {
            "full_name": full_name,
            "role": role,
            "active": active,
        }

        response = (
            client
            .table("app_users")
            .update(data)
            .eq("id", user_id)
            .execute()
        )

        return response.data

    # =====================================================
    # Update password
    # =====================================================

    @staticmethod
    def update_password(
        user_id,
        password_hash
    ):

        client = SupabaseService.get_client()

        data = {
            "password_hash": password_hash,
        }

        response = (
            client
            .table("app_users")
            .update(data)
            .eq("id", user_id)
            .execute()
        )

        return response.data

    # =====================================================
    # Activate / Deactivate user
    # =====================================================

    @staticmethod
    def set_active(
        user_id,
        active
    ):

        client = SupabaseService.get_client()

        response = (
            client
            .table("app_users")
            .update({
                "active": active
            })
            .eq("id", user_id)
            .execute()
        )

        return response.data