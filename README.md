# Ethereum Blockchain Block Crawler 💎

This Block Crawler is intended to retrieve Ethereum Mainnet transactions within a given block range, write them to a SQLite database, and then query for the block that had the largest volume of Ether transferred between 2024-01-01 00:00:00 and 2024-01-01
00:30:00

## Features ✨

-   Retrieves Ethereum Mainnet transactions
-   Writes transactions to a SQLite database for storage
-   Queries the database to find the block with the largest volume of Ether transferred
-   Provides results in both the terminal and in a `.txt` file

## Getting Started 🛠️

### Prerequisites

Make sure the following are installed first:

-   Python 3
-   pip (python package manager)

### Backend Setup

1. **Activate Python Virtual Environment (Optional):** I recommend activating a Python virtual environment (I used Python 3.12.2). If you don't have one, you can create one by running the following command in the root directory:

    ```bash
    python3 -m venv venv
    ```

    then activate it by running:

    ```bash
    source venv/bin/activate  # For Unix/Linux
    venv\Scripts\activate     # For Windows
    ```

    If everything works out, you should see something like this in your terminal:

    ```bash
    (.venv) arianna@Ariannas-MBP
    ```

2. **Install Dependencies:** Then you should install the required Python dependencies:

    ```bash
    python3 -m pip install -r requirements.txt
    ```

3. **Run the `main.py` file**: Now all you have to do is run the command below and you're all set! But make sure to replace the JSON-RPC endpoint url, SQLite database name, and block range with your own values and the correct block range: 18908800-18909050

    ```bash
    python3 main.py \
    https://rpc.quicknode.pro/key \
    ethereum.sqlite3 \
    200-300
    ```

    If everything works out, you should see something like this in your terminal. The output should also appear inside of your newly created `largest_volume_of_ether.txt` file as well

    ```bash
    Block that had the largest volume of Ether transferred between the specified time range

    +----------------+-------------------------+
    |   block_number |   total_volume_of_ether |
    |----------------+-------------------------|
    |       18909040 |                 24636.4 |
    +----------------+-------------------------+

    Result saved to largest_volume_of_ether.txt
    ```

## Note 📝

-   You can run this command if you're unsure what each input argument means, or if you just want more context

    ```bash
    (venv) arianna@Ariannas-MBP ~ % python3 main.py -h
    usage: main.py [-h] json_rpc_endpoint sqlite_file block_range

    Block Crawler that retrieves Ethereum Mainnet transactions within a given block range, writes them to a database, and queries for the block that had the largest volume of ether transferred between 2024-01-01 00:00:00         and 2024-01-01 00:30:00

    positional arguments:
    json_rpc_endpoint  A JSON-RPC endpoint to call an Ethereum client, (ex. https://rpc.quicknode.pro/key)
    sqlite_file        Path to the SQLite file to write to, (ex. db.sqlite3)
    block_range        A block range formatted as 'start-end', (ex. 200-300)

    options:
    -h, --help         show this help message and exit

    For more information, refer to the relayer-technical-challenge.pdf file
    ```

    <br><br>

-   Now for the timestamp values that I used inside my `block_crawler.py` file on line 115: `timestamp BETWEEN 1704067211 AND 1704069011`, I used those specific values because I was not able to find the unix timestamps of 2024-01-01 00:00:00 and 2024-01-01 00:30:00 in my timezone of PST. The closest unix timestamps that I could use that fell between the block range 18908800 to 18909050 were in the GMT timezone, and off by some seconds

    <img src="images/unix_timestamp_1.png" alt="Image Description" width="655"/>
    <img src="images/unix_timestamp_2.png" alt="Image Description" width="655"/>
