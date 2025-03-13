import unittest
from unittest.mock import patch, Mock
from sports_scores import TheSportsDBFree, SportsScoreFetcher, MatchFormatter


class TestSportsScoreFetcher(unittest.TestCase):

    def setUp(self):
        self.data_source = TheSportsDBFree(api_key="3")
        self.fetcher = SportsScoreFetcher(self.data_source)
        self.formatter = MatchFormatter()

    @patch('sports_scores.requests.get')
    def test_fetch_latest_match_success(self, mock_get):
        # Mock team ID response
        mock_team_response = Mock()
        mock_team_response.status_code = 200
        mock_team_response.json.return_value = {
            "teams": [{"idTeam": "133604", "strTeam": "Arsenal"}]
        }

        # Mock match data response
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

        # Simulate two API calls: team search, then match fetch
        mock_get.side_effect = [mock_team_response, mock_match_response]

        result = self.fetcher.get_latest_match("Arsenal")
        expected = (
            "----------------------------------------\n"
            "Match: Arsenal vs PSV Eindhoven\n"
            "Score: 2 - 2\n"
            "Date: 2025-03-12\n"
            "----------------------------------------"
        )
        self.assertEqual(result, expected)

    @patch('sports_scores.requests.get')
    def test_fetch_latest_match_no_results(self, mock_get):
        # Mock team ID response
        mock_team_response = Mock()
        mock_team_response.status_code = 200
        mock_team_response.json.return_value = {
            "teams": [{"idTeam": "133604", "strTeam": "Arsenal"}]
        }

        # Mock empty match data response
        mock_match_response = Mock()
        mock_match_response.status_code = 200
        mock_match_response.json.return_value = {"results": []}

        mock_get.side_effect = [mock_team_response, mock_match_response]

        result = self.fetcher.get_latest_match("Arsenal")
        self.assertEqual(result, "Error: No recent matches found for this team in the free tier.")

    def test_format_match(self):
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