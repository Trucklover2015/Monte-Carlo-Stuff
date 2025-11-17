import requests as request
import pandas as pd
from io import StringIO

def fetch_ppg_table(year: int = 2025) -> pd.DataFrame:
    """
    Fetch and clean PF/PA from NFL.com league standings for a given year.
    Returns a DataFrame with:
        ['Team', 'PF_perG', 'PA_perG']
    """
    url = f"https://www.nfl.com/standings/league/{year}/reg"
    print(f"Fetching data from: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nfl.com/",
    }

    resp = request.get(url, headers=headers, timeout=15)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch {url}. Status code: {resp.status_code}"
        )

    html = resp.text

    tables = pd.read_html(StringIO(html))
    print(f"Found {len(tables)} tables on the page.")

    standings_df = None
    for t in tables:
        cols = [str(c) for c in t.columns]
        if "PF" in cols and "PA" in cols:
            standings_df = t
            break

    if standings_df is None:
        raise RuntimeError("Could not find a table with PF and PA on the NFL standings page.")

    df = standings_df
    ### print("Raw standings table head:")
    ### print(df.head())
    ### print("Raw columns:")
    ### print(df.columns)

    # Heuristic: first column is usually team text; may be named e.g. 'Team' or the division name
    team_col = df.columns[0]

    needed = ["PF", "PA"]
    for col in needed:
        if col not in df.columns:
            raise KeyError(f"Expected column '{col}' not found in standings table. Columns: {df.columns}")

    # W/L/T might not be present in all views, so handle gracefully
    w_col = "W" if "W" in df.columns else None
    l_col = "L" if "L" in df.columns else None
    t_col = "T" if "T" in df.columns else None

    out = df[[team_col] + [c for c in [w_col, l_col, t_col, "PF", "PA"] if c is not None]].copy()
    out = out.rename(columns={team_col: "Team"})

    # Clean up team text (strip spaces, convert to string)
    out["Team"] = out["Team"].astype(str).str.strip()

    # Convert numeric fields
    for col in [c for c in ["W", "L", "T", "PF", "PA"] if c in out.columns]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    # Compute games played
    if all(c in out.columns for c in ["W", "L", "T"]):
        out["Games"] = out["W"] + out["L"] + out["T"]
    else:
        out["Games"] = 17

    # Drop header/summary rows with NaNs or 0 games
    out = out.dropna(subset=["PF", "PA", "Games"])
    out = out[out["Games"] > 0].reset_index(drop=True)

    # Points per game
    out["PF_perG"] = out["PF"] / out["Games"]
    out["PA_perG"] = out["PA"] / out["Games"]

    ### print("\nCleaned PF/PA per-game table head:")
    ### print(out[["Team", "PF_perG", "PA_perG"]].head())

    return out[["Team", "PF_perG", "PA_perG"]]

def get_team_stats(df: pd.DataFrame, team_name: str) -> dict:
    """
    Given the cleaned PPG DataFrame and a team name, return that team's stats.

    Because NFL.com often has extra markers (x, z, *, etc.) or slightly different
    formatting, we do fuzzy matching:

      1) Exact match on full name (case-sensitive)
      2) Case-insensitive contains on full name
      3) Match on mascot (last word, e.g. 'Chiefs')
      4) Match on city/region (e.g. 'Kansas City')
    """
    team_name_clean = team_name.strip()
    teams_series = df["Team"].astype(str)

    row = df[teams_series == team_name_clean]
    teams_lower = teams_series.str.lower()
    name_lower = team_name_clean.lower()
    if row.empty:
        row = df[teams_lower.str.contains(name_lower, na=False)]
    if row.empty:
        parts = team_name_clean.split()
        if parts:
            mascot = parts[-1].lower()
            row = df[teams_lower.str.contains(mascot, na=False)]
    if row.empty and len(team_name_clean.split()) > 1:
        city = " ".join(team_name_clean.split()[:-1]).lower()
        row = df[teams_lower.str.contains(city, na=False)]
    if row.empty:
        print("\nAvailable teams in table (raw 'Team' column):")
        print(teams_series.tolist())
        raise ValueError(f"Team '{team_name}' not found in NFL standings table.")

    # If multiple rows match (e.g. weird header rows), just take first
    row = row.iloc[0]

    return {
        "team": row["Team"],
        "off_ppg": row["PF_perG"],
        "def_ppg_allowed": row["PA_perG"],
    }

def estimate_expected_points(team_off_ppg: float, opp_def_ppg_allowed: float) -> float:
    """
    Simple model: expected points is the average of a team's offensive PPG
    and the opponent's defensive PPG allowed.
    """
    return (team_off_ppg + opp_def_ppg_allowed) / 2.0

def get_expected_scores(team1_name: str, team2_name: str, year: int = 2025):
    """
    High-level helper: fetch league data from NFL.com, pull both teams' stats,
    and compute expected scores for each team.
    Returns (team1_expected, team2_expected, team1_stats, team2_stats).
    """
    df = fetch_ppg_table(year)

    team1_stats = get_team_stats(df, team1_name)
    team2_stats = get_team_stats(df, team2_name)

    team1_expected = estimate_expected_points(
        team1_stats["off_ppg"],
        team2_stats["def_ppg_allowed"],
    )
    team2_expected = estimate_expected_points(
        team2_stats["off_ppg"],
        team1_stats["def_ppg_allowed"],
    )

    return team1_expected, team2_expected, team1_stats, team2_stats

if __name__ == "__main__":
    df = fetch_ppg_table(2025)
    print("\nTeams found (raw 'Team' strings):")
    print(df["Team"].tolist())
