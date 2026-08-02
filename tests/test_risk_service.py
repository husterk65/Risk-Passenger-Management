from services.risk_profile_service import RiskProfileService


rows = RiskProfileService.get_all()

print(f"Total: {len(rows)}")

for row in rows:

    print(row)