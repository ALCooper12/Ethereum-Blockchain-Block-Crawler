import json
import tabulate
from web3 import Web3
import sqlite3


def get_ethereum_mainnet_transactions(json_rpc_url, block_range):
    transactions = []
    split_block_range = block_range.split("-")
    start = int(split_block_range[0])
    end = int(split_block_range[1])

    try: 
        # Connect the JSON-RPC url with the Web3 remote provider
        w3 = Web3(Web3.HTTPProvider(json_rpc_url))
        
        # Start looping over block numbers within a specified start and end range
        for block_num in range(start, end + 1):
            try: 
                # Get block information for the specified block number and also extract the timestamp info
                current_block = w3.eth.get_block(block_num, full_transactions=True)
                timestamp = current_block["timestamp"]
            except KeyError as e:
                print(f"An error occurred while fetching block {block_num}: {e}")
                continue
            
            # Iterate over each transaction dictionary in the current block, and extract the needed information into the "transactions" list
            # We also add a new property called "timestamp" into the dictionary 
            for transaction in current_block["transactions"]:
                transaction_dict = dict(transaction)
                transaction_dict["timestamp"] = timestamp
                transactions.append(transaction_dict)

    except (ValueError, ConnectionError) as e:
        print(f"An error occurred while connecting to the JSON-RPC URL: {e}")
    
    return transactions


def write_to_and_query_sqlite_database(transactions, database):
    try:
        connection = connect_to_database(database)
        if connection:
            create_table_and_insert_transactions(connection, transactions)
            query_largest_volume(connection)
            connection.close()
    except Exception as e:
        print("An unexpected error occurred:", e)


def connect_to_database(database):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(database)
        return connection
    except sqlite3.Error as e:
        print("An error occurred with SQLite:", e)
        return None


def create_table_and_insert_transactions(connection, transactions):
    cursor = connection.cursor()
    try:
        # Create the "block" table if it doesn't exist already
        cursor.execute('''CREATE TABLE IF NOT EXISTS block (
                        hash BLOB,
                        number INTEGER,
                        timestamp INTEGER,
                        block_transaction TEXT
                    )''')

        for transaction in transactions:
            # Extract block information properties
            hash = transaction["blockHash"].hex()
            number = transaction["blockNumber"]
            timestamp = transaction["timestamp"]

            # Extract transaction information properties
            wanted_transaction_properties = {
                "hash": transaction["hash"].hex(),
                "blockHash": transaction["blockHash"].hex(),
                "blockNumber": transaction["blockNumber"],
                "from": transaction["from"],
                "to": transaction["to"],
                "value": transaction["value"]
            }
            # Serialize the wanted transaction properties to JSON
            transaction_data = json.dumps(wanted_transaction_properties)

            # Insert block and transaction data into the block table
            cursor.execute('''INSERT INTO block (hash, number, timestamp, block_transaction)
                        VALUES (?, ?, ?, ?)''', (hash, number, timestamp, transaction_data))
            
        # Commit and write everything done above to the database
        connection.commit()
    except sqlite3.Error as e:
        print("An error occurred with SQLite:", e)
    finally:
        cursor.close()


def query_largest_volume(connection):
    cursor = connection.cursor()
    try:
        # Query the database to calculate the total volume of ether transferred
        # between the specified time range, converting values from wei to ether.
        cursor.execute('''
                        WITH block_transactions AS (
                            SELECT
                                number AS block_number,
                                CAST(JSON_EXTRACT(block_transaction, '$.value') AS REAL) AS value_in_wei
                            FROM
                                block
                            WHERE
                                timestamp BETWEEN 1704067211 AND 1704069011
                        )
                        SELECT
                            block_number,
                            SUM(value_in_wei / 1e18) AS total_volume_in_ether
                        FROM
                            block_transactions
                        GROUP BY
                            block_number
                        ORDER BY
                            total_volume_in_ether DESC
                        LIMIT 1;
                        ''')

        row = [cursor.fetchone()]

        # For the case where a result is not found
        if row is None or not row[0]:
            print("No data found in the database for the specified block range or time range")
        else:
            # Set up the result to be displayed in a PostgreSQL like table in the terminal
            headers = ["block_number", "total_volume_of_ether"]
            print("\n")
            print("Block that had the largest volume of Ether transferred between the specified time range \n")
            print(tabulate.tabulate(row, headers=headers, tablefmt="psql"))
            print("\n")

            # Write the result to a .txt file
            with open('largest_volume_of_ether.txt', 'w') as file:
                file.write("Block that had the largest volume of Ether transferred\n\n")
                file.write(tabulate.tabulate(row, headers=headers, tablefmt="psql"))
                print("Result saved to largest_volume_of_ether.txt \n")

    except sqlite3.Error as e:
        print("An error occurred with SQLite:", e)
    finally:
        cursor.close()
