import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Team_Abbreviations import resolve_team_name

from Data_Scraper import get_expected_scores

sns.set_style('whitegrid')


def monte_carlo(team1_name, team2_name, year=2025, num_simulations=10000, show_plot=True):
    team1_expected_score, team2_expected_score, team1_stats, team2_stats = \
        get_expected_scores(team1_name, team2_name, year=year)

    print("\nEstimated scoring based on stats:")
    print(f"{team1_stats['team']}: {team1_expected_score:.2f} points")
    print(f"{team2_stats['team']}: {team2_expected_score:.2f} points\n")

    team1_score = np.random.poisson(team1_expected_score, size=num_simulations)
    team2_score = np.random.poisson(team2_expected_score, size=num_simulations)

    team1_wins = np.sum(team1_score > team2_score)
    team2_wins = np.sum(team2_score > team1_score)
    tie = np.sum(team1_score == team2_score)

    team1_win_prob = team1_wins / num_simulations
    team2_win_prob = team2_wins / num_simulations
    tie_prob = tie / num_simulations

    print(f"{team1_name} win probability: {team1_win_prob:.3%}")
    print(f"{team2_name} win probability: {team2_win_prob:.3%}")
    print(f"Tie probability: {tie_prob:.3%}")

    if show_plot:
        plt.figure(figsize=(10, 5))
        plt.hist(team1_score, bins=range(0, 60), alpha=0.5, label=team1_name)
        plt.hist(team2_score, bins=range(0, 60), alpha=0.5, label=team2_name)
        plt.title("Simulated Score Distributions")
        plt.xlabel("Points Scored")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

    return {
        "team1_name": team1_name,
        "team2_name": team2_name,
        "team1_win_prob": team1_win_prob,
        "team2_win_prob": team2_win_prob,
        "tie_prob": tie_prob,
        "team1_scores": team1_score,
        "team2_scores": team2_score,
    }


if __name__ == "__main__":
    team1_raw = input("Enter Team 1 (full name or abbreviation): ")
    team2_raw = input("Enter Team 2 (full name or abbreviation): ")
    team1_name = resolve_team_name(team1_raw)
    team2_name = resolve_team_name(team2_raw)
    print(f"\nTeams selected: {team1_name} vs {team2_name}\n")

    monte_carlo(team1_name, team2_name, year=2025, num_simulations=10000, show_plot=True)
