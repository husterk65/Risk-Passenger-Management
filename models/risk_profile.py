from dataclasses import dataclass


@dataclass
class RiskProfile:

    id: int | None = None

    full_name: str = ""
    passport_number: str = ""
    nationality: str = ""
    date_of_birth: str = ""
    gender: str = ""

    flight_count: int = 0
    baggage_card_count: int = 0
    destination_airport: str = ""

    # Keep these for future Risk Alert functionality
    risk_level: str = "Low"
    risk_reason: str = ""
    remarks: str = ""

    active: bool = True
    created_at: str = ""

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data.get("id"),

            full_name=data.get("full_name", ""),
            passport_number=data.get("passport_number", ""),
            nationality=data.get("nationality", ""),
            date_of_birth=data.get("date_of_birth", ""),
            gender=data.get("gender", ""),

            flight_count=data.get("flight_count", 0) or 0,
            baggage_card_count=data.get(
                "baggage_card_count", 0
            ) or 0,

            destination_airport=data.get(
                "destination_airport", ""
            ) or "",

            risk_level=data.get(
                "risk_level", "Low"
            ) or "Low",

            risk_reason=data.get(
                "risk_reason", ""
            ) or "",

            remarks=data.get(
                "remarks", ""
            ) or "",

            active=data.get("active", True),

            created_at=data.get(
                "created_at", ""
            ) or ""
        )

    def to_dict(self):

        data = {
            "full_name": self.full_name,
            "passport_number": self.passport_number,
            "nationality": self.nationality,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,

            "flight_count": self.flight_count,
            "baggage_card_count": self.baggage_card_count,
            "destination_airport": self.destination_airport,

            "risk_level": self.risk_level,
            "risk_reason": self.risk_reason,
            "remarks": self.remarks,

            "active": self.active,
        }

        # IMPORTANT:
        # id is intentionally NOT included.
        #
        # Supabase generates id automatically.

        return data