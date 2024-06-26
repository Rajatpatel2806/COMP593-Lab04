import sys
import re
import pandas as pd

def main():
    log_file = get_log_file_path_from_cmd_line(1)

    records, _ = filter_log_by_regex(log_file, r'sshd', ignore_case=True, print_summary=True, print_records=True)
    port_traffic = tally_port_traffic(log_file)
    generate_port_traffic_report(log_file, 22)  # Assuming port 22 for example
    generate_invalid_user_report(log_file)
    generate_source_ip_log(log_file, '220.195.35.40')

# Step 3
def get_log_file_path_from_cmd_line(param_number):
    if len(sys.argv) <= param_number:
        print(f"Error: Missing command line parameter #{param_number}")
        sys.exit(1)
    log_file_path = sys.argv[param_number]
    try:
        with open(log_file_path, 'r') as file:
            pass
    except FileNotFoundError:
        print(f"Error: File not found - {log_file_path}")
        sys.exit(1)

    return log_file_path

# Steps 4-7
def filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=False, print_records=False):
    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(regex, flags)
    matching_records = []
    captured_data = []
    """Gets a list of records in a log file that match a specified regex.

    Args:
        log_file (str): Path of the log file
        regex (str): Regex filter
        ignore_case (bool, optional): Enable case insensitive regex matching. Defaults to True.
        print_summary (bool, optional): Enable printing summary of results. Defaults to False.
        print_records (bool, optional): Enable printing all records that match the regex. Defaults to False.

    Returns:
        (list, list): List of records that match regex, List of tuples of captured data
    """

    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                matching_records.append(line.strip())
                captured_data.append(match.groups())

    if print_records:
        for record in matching_records:
            print(record)
    if print_summary:
        print(f"The log file contains {len(matching_records)} records that {'case-insensitive ' if ignore_case else ''}match the regex \"{regex}\".")
     
    return matching_records, captured_data

# Step 8
def tally_port_traffic(log_file):
    port_traffic = {}

    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'DPT=(\d+)', line)
            if match:
                port = match.group(1)
                if port in port_traffic:
                    port_traffic[port] += 1
                else:
                    port_traffic[port] = 1

    return port_traffic

# Step 9
def generate_port_traffic_report(log_file, port_number):
    matching_records, _ = filter_log_by_regex(log_file, f'DPT={port_number}', ignore_case=False)
    df = pd.DataFrame(matching_records, columns=['Log Records'])
    df.to_csv(f'port_{port_number}_traffic_report.csv', index=False)
    print(f'Report generated: port_{port_number}_traffic_report.csv')

# Step 11
def generate_invalid_user_report(log_file):
    matching_records, _ = filter_log_by_regex(log_file, r'invalid user', ignore_case=True)
    df = pd.DataFrame(matching_records, columns=['Log Records'])
    df.to_csv('invalid_user_report.csv', index=False)
    print('Report generated: invalid_user_report.csv')

# Step 12
def generate_source_ip_log(log_file, ip_address):
    matching_records, _ = filter_log_by_regex(log_file, rf'{ip_address}', ignore_case=False)
    df = pd.DataFrame(matching_records, columns=['Log Records'])
    df.to_csv(f'source_ip_{ip_address.replace(".", "_")}_log.csv', index=False)
    print(f'Report generated: source_ip_{ip_address.replace(".", "_")}_log.csv')

if __name__ == '__main__':
    main()