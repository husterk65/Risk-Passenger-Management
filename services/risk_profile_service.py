from services.supabase_service import SupabaseService
from models.risk_profile import RiskProfile

class RiskProfileService:

    TABLE_NAME = "risk_profiles"

    @staticmethod
    def get_all() -> list[RiskProfile]:

        client = SupabaseService.get_client()

        response = (
            client.table(RiskProfileService.TABLE_NAME)
            .select("*")
            .order("id")
            .execute()
        )

        return [
            RiskProfile.from_dict(row)
            for row in response.data
        ]

    @staticmethod
    def get_by_id(profile_id: int):

        client = SupabaseService.get_client()

        response = (
            client.table(RiskProfileService.TABLE_NAME)
            .select("*")
            .eq("id", profile_id)
            .single()
            .execute()
        )

        if response.data is None:
            return None

        return RiskProfile.from_dict(response.data)

    @staticmethod
    def insert(profile: RiskProfile):

        client = SupabaseService.get_client()

        (
            client.table(RiskProfileService.TABLE_NAME)
            .insert(profile.to_dict())
            .execute()
        )

    @staticmethod
    def update(profile: RiskProfile):

        client = SupabaseService.get_client()

        (
            client.table(RiskProfileService.TABLE_NAME)
            .update(profile.to_dict())
            .eq("id", profile.id)
            .execute()
        )

    @staticmethod
    def delete(profile_id: int):

        client = SupabaseService.get_client()

        (
            client.table(RiskProfileService.TABLE_NAME)
            .delete()
            .eq("id", profile_id)
            .execute()
        )

    @staticmethod
    def search(keyword: str):

        keyword = keyword.strip()

        if keyword == "":
            return RiskProfileService.get_all()

        client = SupabaseService.get_client()

        response = (
            client.table(RiskProfileService.TABLE_NAME)
            .select("*")
            .or_(
                f"full_name.ilike.%{keyword}%,"
                f"passport_number.ilike.%{keyword}%,"
                f"nationality.ilike.%{keyword}%"
            )
            .order("id")
            .execute()
        )

        return [
            RiskProfile.from_dict(row)
            for row in response.data
        ]