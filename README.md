# Simple Sports Score Fetcher (TheSportsDB)

A Python script to fetch and display the latest football match results for a specific team using the free TheSportsDB API (V1).

## Requirements
- Python 3.8+
- Libraries: `requests`
- No API key required (uses free test key "3")

## Setup
1. **Clone the Repository:**
   git clone <repository-url>
   cd sports_score_fetcher

2.**Install Dependencies:**
   pip install -r requirements.txt


## Usage
Run the script and follow the prompts:

python sports_scores.py

Enter a team name (e.g., "Arsenal").
Optionally, enter a date (e.g., "2023-10-10") for specific results.

Example Output 

Welcome to the Sports Score Fetcher (TheSportsDB)!
Enter team name (e.g., Arsenal): Arsenal
Enter date (YYYY-MM-DD) or press Enter for latest: 
----------------------------------------
Match: Arsenal vs Chelsea
Score: 2 - 1
Date: 2023-10-10
----------------------------------------


Running Tests

python -m unittest test_sports_scores.py


