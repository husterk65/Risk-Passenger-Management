from services.supabase_service import SupabaseService
from models.risk_profile import RiskProfile


class RiskProfileService:

    TABLE_NAME = "risk_profiles"

    # ==================================================
    # GET ALL
    # ==================================================

    @staticmethod
    def get_all() -> list[RiskProfile]:

        client = SupabaseService.get_client()

        response = (
            client
            .table(RiskProfileService.TABLE_NAME)
            .select("*")
            .order("id", desc=False)
            .execute()
        )

        return [
            RiskProfile.from_dict(row)
            for row in response.data
        ]

    # ==================================================
    # GET BY ID
    # ==================================================

    @staticmethod
    def get_by_id(profile_id: int):

        client = SupabaseService.get_client()

        response = (
            client
            .table(RiskProfileService.TABLE_NAME)
            .select("*")
            .eq("id", profile_id)
            .single()
            .execute()
        )

        if response.data is None:
            return None

        return RiskProfile.from_dict(
            response.data
        )

    # ==================================================
    # CREATE
    # ==================================================

    @staticmethod
    def create(profile: RiskProfile):

        client = SupabaseService.get_client()

        response = (
            client
            .table(RiskProfileService.TABLE_NAME)
            .insert(profile.to_dict())
            .execute()
        )

        if not response.data:
            return None

        return RiskProfile.from_dict(
            response.data[0]
        )

    # ==================================================
    # CREATE MANY
    # ==================================================

    @staticmethod
    def create_many(profiles: list[RiskProfile]):

        if not profiles:
            return []

        client = SupabaseService.get_client()

        data = [
            profile.to_dict()
            for profile in profiles
        ]

        response = (
            client
            .table(RiskProfileService.TABLE_NAME)
            .insert(data)
            .execute()
        )

        if not response.data:
            return []

        return [
            RiskProfile.from_dict(row)
            for row in response.data
        ]
    # ==================================================
    # UPDATE
    # ==================================================

    @staticmethod
    def update(profile: RiskProfile):

        if profile.id is None:
            raise ValueError(
                "Cannot update profile without id."
            )

        client = SupabaseService.get_client()

        response = (
            client
            .table(RiskProfileService.TABLE_NAME)
            .update(profile.to_dict())
            .eq("id", profile.id)
            .execute()
        )

        if not response.data:
            return None

        return RiskProfile.from_dict(
            response.data[0]
        )

    # ==================================================
    # DELETE
    # ==================================================

    @staticmethod
    def delete(profile_id: int):

        client = SupabaseService.get_client()

        (
            client
            .table(RiskProfileService.TABLE_NAME)
            .delete()
            .eq("id", profile_id)
            .execute()
        )

    # ==================================================
    # SEARCH
    # ==================================================

    @staticmethod
    def search(keyword: str):

        keyword = keyword.strip()

        if keyword == "":
            return RiskProfileService.get_all()

        client = SupabaseService.get_client()

        response = (
            client
            .table(RiskProfileService.TABLE_NAME)
            .select("*")
            .or_(
                f"full_name.ilike.%{keyword}%,"
                f"passport_number.ilike.%{keyword}%,"
                f"nationality.ilike.%{keyword}%,"
                f"destination_airport.ilike.%{keyword}%"
            )
            .order("id", desc=False)
            .execute()
        )

        return [
            RiskProfile.from_dict(row)
            for row in response.data
        ]