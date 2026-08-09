from services.supabase_service import SupabaseService
from models.flight_passenger import FlightPassenger


class FlightPassengerService:

    TABLE_NAME = "flight_passengers"

    @staticmethod
    def get_by_flight(
        flight_id: int
    ) -> list[FlightPassenger]:

        client = SupabaseService.get_client()

        response = (
            client
            .table(
                FlightPassengerService.TABLE_NAME
            )
            .select("*")
            .eq("flight_id", flight_id)
            .order("id")
            .execute()
        )

        return [
            FlightPassenger.from_dict(row)
            for row in response.data
        ]

    @staticmethod
    def create_many(
        passengers: list[FlightPassenger]
    ):

        if not passengers:
            return []

        client = SupabaseService.get_client()

        data = [
            passenger.to_dict()
            for passenger in passengers
        ]

        response = (
            client
            .table(
                FlightPassengerService.TABLE_NAME
            )
            .insert(data)
            .execute()
        )

        return [
            FlightPassenger.from_dict(row)
            for row in response.data
        ]