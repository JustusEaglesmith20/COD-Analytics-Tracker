import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("Dirty Mike & the Boys' COD Analytics Tool")

# --- Gamer Tag Selection ---
gamer_tag = st.selectbox(
    "Select your Gamer Tag:",
    ["Select...", "CozySun400", "ouTTaBubbleGum1", "Justus20", "rcloud14"]
)

# --- Input Reason Selection (appears only after gamer tag is selected) ---
if gamer_tag != "Select...":
    log_reason = st.selectbox("Input Reason", ["Select...", "Death/Gulag", "Team Wipe/Game Lost", "Game Won"])
else:
    st.warning("Please select your gamer tag to begin.")
    log_reason = "Select..."

data = {}
submit = False

# --- Form (only shows when both gamer_tag and log_reason are selected) ---
if log_reason != "Select...":
    with st.form("game_form"):
        if log_reason == "Death/Gulag":
            circle_stage = st.number_input("Circle Stage (Number)", min_value=0)
            drop_location = st.selectbox("Original Drop Location", [
                "Airport", "Boneyard", "Dam", "Downtown", "Farmland", "Hills", "Hospital", "Lumber",
                "Military Base", "Park", "Port", "Prison", "Promenade East", "Promenade West", "Quarry",
                "Stadium", "Storage Town", "Superstore", "Train Station", "TV Station"
            ])
            death_location = st.selectbox("Death Location", [
                "Airport", "Boneyard", "Dam", "Downtown", "Farmland", "Hills", "Hospital", "Lumber",
                "Military Base", "Park", "Port", "Prison", "Promenade East", "Promenade West", "Quarry",
                "Stadium", "Storage Town", "Superstore", "Train Station", "TV Station"
            ])
            loadout = st.selectbox("Loadout?", ["Yes", "No"])
            number_kills = st.number_input("Your Total Kills", min_value=0)

            submit = st.form_submit_button("Submit")
            if submit:
                data = {
                    "Circle Stage": circle_stage,
                    "Drop Location": drop_location,
                    "Death Location": death_location,
                    "Loadout": loadout,
                    "Number of Kills": number_kills,
                }

        elif log_reason == "Team Wipe/Game Lost":
            loss_reason = st.selectbox("Loss Reason", [
                "Justus said, 'Let's play slow' then pushed a 1v4 and said 'My bad y'all.'",
                "Oh fuck oh fuck on me on me on me! He's cracked, he's soooo bad, fuck!... WILL, WHERE WERE YOU?? GOD DAMNIT!",
                "Will shot everything but the enemy.",
                "Ryan got shot out of the air."
            ])
            damage_dealt = st.number_input("Your Total Damage Dealt", min_value=0)
            eliminations = st.number_input("Your Total Eliminations", min_value=0)
            kills = st.number_input("Your Total Kills", min_value=0)
            team_loss_location = st.selectbox("Team Loss Location", [
                "Airport", "Boneyard", "Dam", "Downtown", "Farmland", "Hills", "Hospital", "Lumber",
                "Military Base", "Park", "Port", "Prison", "Promenade East", "Promenade West", "Quarry",
                "Stadium", "Storage Town", "Superstore", "Train Station", "TV Station"
            ])

            submit = st.form_submit_button("Submit")
            if submit:
                data = {
                    "Loss Reason": loss_reason,
                    "Damage Dealt": damage_dealt,
                    "Eliminations": eliminations,
                    "Total Kills": kills,
                    "Team Loss Location": team_loss_location
                }

        elif log_reason == "Game Won":
            win_quote = st.text_input("Victory Quote (optional)", "You probably got one more in ya.")
            last_circle_location = st.selectbox("Last Circle Locaiton", [
                "Airport", "Boneyard", "Dam", "Downtown", "Farmland", "Hills", "Hospital", "Lumber",
                "Military Base", "Park", "Port", "Prison", "Promenade East", "Promenade West", "Quarry",
                "Stadium", "Storage Town", "Superstore", "Train Station", "TV Station"
            ])
            damage_dealt = st.number_input("Your Total Damage Dealt", min_value=0)
            eliminations = st.number_input("Your Total Eliminations", min_value=0)
            kills = st.number_input("Your Total Kill Count", min_value=0)
            submit = st.form_submit_button("Submit")
            if submit:
                data = {
                    "Victory Quote": win_quote
                }

# --- Save to Google Sheet ---
if submit and data:
    column_template = {
        "Circle Stage": "NA", "Drop Location": "NA", "Death Location": "NA",
        "Loadout": "NA", "Number of Kills": "NA", "Alive": "NA",
        "Current Location": "NA", "Cash": "NA", "Death Reason": "NA",
        "Loss Reason": "NA", "Damage Dealt": "NA", "Eliminations": "NA",
        "Total Kills": "NA", "Team Loss Location": "NA", "Victory Quote": "NA"
    }

    final_data = {
        "Timestamp": datetime.now().isoformat(),
        "Gamer Tag": gamer_tag,
        "Log Reason": log_reason,
        **{k: data.get(k, default) for k, default in column_template.items()}
    }

    # Google Sheets API
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(st.secrets["gsheet"]["spreadsheet_url"])
    worksheet = sheet.sheet1

    headers = list(final_data.keys())
    row = [final_data.get(col, "NA") for col in headers]

    if not worksheet.get_all_values():
        worksheet.append_row(headers)

    worksheet.append_row(row)
    st.success("Data Logged to Google Sheet — LOCK IN!!!")
