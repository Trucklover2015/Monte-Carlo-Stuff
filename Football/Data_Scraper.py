import requests as request
import pandas as pd


def fetch_ppg_table(year=2025):
    """
    Fetch and clean the points-per-game table from Pro-Football-Reference
    for a given year. Returns a DataFrame with columns:
    ['Team', 'PF_perG', 'PA_perG'].
    """
    url = f"https://www.pro-football-reference.com/years/{year}/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = request.get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch {url}. Status code: {response.status_code}"
        )

    tables = pd.read_html(response.text)
    print(f"Found {len(tables)} tables on the page.")

    df = tables[0]
    print("Raw table head:")
    print(df.head())
    print("Raw columns:")
    print(df.columns)

    # Map the original columns to standardized names
    column_mapping = {}

    # Team column can be 'Tm' or 'Team'
    if 'Tm' in df.columns:
        column_mapping['Tm'] = 'Team'
    elif 'Team' in df.columns:
        column_mapping['Team'] = 'Team'
    else:
        raise KeyError("Could not find 'Tm' or 'Team' column in table.")

    # Points for per game
    if 'Pts/G' in df.columns:
        column_mapping['Pts/G'] = 'PF_perG'
    else:
        raise KeyError("Could not find 'Pts/G' column in table.")

    # Points allowed per game
    if 'Opp Pts/G' in df.columns:
        column_mapping['Opp Pts/G'] = 'PA_perG'
    else:
        raise KeyError("Could not find 'Opp Pts/G' column in table.")

    df = df.rename(columns=column_mapping)

    needed_cols = ['Team', 'PF_perG', 'PA_perG']
    df = df[needed_cols]

    # Ensure numeric
    df['PF_perG'] = pd.to_numeric(df['PF_perG'], errors='coerce')
    df['PA_perG'] = pd.to_numeric(df['PA_perG'], errors='coerce')

    # Drop rows with missing values (like headers/subtotals)
    df = df.dropna(subset=['PF_perG', 'PA_perG']).reset_index(drop=True)

    print("\nCleaned PPG table head:")
    print(df.head())

    return df


def get_team_stats(df, team_name):
    """
    Given the cleaned PPG DataFrame and a team name, return that team's stats.
    """
    row = df[df['Team'] == team_name]
    if row.empty:
        raise ValueError(f"Team '{team_name}' not found. Check spelling or team list.")
    row = row.iloc[0]
    return {
        'team': team_name,
        'off_ppg': row['PF_perG'],
        'def_ppg_allowed': row['PA_perG']
    }


def estimate_expected_points(team_off_ppg, opp_def_ppg_allowed):
    """
    Simple model: expected points is the average of a team's offensive PPG
    and the opponent's defensive PPG allowed.
    """
    return (team_off_ppg + opp_def_ppg_allowed) / 2.0


def get_expected_scores(team1_name, team2_name, year=2025):
    """
    High-level helper: fetch league data, pull both teams' stats,
    and compute expected scores for each team.
    Returns (team1_expected, team2_expected, team1_stats, team2_stats).
    """
    df = fetch_ppg_table(year)

    team1_stats = get_team_stats(df, team1_name)
    team2_stats = get_team_stats(df, team2_name)

    team1_expected = estimate_expected_points(
        team1_stats['off_ppg'],
        team2_stats['def_ppg_allowed']
    )
    team2_expected = estimate_expected_points(
        team2_stats['off_ppg'],
        team1_stats['def_ppg_allowed']
    )

    return team1_expected, team2_expected, team1_stats, team2_stats


# Optional: quick test if you run this file directly
if __name__ == "__main__":
    df = fetch_ppg_table(2025)
    print(df['Team'].tolist())
