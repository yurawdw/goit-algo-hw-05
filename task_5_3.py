'''
    Task 3. Module 5
'''

import re
import sys
from typing import List, Dict
from pathlib import Path
from colorama import init, Fore, Back, Style

# Initializing the colorama
init(autoreset=True)


def parse_log_line(line: str) -> Dict[str, str]:
    """
    Parses the log string, returning a dictionary with date, time, logging level and message.
    """
    match = re.match(
        r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (INFO|ERROR|DEBUG|WARNING) (.*)', line)
    if match:
        return {"date": match.group(1), "time": match.group(2), "level": match.group(3), "message": match.group(4)}
    return {}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Loads logs from a file and returns a list of dictionaries.
    """
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = parse_log_line(line.strip())
            if log_entry:
                logs.append(log_entry)
    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Filters logs by logging level.
    """
    return [log for log in logs if log["level"] == level.upper()]


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Counts the number of logs by logging level.
    """
    counts = {"INFO": 0, "ERROR": 0, "DEBUG": 0, "WARNING": 0}
    for log in logs:
        counts[log["level"]] += 1
    return counts


def display_log_counts(counts: Dict[str, int]):
    """
    Displays log statistics in a table.
    """
    print(
        f"\n{Fore.WHITE}Рівень логування{Style.RESET_ALL} | {Fore.WHITE}Кількість{Style.RESET_ALL}")
    print("----------------------------")
    for level, count in counts.items():
        if level == "INFO":
            print(f"{Fore.GREEN}{level:<16}{Style.RESET_ALL} | {count}")
        elif level == "WARNING":
            print(f"{Fore.YELLOW}{level:<16}{Style.RESET_ALL} | {count}")
        elif level == "ERROR":
            print(f"{Fore.RED}{level:<16}{Style.RESET_ALL} | {count}")
        elif level == "DEBUG":
            print(f"{Fore.BLUE}{level:<16}{Style.RESET_ALL} | {count}")
    print("\n")


def main():
    """
    The main function that processes command line arguments and analyzes logs.
    """
    if len(sys.argv) < 2:
        print(
            f"\nUsage: python3 {Path(sys.argv[0]).name} <log_file> [log_level]\n")
        return

    log_file = sys.argv[1]

    if not Path(log_file).exists():
        print(f"\n{Fore.YELLOW}Log file not found.{Style.RESET_ALL}")
        print(
            f"\nUsage: python3 {Path(sys.argv[0]).name} <log_file> [log_level]\n")
        return

    logs = load_logs(log_file)

    if len(sys.argv) == 3 and sys.argv[2].upper() in {"INFO", "WARNING", "ERROR", "DEBUG"}:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)
        for log in filtered_logs:
            if level.upper() == "INFO":
                print(
                    f"[{Fore.GREEN}{log['level']}{Style.RESET_ALL}] {log['date']} {log['time']} - {log['message']}")
            elif level.upper() == "WARNING":
                print(
                    f"[{Fore.YELLOW}{log['level']}{Style.RESET_ALL}] {log['date']} {log['time']} - {log['message']}")
            elif level.upper() == "ERROR":
                print(
                    f"[{Fore.RED}{log['level']}{Style.RESET_ALL}] {log['date']} {log['time']} - {log['message']}")
            elif level.upper() == "DEBUG":
                print(
                    f"[{Fore.BLUE}{log['level']}{Style.RESET_ALL}] {log['date']} {log['time']} - {log['message']}")
            else:
                print(
                    f"[{log['level']}] {log['date']} {log['time']} - {log['message']}")

    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)


if __name__ == "__main__":
    main()
