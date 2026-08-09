# ============================================================
# Risk Profile - Table Columns
# ============================================================

RISK_PROFILE_COLUMNS = [
    {
        "field": "full_name",
        "title": "Full Name",
    },
    {
        "field": "passport_number",
        "title": "Passport",
    },
    {
        "field": "nationality",
        "title": "Nationality",
    },
    {
        "field": "date_of_birth",
        "title": "Date of Birth",
    },
    {
        "field": "gender",
        "title": "Gender",
    },
    {
        "field": "flight_count",
        "title": "Flight Count",
    },
    {
        "field": "baggage_card_count",
        "title": "Baggage Cards",
    },
    {
        "field": "risk_level",
        "title": "Risk Level",
    },
]


# ============================================================
# Flight - Table Columns
# ============================================================

FLIGHT_COLUMNS = [
    {
        "field": "flight_number",
        "title": "Flight",
    },
    {
        "field": "airline",
        "title": "Airline",
    },
    {
        "field": "flight_date",
        "title": "Flight Date",
    },
    {
        "field": "origin",
        "title": "Origin",
    },
    {
        "field": "destination",
        "title": "Destination",
    },
    {
        "field": "route",
        "title": "Route",
    },
    {
        "field": "transit",
        "title": "Transit",
    },
]


# ============================================================
# Flight Passenger - Table Columns
# ============================================================

FLIGHT_PASSENGER_COLUMNS = [
    {
        "field": "full_name",
        "title": "Full Name",
    },
    {
        "field": "gender",
        "title": "Gender",
    },
    {
        "field": "nationality",
        "title": "Nationality",
    },
    {
        "field": "date_of_birth",
        "title": "Date of Birth",
    },
    {
        "field": "document_type",
        "title": "Document Type",
    },
    {
        "field": "document_number",
        "title": "Document Number",
    },
    {
        "field": "seat_number",
        "title": "Seat",
    },
    {
        "field": "origin",
        "title": "Origin",
    },
    {
        "field": "destination",
        "title": "Destination",
    },
    {
        "field": "baggage_count",
        "title": "Baggage",
    },
]


# ============================================================
# Excel Sheet Configuration
# ============================================================

EXCEL_SHEET_CONFIG = {
    "flight": {
        "name": "Chuyen bay",
        "header": 2,
    },

    "passenger": {
        "name": "Hành khách",
        "header": 2,
    },
}


# ============================================================
# Excel -> Flight Model Mapping
# ============================================================

FLIGHT_EXCEL_MAP = {
    "Số chuyến bay": "flight_number",
    "Hãng vận chuyển": "airline",
    "Ngày bay": "flight_date",
    "Nơi đi": "origin",
    "Nơi đến": "destination",
    "Đường bay": "route",
    "Nơi quá cảnh": "transit",
}


# ============================================================
# Excel -> FlightPassenger Model Mapping
# ============================================================

PASSENGER_EXCEL_MAP = {
    "Số ghế": "seat_number",
    "Họ và tên": "full_name",
    "Giới tính": "gender",
    "Quốc tịch": "nationality",
    "Ngày sinh": "date_of_birth",
    "Loại giấy tờ": "document_type",
    "Số giấy tờ": "document_number",
    "Nơi cấp": "issuing_country",
    "Quốc gia cư trú": "residence_country",
    "Nơi đi": "origin",
    "Nơi đến": "destination",
    "Cảng hàng không đầu tiên": "first_airport",
    "Hành lý": "baggage_count",
    "Ngày hết hạn": "document_expiry_date",
}