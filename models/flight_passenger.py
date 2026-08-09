from dataclasses import dataclass


@dataclass
class FlightPassenger:

    id: int | None = None
    flight_id: int | None = None

    seat_number: str = ""

    full_name: str = ""
    gender: str = ""
    nationality: str = ""
    date_of_birth: str = ""

    document_type: str = ""
    document_number: str = ""

    issuing_country: str = ""
    residence_country: str = ""

    origin: str = ""
    destination: str = ""
    first_airport: str = ""

    baggage_count: int = 0
    document_expiry_date: str = ""

    created_at: str = ""

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data.get("id"),
            flight_id=data.get("flight_id"),

            seat_number=data.get(
                "seat_number", ""
            ),

            full_name=data.get(
                "full_name", ""
            ),

            gender=data.get(
                "gender", ""
            ),

            nationality=data.get(
                "nationality", ""
            ),

            date_of_birth=data.get(
                "date_of_birth", ""
            ),

            document_type=data.get(
                "document_type", ""
            ),

            document_number=data.get(
                "document_number", ""
            ),

            issuing_country=data.get(
                "issuing_country", ""
            ),

            residence_country=data.get(
                "residence_country", ""
            ),

            origin=data.get(
                "origin", ""
            ),

            destination=data.get(
                "destination", ""
            ),

            first_airport=data.get(
                "first_airport", ""
            ),

            baggage_count=data.get(
                "baggage_count", 0
            ),

            document_expiry_date=data.get(
                "document_expiry_date", ""
            ),

            created_at=data.get(
                "created_at", ""
            ),
        )

    def to_dict(self):

        return {
            "flight_id": self.flight_id,
            "seat_number": self.seat_number,
            "full_name": self.full_name,
            "gender": self.gender,
            "nationality": self.nationality,
            "date_of_birth": self.date_of_birth,
            "document_type": self.document_type,
            "document_number": self.document_number,
            "issuing_country": self.issuing_country,
            "residence_country": self.residence_country,
            "origin": self.origin,
            "destination": self.destination,
            "first_airport": self.first_airport,
            "baggage_count": self.baggage_count,
            "document_expiry_date": self.document_expiry_date,
        }