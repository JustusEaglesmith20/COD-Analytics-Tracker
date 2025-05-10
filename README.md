# 🎮 Dirty Mike & the Boys' COD Analytics Tool

Track Warzone match performance across your squad using a lightweight Streamlit app and Google Sheets as the backend database.

## 📌 What It Does

- Lets you and your teammates log in-game events like Gulag deaths, match wins/losses, or mid-game updates
- Logs are submitted through a structured form with conditional logic (only the relevant fields are shown based on input reason)
- Automatically appends data to a Google Sheet for permanent storage
- Designed to be fast, fun, and usable between matches on desktop or mobile

## 🧑‍💻 Supported Gamertags

Only the following tags can submit entries:
- `CozySun400`
- `ouTTaBubbleGum1`
- `Justus20`
- `rcloud14`

## 🧱 Data Fields Captured

| Field             | Description                               |
|------------------|-------------------------------------------|
| Timestamp         | ISO timestamp of submission               |
| Gamer Tag         | Selected user from list                   |
| Log Reason        | Reason for logging (Gulag, Win, etc.)     |
| Circle Stage      | Which circle it was at death              |
| Drop Location     | Initial landing spot                      |
| Death Location    | Where player died                         |
| Loadout           | Whether the player had their loadout      |
| Number of Kills   | Total kills at time of submission         |
| Alive             | Yes/No (for mid-game updates)             |
| Current Location  | Player’s current spot if still alive      |
| Cash              | Amount of money on-hand mid-game          |
| Death Reason      | Fun team-defined reasons for dying        |
| Loss Reason       | Team wipe cause                           |
| Damage Dealt      | Total team damage                         |
| Eliminations      | Total team elims                          |
| Total Kills       | Team kill count                           |
| Team Loss Location| Where the team got wiped                  |
| Victory Quote     | Custom quote if the team won              |

All fields not relevant to a submission are filled in as `"NA"`.

---

## 🚀 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cod-analytics-tracker.git
   cd cod-analytics-tracker
