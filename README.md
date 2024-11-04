# Bounty Fetcher

A Python script designed to fetch and track open bounties on Replit's bounty page. Leveraging Playwright for headless browsing, it identifies new bounties, saves them to a local file, and prints fresh opportunities directly to your console.

## Table of Contents

- [Features](https://www.notion.so/Readmes-134fd8aef4bd80fa96b9d1cc39a037fa?pvs=21)
- [Installation](https://www.notion.so/Readmes-134fd8aef4bd80fa96b9d1cc39a037fa?pvs=21)
- [Usage](https://www.notion.so/Readmes-134fd8aef4bd80fa96b9d1cc39a037fa?pvs=21)
- [Configuration](https://www.notion.so/Readmes-134fd8aef4bd80fa96b9d1cc39a037fa?pvs=21)
- [Contributing](https://www.notion.so/Readmes-134fd8aef4bd80fa96b9d1cc39a037fa?pvs=21)
- [License](https://www.notion.so/Readmes-134fd8aef4bd80fa96b9d1cc39a037fa?pvs=21)

---

### Features

- **Automated Bounty Fetching:** Scans the Replit bounties page and fetches details of available bounties.
- **Data Persistence:** Stores bounty data in a local JSON file (`bounties.json`) for easy tracking and comparison.
- **Efficient Tracking of New Bounties:** Compares newly fetched data with previously saved data and highlights any new bounties.
- **Error Handling:** Captures and logs errors, with an optional screenshot for debugging.

---

### Installation

1. **Clone the Repository:**
    
    ```bash
    
    git clone https://github.com/yourusername/bounty-fetcher.git
    cd bounty-fetcher
    ```
    
2. **Install Dependencies:**
Ensure you have Python 3.7+ and install the required packages:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Install Playwright:**
    
    ```bash
    playwright install
    ```
    

---

### Usage

1. **Run the Script:**
Start the script to begin fetching open bounties:
    
    ```bash
    python bounty_fetcher.py
    ```
    
2. **Outputs:**
    - The console will print any new bounties found.
    - The `bounties.json` file will update with the latest bounty data for easy tracking.

---

### How It Works

The main functionality of this script is defined across three key functions:

1. **fetch_bounties():**
    - Opens a headless Chromium browser, navigates to the Replit bounties page, and waits for the bounty elements to load.
    - Fetches data from the first 20 bounty listings, capturing the bounty ID, price, and description.
    - Returns a list of bounties as dictionaries.
2. **read_bounties_from_file():**
    - Reads previously saved bounties from `bounties.json`.
    - Returns an empty list if no file exists.
3. **write_bounties_to_file():**
    - Writes the provided list of bounties to `bounties.json`.
4. **main():**
    - The primary function that orchestrates bounty fetching, comparing, and output.
    - Displays any new bounties found and saves the latest data for future runs.

---

### Configuration

The script is designed to run in its default state without any additional configuration. However, you may customize these aspects:

- **URL**: The script currently fetches data from `https://replit.com/bounties?status=open&order=creationDateDescending`. Change the URL inside `fetch_bounties()` if needed.
- **Headless Mode**: By default, the browser runs headlessly (invisible). To view the scraping in real time, set `headless=False` in the `launch` method in `fetch_bounties()`.

---

### Contributing

Contributions are welcome! Please submit a pull request with any features or bug fixes. Make sure your code adheres to the existing style and includes relevant comments.
