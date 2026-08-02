from dataclasses import dataclass
from typing import Optional


@dataclass
class RiskProfile:

    id: Optional[int] = None

    full_name: str = ""

    passport_number: str = ""

    nationality: str = ""

    date_of_birth: str = ""

    gender: str = ""

    risk_level: str = ""

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
            date_of_birth=str(data.get("date_of_birth", "")),
            gender=data.get("gender", ""),
            risk_level=data.get("risk_level", ""),
            risk_reason=data.get("risk_reason", ""),
            remarks=data.get("remarks", ""),
            active=data.get("active", True),
            created_at=str(data.get("created_at", ""))
        )

    def to_dict(self):

        return {
            "full_name": self.full_name,
            "passport_number": self.passport_number,
            "nationality": self.nationality,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "risk_level": self.risk_level,
            "risk_reason": self.risk_reason,
            "remarks": self.remarks,
            "active": self.active
        }