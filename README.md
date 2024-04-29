# Ethereum Blockchain Block Crawler 💎

This Block Crawler is intended to retrieve Ethereum Mainnet transactions within a given block range, write them to a SQLite database, and then query for the block that had the largest volume of Ether transferred between 2024-01-01 00:00:11 and 2024-01-01 00:30:11

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

3. **Run the `main.py` file**: Now all you have to do is run the command below and you're all set! But make sure to replace the JSON-RPC endpoint url, SQLite database name, and block range with your own values and block range

    ```bash
    python3 main.py \
    https://rpc.quicknode.pro/key \
    ethereum.sqlite3 \
    500-555
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

    Block Crawler that retrieves Ethereum Mainnet transactions within a given block range, writes them to a database, and queries for the block that had the largest volume of ether transferred between 2024-01-01 00:00:11 and 2024-01-01 00:30:11

    positional arguments:
    json_rpc_endpoint  A JSON-RPC endpoint to call an Ethereum client, (ex. https://rpc.quicknode.pro/key)
    sqlite_file        Path to the SQLite file to write to, (ex. db.sqlite3)
    block_range        A block range formatted as 'start-end', (ex. 200-300)

    options:
    -h, --help         show this help message and exit

    For more information, refer to https://www.quicknode.com/ and https://ethereum.org/en/developers/docs/programming-languages/python/
    ```
