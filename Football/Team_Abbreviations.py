# Team_Abbreviations.py

TEAM_ABBREVIATIONS = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB":  "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC":  "Kansas City Chiefs",
    "LV":  "Las Vegas Raiders",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE":  "New England Patriots",
    "NO":  "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SF":  "San Francisco 49ers",
    "SEA": "Seattle Seahawks",
    "TB":  "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders",
}


def resolve_team_name(user_input: str) -> str:
    """
    Convert user input into a full team name.
    Accepts:
      - Abbreviations (KC, BUF, DAL, etc.)
      - Exact full names (Kansas City Chiefs, etc.)
    """
    ui = user_input.strip().upper()

    if ui in TEAM_ABBREVIATIONS:
        return TEAM_ABBREVIATIONS[ui]

    formatted = user_input.strip().title()
    if formatted in TEAM_ABBREVIATIONS.values():
        return formatted

    raise ValueError(
        f"'{user_input}' is not a valid team name or abbreviation.\n"
        f"Valid abbreviations are:\n{', '.join(sorted(TEAM_ABBREVIATIONS.keys()))}"
    )