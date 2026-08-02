from services.risk_profile_service import RiskProfileService
rows = RiskProfileService.search("TEST")

for row in rows:
    print(row.full_name)