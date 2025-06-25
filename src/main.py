import os
import combinaison
from mailmeteor import MailMeteor

def list_files():
    files = []
    # For each folder in "data"
    for folder in os.listdir("data"):
        # For each file in the folder
        for filename in os.listdir(os.path.join("data", folder)):
            # If the file is a .txt file
            if filename.endswith(".txt"):
                # Absolute path of the file
                filepath = os.path.join("data", folder, filename)
                files.append({
                    "domain": folder,
                    "name": filename.replace('.txt', ''),
                    "filepath": filepath
                })

    return files


def main():
    # Get all files
    files = list_files()
    mailmeteor = MailMeteor()

    try:
        # For each file
        for file in files:
            # Get the name and domain of the file
            name = file["name"]
            domain = file["domain"]
            filepath = file["filepath"]

            # Get all combinations of the name and domain
            emails = combinaison.generate_email_combinations(name, domain)
            action_performed = False

            # Read the file
            with open(filepath, 'r+') as f:
                content = f.read()

                # If the file is empty
                if not content:
                    # Check if a random email is valid
                    random_email_is_valid = mailmeteor.verify_email(f"this_is_a_random_email@{domain}")
                    if random_email_is_valid:
                        print(f"Random email failed for {domain}. Existing...")
                        f.write(f"*@{domain} is not compatible with MailMeteor. Find an other way...\n")
                        continue
                
                # Skip if the file already contains *@domain
                if f"*@{domain}" in content:
                    continue

                # For each email to check
                for email in emails:

                    #If the email is not in the file
                    if email not in content:

                        action_performed = True
                        # Print the remaining number of emails to check
                        print(f"Checking email: {email} ({emails.index(email) + 1}/{len(emails)})")

                        # Write the email in the file
                        is_valid = mailmeteor.verify_email(email)
                        f.write(f"{is_valid}\t{email}\n")

                        if is_valid:
                            print(f"{email} is valid!")

            # Read the file again
            with open(filepath, 'r') as f:
                if action_performed:
                    # Read content again
                    content = f.read()
                    # Print report
                    print(f"----------------\nReport for {name} (@{domain}):")
                    valid_emails = [line for line in content.split('\n') if line and line.split('\t')[0] == 'True']
                    if len(valid_emails) > 0:
                        print(f"Valid emails: {len(valid_emails)}")
                        for email in valid_emails:
                            print(f"- {email.split('\t')[1]}")
                    else:
                        print("No valid emails found. Is it a gost?")

                    print(f"Full report saved in: {filepath}\n----------------")

    finally:
        mailmeteor.close()

    # Ask for person full name
    name = input("Enter your target fullname with spaces between names (case insensitive) (eg. Arthur MENSCH): ")
    # Ask for person domain
    domain = input("Enter your target domain (eg. mistral.ai): ")
    # Create the file path
    filepath = os.path.join("data", domain, f"{name}.txt")
    # Create the file if it doesn't exist
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write("")

    # Call main again
    main()

    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:   
        pass
