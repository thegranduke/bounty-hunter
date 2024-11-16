# Bounty Hunter Docs

## Table of Contents

1. Introduction
2. Features
3. Getting Started
4. Configuration
5. How It Works
    - Key Functions
6. Usage
7. Email Notifications
8. Error Handling

---

## Introduction

Welcome to the **Bounty Hunter**! This Python script is your friendly companion for tracking open bounties on Replit. With its asynchronous web scraping capabilities, it fetches bounty information and sends email notifications for the latest opportunities. Whether you’re a developer hunting for gigs or just love the thrill of the chase, this tool is designed to make your bounty hunting experience smooth and enjoyable.

## Features

- **Asynchronous Bounty Fetching**: Efficiently scrape bounty data using Playwright.
- **Email Notifications**: Stay updated with the latest bounties delivered straight to your inbox.
- **Data Storage**: Keeps track of previously fetched bounties for easy comparison.
- **Error Handling**: Robust mechanisms to deal with common issues during execution.

## Getting Started

To set up the Bounty Hunter script, follow these simple steps:

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or later
- Pip (Python package installer)
- Playwright

### Installation

1. Clone the repository:
    
    ```bash
    git clone https://github.com/yourusername/bounty-hunter.git
    cd bounty-hunter
    ```
    
2. Install the required packages:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Set up your environment variables. Create a `.env` file in the project root with the following contents:
    
    ```
    env
    SENDER_EMAIL=your_email@example.com
    RECIPIENT_EMAIL=recipient_email@example.com
    SENDER_PASSWORD=your_email_password
    ```
    

## Configuration

The script uses environment variables for configuration, which are loaded using the `dotenv` package. Ensure you update your `.env` file with your email credentials.

- **SENDER_EMAIL**: Your email address from which notifications will be sent.
- **RECIPIENT_EMAIL**: The email address that will receive bounty notifications.
- **SENDER_PASSWORD**: The password for your email account.

### URL Configuration

The URL from which bounties are fetched is hardcoded in the script:

```python
url = 'https://replit.com/bounties?status=open&order=creationDateDescending'
```

You can modify this URL to point to different bounty listings or other pages as needed.

### Browser Configuration

The browser is set to run in headless mode by default, meaning it will operate without a graphical user interface (GUI):

```python
browser = await p.chromium.launch(headless=True)
```

If you want to run the browser in a visible mode for debugging or development, change `headless=True` to `headless=False`.

## How It Works

The Bounty Hunter script is organized into several key functions, each responsible for a specific part of the bounty hunting process.

### Key Functions

1. **`fetch_bounties()`**:
    - This asynchronous function is responsible for scraping bounty data from Replit. It launches a headless browser and navigates to the bounty listing page.
    - After loading the page, it waits for the bounty elements to appear, then retrieves information about the bounties, such as their ID, price, and description.
    - It processes the first 20 bounties found on the page and returns a list of dictionaries containing this information.
    
    ```python
    async def fetch_bounties():
        # Launch browser and fetch data
    ```
    
2. **`read_bounties_from_file()`**:
    - This function checks if a local file containing previously fetched bounties exists. If it does, it reads the JSON data and returns it as a Python list.
    - If the file does not exist, it returns an empty list.
    
    ```python
    def read_bounties_from_file():
        # Read stored bounty data from local file
    ```
    
3. **`write_bounties_to_file(bounty_data)`**:
    - This function writes the current bounty data to a local JSON file for future reference. It formats the data nicely with indentation for readability.
    
    ```python
    def write_bounties_to_file(bounty_data):
        # Save bounty data to a local file
    ```
    

1. **`main()`**:
    - The entry point of the script. It orchestrates the overall flow: starting the bounty fetching process, comparing current bounties with previously stored ones, and sending email notifications for any new bounties found. The script is set to run continuously every 15 minutes, allowing it to check for new bounties automatically.
    
    ```python
    async def main():
        # Control the flow of the bounty hunting process
    ```
    
- **Continuous Execution**:
    - The script runs indefinitely, executing the main function every 15 minutes. This is done using a `while True` loop combined with `asyncio.run(main())`. If an exception occurs, it will print an error message and continue to the next cycle after sleeping for 15 minutes.
    
    ```python
    if __name__ == "__main__":
        while True:
            try:
                asyncio.run(main())
            except Exception as e:
                print(f"Error in main loop: {e}")
            finally:
                print("Sleeping for 15 minutes...")
                time.sleep(900)
    ```
    

## Usage

Update the **Usage** section to indicate that the script now runs continuously:

To run the script, simply execute:

```bash
python bounty_hunter.py
```

The script will automatically fetch the latest bounties, compare them with the stored data, and send an email if there are any new bounties found. The script is designed to run continuously, checking for new bounties every 15 minutes.

## Email Notifications

Email notifications are sent using the `smtplib` library. The script constructs an email with the details of the latest bounty and sends it to the specified recipient.

### Note

Make sure that your email provider allows SMTP access and check the specific settings (like server and port) required for sending emails.

## Error Handling

The Bounty Hunter script includes basic error handling to catch common issues, such as:

- **Connection Errors**: If there are issues fetching data from the Replit website.
- **Email Errors**: Problems related to sending emails, such as authentication failures or server disconnections.

When an error occurs, the script prints a friendly message to help you diagnose the issue.

---

With the Bounty Hunter, you can to dive into the world of bounties with ease, let the hunt begin.
