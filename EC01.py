import csv
from collections import defaultdict
#Hello this is a change I am making here
# Read the CSV file and process data
def process_friend_count(file_name):
    data = defaultdict(lambda: {"users": 0, "total_friends": 0})

    try:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                if len(row) < 2:
                    continue  # Skip malformed rows
                name, friends = row
                friends = int(friends)
                first_letter = name[0].upper()  # Get the first letter of the name
                data[first_letter]["users"] += 1
                data[first_letter]["total_friends"] += friends

        return data
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Print the summary
def print_summary(data):
    if data:
        for letter in sorted(data.keys()):
            users = data[letter]["users"]
            total_friends = data[letter]["total_friends"]
            print(f"{letter} - {users} users, {total_friends} total friends")

# Main execution
if __name__ == "__main__":
    file_name = "friend-count.csv"
    summary_data = process_friend_count(file_name)
    print_summary(summary_data)
