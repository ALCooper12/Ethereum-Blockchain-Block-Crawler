import argparse
import re

from block_crawler import get_ethereum_mainnet_transactions, write_to_and_query_sqlite_database

def main():
    # Set up all the user input argument parameters
    parser = argparse.ArgumentParser(
        prog="main.py",
        description='''
                    Block Crawler that retrieves Ethereum Mainnet transactions within a given block range, writes them to a database, and 
                    queries for the block that had the largest volume of ether transferred between 2024-01-01 00:00:00 and 2024-01-01 00:30:00
                    ''',
        epilog="For more information, refer to the relayer-technical-challenge.pdf file"
    )
    parser.add_argument("json_rpc_endpoint", type=validate_json_rpc_endpoint, help="A JSON-RPC endpoint to call an Ethereum client, (ex. https://rpc.quicknode.pro/key)")
    parser.add_argument("sqlite_file", type=validate_sqlite_file, help="Path to the SQLite file to write to, (ex. db.sqlite3)")
    parser.add_argument("block_range", type=validate_block_range, help="A block range formatted as 'start-end', (ex. 200-300)")

    args = parser.parse_args()

    # Retrieve all Ethereum Mainnet transactions within a given block range
    transactions = get_ethereum_mainnet_transactions(args.json_rpc_endpoint, args.block_range)

    # Persist all the transactions recieved above to a SQLite database
    # Query the populated database for the block that had the largest volume of ether transferred 
    # between 2024-01-01 00:00:00 and 2024-01-01 00:30:00
    write_to_and_query_sqlite_database(transactions, args.sqlite_file)

def validate_json_rpc_endpoint(endpoint):
    # Check if the endpoint starts with http:// or https://
    if not re.match(r'^https?://', endpoint):
        raise argparse.ArgumentTypeError("Invalid JSON-RPC endpoint format. It should start with 'http://' or 'https://'")
    return endpoint

def validate_sqlite_file(file_path):
    # Check if the file path ends with .sqlite or .sqlite3
    if not file_path.endswith(('.sqlite', '.sqlite3')):
        raise argparse.ArgumentTypeError("Invalid SQLite file format. File path should end with '.sqlite3' or '.db'")
    return file_path

def validate_block_range(block_range):
    # Check if the block range is formatted correctly as start-end
    if not re.match(r'^\d+-\d+$', block_range):
        raise argparse.ArgumentTypeError("Invalid block range format. It should be formatted as 'start-end', (ex. '200-300')")
    return block_range


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred while trying to execute the main function:", e)
