from services.supabase_service import SupabaseService
from models.flight import Flight


class FlightService:

    TABLE_NAME = "flights"

    @staticmethod
    def get_all() -> list[Flight]:

        client = SupabaseService.get_client()

        response = (
            client
            .table(FlightService.TABLE_NAME)
            .select("*")
            .order("flight_date", desc=True)
            .execute()
        )

        return [
            Flight.from_dict(row)
            for row in response.data
        ]

    @staticmethod
    def get_by_id(flight_id: int):

        client = SupabaseService.get_client()

        response = (
            client
            .table(FlightService.TABLE_NAME)
            .select("*")
            .eq("id", flight_id)
            .single()
            .execute()
        )

        if response.data is None:
            return None

        return Flight.from_dict(
            response.data
        )

    @staticmethod
    def find_by_number_and_date(
        flight_number: str,
        flight_date: str
    ):

        client = SupabaseService.get_client()

        response = (
            client
            .table(FlightService.TABLE_NAME)
            .select("*")
            .eq("flight_number", flight_number)
            .eq("flight_date", flight_date)
            .execute()
        )

        if not response.data:
            return None

        return Flight.from_dict(
            response.data[0]
        )

    @staticmethod
    def create(flight: Flight):

        client = SupabaseService.get_client()

        response = (
            client
            .table(FlightService.TABLE_NAME)
            .insert(flight.to_dict())
            .execute()
        )

        if not response.data:
            return None

        return Flight.from_dict(
            response.data[0]
        )