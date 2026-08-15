class RiskAlertStore:
    """
    Runtime storage for risk check results.

    Data is kept only during the current application session.
    Nothing is saved to the database.
    """

    def __init__(self):
        self._alerts = []

    # =========================================================
    # REPLACE ALERTS FOR ONE FLIGHT
    # =========================================================

    def replace_flight_alerts(
        self,
        flight_id: int,
        alerts: list
    ):
        """
        Replace all existing alerts belonging to flight_id.

        If the same flight is checked again, the old results
        are removed and replaced by the new results.

        Results of other flights are kept.
        """

        # Remove old alerts of this flight
        self._alerts = [
            alert
            for alert in self._alerts
            if self._get_flight_id(alert) != flight_id
        ]

        # Add new alerts
        if alerts:
            self._alerts.extend(alerts)

    # =========================================================
    # GET ALL
    # =========================================================

    def get_all(self) -> list:
        """
        Return all alerts in the current session.
        """

        return list(
            self._alerts
        )

    # =========================================================
    # GET BY FLIGHT
    # =========================================================

    def get_by_flight(
        self,
        flight_id: int
    ) -> list:

        return [
            alert
            for alert in self._alerts
            if self._get_flight_id(alert) == flight_id
        ]

    # =========================================================
    # COUNT
    # =========================================================

    def count(self) -> int:

        return len(
            self._alerts
        )

    # =========================================================
    # COUNT BY FLIGHT
    # =========================================================

    def count_by_flight(
        self,
        flight_id: int
    ) -> int:

        return len(
            self.get_by_flight(
                flight_id
            )
        )

    # =========================================================
    # REMOVE ONE FLIGHT
    # =========================================================

    def remove_flight(
        self,
        flight_id: int
    ):

        self._alerts = [
            alert
            for alert in self._alerts
            if self._get_flight_id(alert) != flight_id
        ]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):

        self._alerts.clear()

    # =========================================================
    # INTERNAL
    # =========================================================

    @staticmethod
    def _get_flight_id(
        alert
    ):

        # Support dataclass/object
        if hasattr(
            alert,
            "flight_id"
        ):
            return alert.flight_id

        # Support dict
        if isinstance(
            alert,
            dict
        ):
            return alert.get(
                "flight_id"
            )

        return None