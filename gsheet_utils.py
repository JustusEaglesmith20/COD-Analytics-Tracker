import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def get_worksheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(st.secrets["gsheet"]["spreadsheet_url"])
    return sheet.sheet1

def append_row_to_gsheet(data: dict):
    worksheet = get_worksheet()
    headers = list(data.keys())
    row = [data.get(col, "") for col in headers]

    existing = worksheet.get_all_values()

    if not existing:  # Sheet is empty
        worksheet.append_row(headers)

    # Optional: re-check header match before appending
    elif existing[0] != headers:
        st.warning("⚠️ Header mismatch — check your Google Sheet structure.")
        return

    worksheet.append_row(row)

