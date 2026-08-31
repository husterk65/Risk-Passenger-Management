import pandas as pd

from models.risk_profile import RiskProfile
from models.flight import Flight
from models.flight_passenger import FlightPassenger

from services.flight_service import FlightService
from services.flight_passenger_service import (
    FlightPassengerService
)

from utils.column_config import (
    EXCEL_SHEET_CONFIG,
    FLIGHT_EXCEL_MAP,
    PASSENGER_EXCEL_MAP,
)


class ExcelService:

    # ==================================================
    # RISK PROFILE - EXCEL COLUMN INDEX
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
    def read_risk_profiles(
        file_path: str
    ) -> list[RiskProfile]:

        df = pd.read_excel(
            file_path,
            header=None
        )

        df = df.dropna(
            how="all"
        )

        profiles = []

        for _, row in df.iloc[2:].iterrows():

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
    # CONVERT ROW -> RISK PROFILE
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
    # IMPORT FLIGHT EXCEL
    # ==================================================

    @staticmethod
    def import_flight_excel(
        file_path: str
    ):

        # --------------------------------------------------
        # Read Flight Sheet
        # --------------------------------------------------

        flight_config = (
            EXCEL_SHEET_CONFIG["flight"]
        )

        flight_df = pd.read_excel(
            file_path,
            sheet_name=flight_config["name"],
            header=flight_config["header"]
        )

        # --------------------------------------------------
        # Read Passenger Sheet
        # --------------------------------------------------

        passenger_config = (
            EXCEL_SHEET_CONFIG["passenger"]
        )

        passenger_df = pd.read_excel(
            file_path,
            sheet_name=passenger_config["name"],
            header=passenger_config["header"]
        )

        # --------------------------------------------------
        # Normalize columns
        # --------------------------------------------------

        flight_df = (
            ExcelService._normalize_dataframe(
                flight_df
            )
        )

        passenger_df = (
            ExcelService._normalize_dataframe(
                passenger_df
            )
        )

        # --------------------------------------------------
        # Validate columns
        # --------------------------------------------------

        ExcelService._validate_columns(
            flight_df,
            FLIGHT_EXCEL_MAP
        )

        ExcelService._validate_columns(
            passenger_df,
            PASSENGER_EXCEL_MAP
        )

        # --------------------------------------------------
        # Validate Flight Data
        # --------------------------------------------------

        if flight_df.empty:

            raise ValueError(
                "Sheet chuyến bay không có dữ liệu."
            )

        # --------------------------------------------------
        # Read first Flight row
        # --------------------------------------------------

        flight_row = flight_df.iloc[0]

        flight_data = ExcelService._map_row(
            flight_row,
            FLIGHT_EXCEL_MAP
        )

        # --------------------------------------------------
        # Convert Flight Date
        # --------------------------------------------------

        flight_data["flight_date"] = (
            ExcelService._get_date(
                flight_data.get(
                    "flight_date"
                )
            )
        )

        # --------------------------------------------------
        # Required fields
        # --------------------------------------------------

        if not flight_data.get(
            "flight_number"
        ):

            raise ValueError(
                "Không tìm thấy số chuyến bay."
            )

        if not flight_data.get(
            "flight_date"
        ):

            raise ValueError(
                "Không tìm thấy ngày bay."
            )

        # --------------------------------------------------
        # Check duplicate Flight
        # --------------------------------------------------

        existing_flight = (
            FlightService.find_by_number_and_date(
                flight_data["flight_number"],
                flight_data["flight_date"]
            )
        )

        if existing_flight:

            raise ValueError(
                f"Chuyến bay "
                f"{flight_data['flight_number']} "
                f"ngày "
                f"{flight_data['flight_date']} "
                f"đã tồn tại."
            )

        # --------------------------------------------------
        # Create Flight
        # --------------------------------------------------

        flight = Flight(
            **flight_data
        )

        created_flight = (
            FlightService.create(
                flight
            )
        )

        if created_flight is None:

            raise RuntimeError(
                "Không thể tạo chuyến bay."
            )

        # --------------------------------------------------
        # Create Passengers
        # --------------------------------------------------

        passengers = []

        for _, row in passenger_df.iterrows():

            passenger_data = (
                ExcelService._map_row(
                    row,
                    PASSENGER_EXCEL_MAP
                )
            )

            # Skip empty passenger row

            if not passenger_data.get(
                "full_name"
            ):
                continue

            # ----------------------------------------------
            # Attach Flight ID
            # ----------------------------------------------

            passenger_data["flight_id"] = (
                created_flight.id
            )

            # ----------------------------------------------
            # Convert Date
            # ----------------------------------------------

            passenger_data[
                "date_of_birth"
            ] = ExcelService._get_date(
                passenger_data.get(
                    "date_of_birth"
                )
            )

            passenger_data[
                "document_expiry_date"
            ] = ExcelService._get_date(
                passenger_data.get(
                    "document_expiry_date"
                )
            )

            # ----------------------------------------------
            # Convert Integer
            # ----------------------------------------------

            passenger_data[
                "baggage_count"
            ] = ExcelService._get_int(
                passenger_data.get(
                    "baggage_count"
                )
            )

            # ----------------------------------------------
            # Gender
            # ----------------------------------------------

            passenger_data[
                "gender"
            ] = ExcelService._convert_gender(
                passenger_data.get(
                    "gender"
                )
            )

            # ----------------------------------------------
            # Create Model
            # ----------------------------------------------

            passengers.append(
                FlightPassenger(
                    **passenger_data
                )
            )

        # --------------------------------------------------
        # Insert Passengers
        # --------------------------------------------------

        created_passengers = (
            FlightPassengerService.create_many(
                passengers
            )
        )

        # --------------------------------------------------
        # Return result
        # --------------------------------------------------

        return {
            "flight": created_flight,
            "passenger_count": len(
                created_passengers
            )
        }

    # ==================================================
    # NORMALIZE DATAFRAME
    # ==================================================

    @staticmethod
    def _normalize_dataframe(
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe = dataframe.copy()

        dataframe.columns = [
            ExcelService._normalize_header(
                column
            )
            for column in dataframe.columns
        ]

        return dataframe

    # ==================================================
    # NORMALIZE HEADER
    # ==================================================

    @staticmethod
    def _normalize_header(
        value
    ) -> str:

        return (
            str(value)
            .strip()
            .replace("\n", " ")
            .replace("\r", " ")
        )

    # ==================================================
    # MAP EXCEL ROW -> MODEL DATA
    # ==================================================

    @staticmethod
    def _map_row(row, column_map: dict) -> dict:

        result = {}

        for excel_column, model_field in column_map.items():

            value = row.get(
                excel_column,
                ""
            )

            if pd.isna(value):
                value = ""

            result[model_field] = value

        return result

    # ==================================================
    # VALIDATE EXCEL COLUMNS
    # ==================================================

    @staticmethod
    def _validate_columns(
        dataframe: pd.DataFrame,
        column_map: dict
    ):

        required_columns = set(
            column_map.keys()
        )

        actual_columns = set(
            dataframe.columns
        )

        missing_columns = (
            required_columns
            - actual_columns
        )

        if missing_columns:

            raise ValueError(
                "Excel thiếu các cột: "
                + ", ".join(
                    sorted(missing_columns)
                )
            )

    # ==================================================
    # HELPERS
    # ==================================================

    @staticmethod
    def _get_string(
        value
    ) -> str:

        if value is None:
            return ""

        if pd.isna(value):
            return ""

        return str(value).strip()

    @staticmethod
    def _get_int(
        value
    ) -> int:

        if value is None:
            return 0

        if pd.isna(value):
            return 0

        try:

            return int(
                float(value)
            )

        except (
            ValueError,
            TypeError
        ):

            return 0

    @staticmethod
    def _get_date(
        value
    ) -> str:

        if value is None:
            return ""

        if value == "":
            return ""

        if pd.isna(value):
            return ""

        try:

            date = pd.to_datetime(
                value,
                dayfirst=True
            )

            return date.strftime(
                "%Y-%m-%d"
            )

        except (
            ValueError,
            TypeError
        ):

            return ""

    @staticmethod
    def _convert_gender(
        value
    ) -> str:

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
            "M": "Male",
            "F": "Female",
        }

        return mapping.get(
            gender,
            gender
        )
        
    # ==================================================
    # EXPORT RISK ALERTS
    # ==================================================

    @staticmethod
    def export_risk_alerts(
        alerts: list,
        file_path: str
    ):
        data = []

        for alert in alerts:
            data.append({
                "Flight": alert.flight_number,
                "Full Name": alert.full_name,
                "Passport": alert.passport_number,
                "Nationality": alert.nationality,
                "Date of Birth": alert.date_of_birth,
                "Gender": alert.gender,
                "Risk Level": alert.risk_level,
                "Risk Reason": alert.risk_reason,
                "Checked At": alert.created_at,
            })

        df = pd.DataFrame(data)

        df.to_excel(
            file_path,
            index=False,
            sheet_name="Risk Alerts"
        )