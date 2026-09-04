from services.supabase_service import SupabaseService


class AuditLogService:

    @staticmethod
    def log(
        user_id,
        username,
        action,
        module,
        details=None
    ):
        supabase = SupabaseService.get_client()

        data = {
            "user_id": user_id,
            "username": username,
            "action": action,
            "module": module,
            "details": details,
        }

        response = (
            supabase
            .table("audit_logs")
            .insert(data)
            .execute()
        )

        return response.data

    @staticmethod
    def get_all():
        supabase = SupabaseService.get_client()

        response = (
            supabase
            .table("audit_logs")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data