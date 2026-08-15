from datetime import datetime

from services.supabase_service import SupabaseService
from services.flight_passenger_service import FlightPassengerService

from models.flight_passenger import FlightPassenger
from models.risk_alert import RiskAlert
from models.risk_profile import RiskProfile


class RiskCheckService:

    RISK_PROFILE_TABLE = "risk_profiles"

    def __init__(
        self,
        alert_store
    ):

        self.alert_store = alert_store

    # =========================================================
    # CHECK FLIGHT
    # =========================================================

    def check_flight(
        self,
        flight
    ) -> list[RiskAlert]:

        passengers = (
            FlightPassengerService.get_by_flight(
                flight.id
            )
        )

        risk_profiles = (
            self._get_active_risk_profiles()
        )

        alerts = []

        # -----------------------------------------------------
        # Check every passenger
        # -----------------------------------------------------

        for passenger in passengers:

            matched_profiles = (
                self._find_matches(
                    passenger,
                    risk_profiles
                )
            )

            for profile in matched_profiles:

                alert = self._create_alert(
                    flight,
                    passenger,
                    profile
                )

                alerts.append(
                    alert
                )

        # -----------------------------------------------------
        # IMPORTANT
        #
        # Replace old result of this flight.
        #
        # This prevents duplicate alerts when the same
        # flight is checked multiple times.
        #
        # Alerts from other flights remain untouched.
        # -----------------------------------------------------

        self.alert_store.replace_flight_alerts(
            flight.id,
            alerts
        )

        return alerts

    # =========================================================
    # GET RISK PROFILES
    # =========================================================

    def _get_active_risk_profiles(
        self
    ) -> list[RiskProfile]:

        client = (
            SupabaseService.get_client()
        )

        response = (
            client
            .table(
                self.RISK_PROFILE_TABLE
            )
            .select("*")
            .eq(
                "active",
                True
            )
            .execute()
        )

        return [
            RiskProfile.from_dict(row)
            for row in response.data
        ]

    # =========================================================
    # MATCH
    # =========================================================

    def _find_matches(
        self,
        passenger: FlightPassenger,
        profiles: list[RiskProfile]
    ) -> list[RiskProfile]:

        matches = []

        for profile in profiles:

            if self._is_match(
                passenger,
                profile
            ):

                matches.append(
                    profile
                )

        return matches

    # =========================================================
    # MATCH LOGIC
    # =========================================================

    def _is_match(
        self,
        passenger: FlightPassenger,
        profile: RiskProfile
    ) -> bool:

        # -----------------------------------------------------
        # Passport number
        # -----------------------------------------------------

        passenger_passport = (
            self._normalize(
                passenger.document_number
            )
        )

        profile_passport = (
            self._normalize(
                profile.passport_number
            )
        )

        if (
            passenger_passport
            and
            profile_passport
            and
            passenger_passport
            == profile_passport
        ):

            return True

        # -----------------------------------------------------
        # Full name + Date of Birth
        # -----------------------------------------------------

        passenger_name = (
            self._normalize_name(
                passenger.full_name
            )
        )

        profile_name = (
            self._normalize_name(
                profile.full_name
            )
        )

        passenger_dob = (
            self._normalize(
                passenger.date_of_birth
            )
        )

        profile_dob = (
            self._normalize(
                profile.date_of_birth
            )
        )

        if (
            passenger_name
            and
            profile_name
            and
            passenger_name
            == profile_name
            and
            passenger_dob
            and
            profile_dob
            and
            passenger_dob
            == profile_dob
        ):

            return True

        return False

    # =========================================================
    # CREATE ALERT
    # =========================================================

    def _create_alert(
        self,
        flight,
        passenger: FlightPassenger,
        profile: RiskProfile
    ) -> RiskAlert:

        reason = (
            profile.risk_reason
            or
            "Passenger matched risk profile."
        )

        return RiskAlert(

            flight_id=(
                flight.id
            ),

            flight_number=(
                flight.flight_number
            ),

            passenger_id=(
                passenger.id
            ),

            full_name=(
                passenger.full_name
            ),

            passport_number=(
                passenger.document_number
            ),

            nationality=(
                passenger.nationality
            ),

            date_of_birth=(
                passenger.date_of_birth
            ),

            gender=(
                passenger.gender
            ),

            risk_level=(
                profile.risk_level
                or "Low"
            ),

            risk_reason=(
                reason
            ),

            created_at=(
                datetime.now().isoformat()
            ),
        )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _normalize(
        value
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        ).strip().upper()

    @staticmethod
    def _normalize_name(
        value
    ) -> str:

        if value is None:
            return ""

        return " ".join(
            str(value)
            .strip()
            .upper()
            .split()
        )