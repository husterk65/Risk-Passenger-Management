from dataclasses import dataclass


@dataclass
class Flight:

    id: int | None = None

    flight_number: str = ""
    airline: str = ""

    flight_date: str = ""

    origin: str = ""
    destination: str = ""

    route: str = ""
    transit: str = ""

    created_at: str = ""

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data.get("id"),

            flight_number=data.get(
                "flight_number", ""
            ),

            airline=data.get(
                "airline", ""
            ),

            flight_date=data.get(
                "flight_date", ""
            ),

            origin=data.get(
                "origin", ""
            ),

            destination=data.get(
                "destination", ""
            ),

            route=data.get(
                "route", ""
            ),

            transit=data.get(
                "transit", ""
            ),

            created_at=data.get(
                "created_at", ""
            ),
        )

    def to_dict(self):

        return {
            "flight_number": self.flight_number,
            "airline": self.airline,
            "flight_date": self.flight_date,
            "origin": self.origin,
            "destination": self.destination,
            "route": self.route,
            "transit": self.transit,
        }