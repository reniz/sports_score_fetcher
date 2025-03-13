import requests
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Optional
import logging

# Set up logging to a file
logging.basicConfig(filename='sports_scores.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')


# --- Abstract Data Source Interface ---
class SportsDataSource(ABC):
    @abstractmethod
    def fetch_latest_match(self, team: str) -> Dict:
        pass


# --- Concrete TheSportsDB Data Source (Free Tier) ---
class TheSportsDBFree(SportsDataSource):
    def __init__(self, api_key: str = "3"):
        self.api_key = api_key
        self.base_url = "https://www.thesportsdb.com/api/v1/json"

    def fetch_latest_match(self, team: str) -> Dict:
        if not team:
            raise ValueError("Team name is required")

        try:
            team_id = self._get_team_id(team)
            url = f"{self.base_url}/{self.api_key}/eventslast.php"
            params = {"id": team_id}
            logging.info(f"Fetching from: {url} with params: {params}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.info(f"API Response: {data}")
            print(f"API Response logged to sports_scores.log")

            if not data.get("results"):  # Check 'results' instead of 'events'
                raise ValueError("No recent matches found for this team in the free tier.")

            return data["results"][0]  # Return the most recent match

        except requests.Timeout:
            raise ConnectionError("Request timed out after 10 seconds")
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch data: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))

    def _get_team_id(self, team_name: str) -> str:
        url = f"{self.base_url}/{self.api_key}/searchteams.php"
        response = requests.get(url, params={"t": team_name}, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Team Search Response: {data}")

        if not data["teams"]:
            raise ValueError(f"Team {team_name} not found")
        return data["teams"][0]["idTeam"]


# --- Display Formatter ---
class MatchFormatter:
    @staticmethod
    def format_match(match_data: Dict) -> str:
        home_team = match_data["strHomeTeam"]
        away_team = match_data["strAwayTeam"]
        home_score = match_data.get("intHomeScore", "N/A")
        away_score = match_data.get("intAwayScore", "N/A")
        score = f"{home_score} - {away_score}"
        date = match_data["dateEvent"]
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

        return (
            f"{'-' * 40}\n"
            f"Match: {home_team} vs {away_team}\n"
            f"Score: {score}\n"
            f"Date: {formatted_date}\n"
            f"{'-' * 40}"
        )


# --- Main Application Class ---
class SportsScoreFetcher:
    def __init__(self, data_source: SportsDataSource):
        self.data_source = data_source
        self.formatter = MatchFormatter()

    def get_latest_match(self, team: str) -> str:
        try:
            match_data = self.data_source.fetch_latest_match(team)
            return self.formatter.format_match(match_data)
        except (ValueError, ConnectionError) as e:
            return f"Error: {str(e)}"


# --- Command-Line Interface ---
def main():
    data_source = TheSportsDBFree(api_key="3")
    fetcher = SportsScoreFetcher(data_source)

    print("Welcome to the Sports Score Fetcher (TheSportsDB Free Tier)!")
    print("Note: Shows latest home match from the last 5 available in free tier.")
    team = input("Enter team name (e.g., Arsenal): ").strip()

    result = fetcher.get_latest_match(team=team)
    print(result)
    print("Check 'sports_scores.log' for full API responses.")


if __name__ == "__main__":
    main()