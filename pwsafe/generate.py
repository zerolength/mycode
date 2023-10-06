import csv
import random
import string

# Function to generate a random password
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate a random username
def generate_random_username():
    adjectives = ["happy", "sunny", "lucky", "smiling", "funny"]
    animals = ["dog", "cat", "bird", "elephant", "giraffe"]
    return random.choice(adjectives) + random.choice(animals) + str(random.randint(1, 100))

# Function to generate a random URL
def generate_random_url():
    domains = [".com", ".net", ".org", ".gov"]
    return "http://www.example" + random.choice(domains)

# Function to generate a random description
def generate_random_description():
    words = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    return ' '.join(random.choices(words, k=random.randint(3, 10)))

# Function to generate random password entries
def generate_password_entries(num_entries):
    entries = []
    for _ in range(num_entries):
        group = "Group" + str(random.randint(1, 10))
        title = "Title" + str(random.randint(1, 100))
        username = generate_random_username()
        password = generate_random_password()
        url = generate_random_url()
        autotype = "Autotype" + str(random.randint(1, 5))
        created_time = "Created Time" + str(random.randint(1, 100))
        password_modified_time = "Password Modified Time" + str(random.randint(1, 100))
        last_access_time = "Last Access Time" + str(random.randint(1, 100))
        password_expiry_date = "Password Expiry Date" + str(random.randint(1, 100))
        password_expiry_interval = "Password Expiry Interval" + str(random.randint(1, 100))
        record_modified_time = "Record Modified Time" + str(random.randint(1, 100))
        password_policy = "Password Policy" + str(random.randint(1, 100))
        password_policy_name = "Password Policy Name" + str(random.randint(1, 100))
        history = "History" + str(random.randint(1, 10))
        run_command = "Run Command" + str(random.randint(1, 5))
        dca = "DCA" + str(random.randint(1, 5))
        shift_dca = "Shift+DCA" + str(random.randint(1, 5))
        email = "email" + str(random.randint(1, 100))
        protected = "Protected" + str(random.randint(0, 1))
        symbols = "Symbols" + str(random.randint(1, 5))
        keyboard_shortcut = "Keyboard Shortcut" + str(random.randint(1, 5))
        notes = generate_random_description()

        entry = [
            group, title, username, password, url, autotype, created_time, password_modified_time,
            last_access_time, password_expiry_date, password_expiry_interval, record_modified_time,
            password_policy, password_policy_name, history, run_command, dca, shift_dca, email,
            protected, symbols, keyboard_shortcut, notes
        ]

        entries.append(entry)

    return entries

# Function to save password entries to a file
def save_password_entries(entries, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        header = [
            'Group/Title', 'Username', 'Password', 'URL', 'AutoType', 'Created Time',
            'Password Modified Time', 'Last Access Time', 'Password Expiry Date',
            'Password Expiry Interval', 'Record Modified Time', 'Password Policy',
            'Password Policy Name', 'History', 'Run Command', 'DCA', 'Shift+DCA', 'e-mail',
            'Protected', 'Symbols', 'Keyboard Shortcut', 'Notes'
        ]
        writer.writerow(header)
        writer.writerows(entries)

def main():
    num_entries = 10  # Change this to the number of entries you want to generate
    filename = "passwords.txt"
    entries = generate_password_entries(num_entries)
    save_password_entries(entries, filename)
    print(f"{num_entries} password entries saved to {filename}")

if __name__ == "__main__":
    main()

