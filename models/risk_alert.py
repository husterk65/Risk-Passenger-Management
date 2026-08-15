from dataclasses import dataclass


@dataclass
class RiskAlert:

    flight_id: int
    flight_number: str

    passenger_id: int | None = None

    full_name: str = ""
    passport_number: str = ""
    nationality: str = ""
    date_of_birth: str = ""
    gender: str = ""

    risk_level: str = ""
    risk_reason: str = ""

    created_at: str = ""

    def to_dict(self) -> dict:

        return {
            "flight_id": self.flight_id,
            "flight_number": self.flight_number,
            "passenger_id": self.passenger_id,
            "full_name": self.full_name,
            "passport_number": self.passport_number,
            "nationality": self.nationality,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "risk_level": self.risk_level,
            "risk_reason": self.risk_reason,
            "created_at": self.created_at,
        }