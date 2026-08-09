import pandas as pd

from models.risk_profile import RiskProfile


class ExcelService:

    # ==================================================
    # EXCEL COLUMN INDEX
    # ==================================================

    FULL_NAME_COL = 1
    NATIONALITY_COL = 2
    DATE_OF_BIRTH_COL = 3
    PASSPORT_COL = 4
    GENDER_COL = 5
    FLIGHT_COUNT_COL = 6
    BAGGAGE_CARD_COUNT_COL = 7
    DESTINATION_AIRPORT_COL = 8

    # ==================================================
    # READ RISK PROFILES
    # ==================================================

    @staticmethod
    def read_risk_profiles(file_path: str) -> list[RiskProfile]:

        # Read Excel without using the first row as header
        df = pd.read_excel(
            file_path,
            header=None
        )

        # Remove completely empty rows
        df = df.dropna(
            how="all"
        )

        profiles = []

        # Data starts from row index 2
        for _, row in df.iloc[2:].iterrows():

            # Skip empty rows
            if pd.isna(
                row[ExcelService.FULL_NAME_COL]
            ):
                continue

            profile = ExcelService._row_to_profile(
                row
            )

            profiles.append(profile)

        return profiles

    # ==================================================
    # CONVERT ROW → RISK PROFILE
    # ==================================================

    @staticmethod
    def _row_to_profile(row) -> RiskProfile:

        return RiskProfile(

            id=None,

            full_name=ExcelService._get_string(
                row[ExcelService.FULL_NAME_COL]
            ),

            passport_number=ExcelService._get_string(
                row[ExcelService.PASSPORT_COL]
            ),

            nationality=ExcelService._get_string(
                row[ExcelService.NATIONALITY_COL]
            ),

            date_of_birth=ExcelService._get_date(
                row[ExcelService.DATE_OF_BIRTH_COL]
            ),

            gender=ExcelService._convert_gender(
                row[ExcelService.GENDER_COL]
            ),

            flight_count=ExcelService._get_int(
                row[ExcelService.FLIGHT_COUNT_COL]
            ),

            baggage_card_count=ExcelService._get_int(
                row[ExcelService.BAGGAGE_CARD_COUNT_COL]
            ),

            destination_airport=ExcelService._get_string(
                row[ExcelService.DESTINATION_AIRPORT_COL]
            ),

            risk_level="Low",

            risk_reason="",

            remarks="",

            active=True,

            created_at=""
        )

    # ==================================================
    # HELPERS
    # ==================================================

    @staticmethod
    def _get_string(value) -> str:

        if pd.isna(value):
            return ""

        return str(value).strip()

    @staticmethod
    def _get_int(value) -> int:

        if pd.isna(value):
            return 0

        try:
            return int(value)

        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _get_date(value) -> str:

        if pd.isna(value):
            return ""

        try:
            date = pd.to_datetime(value)

            return date.strftime(
                "%Y-%m-%d"
            )

        except (ValueError, TypeError):
            return ""

    @staticmethod
    def _convert_gender(value) -> str:

        gender = ExcelService._get_string(
            value
        )

        mapping = {
            "Nam": "Male",
            "Nữ": "Female",
            "Nu": "Female",
            "Male": "Male",
            "Female": "Female",
            "Other": "Other",
        }

        return mapping.get(
            gender,
            gender
        )