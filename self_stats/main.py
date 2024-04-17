from selector import get_file_presence_flags
import process_watch_history
import process_search_history

def main() -> None:
    """
    Main function that orchestrates the processing of watch history and search history based on file presence.
    """
    directory: str = input("Enter the directory path where your input data is held: ")
    print(f"Processing data from {directory}...")

    file_flags: dict = get_file_presence_flags(directory)
    if file_flags['watch_history_present']:
        process_watch_history.main(directory)
    if file_flags['my_activity_present']:
        process_search_history.main(directory)

if __name__ == "__main__":
    main()
