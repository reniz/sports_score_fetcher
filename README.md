# Simple Sports Score Fetcher 

A Python script to fetch and display the latest football match results for a specific team using the free TheSportsDB API (V1).

## Requirements
- Python 3.8+
- Libraries: `requests`
- No API key required (uses free test key "3")

## Setup
1. **Clone the Repository:**
   git clone <repository-url>
   cd sports_score_fetcher

2. **Install Dependencies:**
    pip install -r requirements.txt


## Usage
Run the script and follow the prompts:

python sports_scores.py

Enter a team name (e.g., "Arsenal").
Optionally, enter a date (e.g., "2023-10-10") for specific results.

## Example Output 
   
**Welcome to the Sports Score Fetcher (TheSportsDB)!**

**Enter team name (e.g., Arsenal): Arsenal**

**Enter date (YYYY-MM-DD) or press Enter for latest:**

**Match: Arsenal vs Chelsea**

**Score: 2 - 1**

**Date: 2023-10-10**



## Running Tests

python -m unittest test_sports_scores.py


## Future Improvements
Here are potential enhancements to extend the project’s functionality, robustness, and usability:

**Enhanced Error Handling**

Add handling for malformed API responses (e.g., invalid JSON) and rate limit errors (HTTP 429), displaying clear, user-friendly messages instead of silent failures.

**Support for Other Sports**

Extend the script to fetch scores for sports like basketball or tennis by allowing users to specify a sport type and adapting TheSportsDB API endpoints accordingly.

**Graphical User Interface (GUI)**

Develop a simple GUI using tkinter (Python standard library) to replace the CLI, making it more accessible with input fields and buttons.

**Custom Date Range**

Allow users to enter a date range (e.g., "2023-10-01 to 2023-10-10") to fetch and display results for multiple matches, enhancing the single-date feature.

**League Support**

Add support for fetching the latest match by league (e.g., "Premier League") using TheSportsDB’s eventsseason.php endpoint, completing the "team or league" task option.

**Multiple API Support**

Introduce alternative APIs (e.g., API-Football) via new SportsDataSource subclasses, letting users choose their data source for greater flexibility.

**Caching**

Cache API results in memory (e.g., using functools.lru_cache) to speed up repeated queries and reduce API load.

**Additional Test Cases**

Expand unit tests to cover edge cases like invalid date formats, network timeouts, and unexpected API responses, ensuring full reliability.


