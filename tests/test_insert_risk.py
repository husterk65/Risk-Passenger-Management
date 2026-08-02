from models.risk_profile import RiskProfile
from services.risk_profile_service import RiskProfileService

profile = RiskProfile(
    full_name="CHOVY",
    passport_number="BAVK129434",
    nationality="Vietnam",
    date_of_birth="2002-01-01",
    gender="Male",
    risk_level="High",
    risk_reason="Testing",
    remarks="Insert Test"
)

RiskProfileService.insert(profile)

print("Done")