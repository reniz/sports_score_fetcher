import unittest
from unittest.mock import patch, Mock
from sports_scores import TheSportsDBFree, SportsScoreFetcher, MatchFormatter


class TestSportsScoreFetcher(unittest.TestCase):

    def setUp(self):
        self.data_source = TheSportsDBFree(api_key="3")
        self.fetcher = SportsScoreFetcher(self.data_source)
        self.formatter = MatchFormatter()

    @patch('sports_scores.requests.get')
    def test_fetch_latest_match_success_no_date(self, mock_get):
        # Tests fetching the latest match when no date is provided
        mock_team_response = Mock()
        mock_team_response.status_code = 200
        mock_team_response.json.return_value = {
            "teams": [{"idTeam": "133604", "strTeam": "Arsenal"}]
        }
        mock_match_response = Mock()
        mock_match_response.status_code = 200
        mock_match_response.json.return_value = {
            "results": [{
                "strHomeTeam": "Arsenal",
                "strAwayTeam": "PSV Eindhoven",
                "intHomeScore": "2",
                "intAwayScore": "2",
                "dateEvent": "2025-03-12"
            }]
        }
        mock_get.side_effect = [mock_team_response, mock_match_response]

        result = self.fetcher.get_latest_match("Arsenal")  # No date
        expected = (
            "----------------------------------------\n"
            "Match: Arsenal vs PSV Eindhoven\n"
            "Score: 2 - 2\n"
            "Date: 2025-03-12\n"
            "----------------------------------------"
        )
        self.assertEqual(result, expected)

    @patch('sports_scores.requests.get')
    def test_fetch_latest_match_success_with_date(self, mock_get):
        # Tests fetching a match for a specific date
        mock_team_response = Mock()
        mock_team_response.status_code = 200
        mock_team_response.json.return_value = {
            "teams": [{"idTeam": "133604", "strTeam": "Arsenal"}]
        }
        mock_match_response = Mock()
        mock_match_response.status_code = 200
        mock_match_response.json.return_value = {
            "results": [
                {"strHomeTeam": "Arsenal", "strAwayTeam": "PSV Eindhoven",
                 "intHomeScore": "2", "intAwayScore": "2", "dateEvent": "2025-03-12"},
                {"strHomeTeam": "Arsenal", "strAwayTeam": "Dinamo Zagreb",
                 "intHomeScore": "3", "intAwayScore": "0", "dateEvent": "2025-01-22"}
            ]
        }
        mock_get.side_effect = [mock_team_response, mock_match_response]

        result = self.fetcher.get_latest_match("Arsenal", "2025-01-22")  # Specific date
        expected = (
            "----------------------------------------\n"
            "Match: Arsenal vs Dinamo Zagreb\n"
            "Score: 3 - 0\n"
            "Date: 2025-01-22\n"
            "----------------------------------------"
        )
        self.assertEqual(result, expected)

    @patch('sports_scores.requests.get')
    def test_fetch_latest_match_no_results(self, mock_get):
        # Tests error when no matches are found
        mock_team_response = Mock()
        mock_team_response.status_code = 200
        mock_team_response.json.return_value = {
            "teams": [{"idTeam": "133604", "strTeam": "Arsenal"}]
        }
        mock_match_response = Mock()
        mock_match_response.status_code = 200
        mock_match_response.json.return_value = {"results": []}
        mock_get.side_effect = [mock_team_response, mock_match_response]

        result = self.fetcher.get_latest_match("Arsenal")
        self.assertEqual(result, "Error: No recent matches found for this team in the free tier.")

    @patch('sports_scores.requests.get')
    def test_fetch_latest_match_date_not_found(self, mock_get):
        # Tests error when date is provided but no match exists on that date
        mock_team_response = Mock()
        mock_team_response.status_code = 200
        mock_team_response.json.return_value = {
            "teams": [{"idTeam": "133604", "strTeam": "Arsenal"}]
        }
        mock_match_response = Mock()
        mock_match_response.status_code = 200
        mock_match_response.json.return_value = {
            "results": [{
                "strHomeTeam": "Arsenal",
                "strAwayTeam": "PSV Eindhoven",
                "intHomeScore": "2",
                "intAwayScore": "2",
                "dateEvent": "2025-03-12"
            }]
        }
        mock_get.side_effect = [mock_team_response, mock_match_response]

        result = self.fetcher.get_latest_match("Arsenal", "2025-03-13")  # Date not in results
        self.assertEqual(result, "Error: No match found for Arsenal on 2025-03-13 in the last 5 home matches.")

    def test_format_match(self):
        # Tests formatting logic
        match_data = {
            "strHomeTeam": "Arsenal",
            "strAwayTeam": "PSV Eindhoven",
            "intHomeScore": "2",
            "intAwayScore": "2",
            "dateEvent": "2025-03-12"
        }
        result = self.formatter.format_match(match_data)
        expected = (
            "----------------------------------------\n"
            "Match: Arsenal vs PSV Eindhoven\n"
            "Score: 2 - 2\n"
            "Date: 2025-03-12\n"
            "----------------------------------------"
        )
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
