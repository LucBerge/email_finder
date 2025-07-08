import os
from email_finder import EmailFinder

EMAIL_VERIFIER = "smtp"

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

    # For each file
    for file in files:
        # Get the name and domain of the file
        name = file["name"]
        domain = file["domain"]
        filepath = file["filepath"]

        # Read the file
        with open(filepath, 'r+') as f:
            content = f.read()

            # If the file is empty
            if not content:
                # Find valid email
                emails = []

                try:
                    emails = EmailFinder(EMAIL_VERIFIER).find_email(name, domain)
                except Exception as e:
                    print(f"Error while finding emails for {name} (@{domain}):\n{e}")
                    f.write(f"Error while finding emails for {name} (@{domain}):\n{e}\n")
                    continue

                print(f"----------------\nReport for {name} (@{domain}):")
                f.write('---------- VALID EMAILS ----------\n')

                # Get valid emails
                valid_emails = [email for email, is_valid in emails.items() if is_valid]
                if len(valid_emails) == 0:
                    print(f"No valid emails found for {name} (@{domain}). Is it a gost?")
                    f.write(f"None\n")
                else:
                    print(f"Valid emails: {len(valid_emails)}")
                    for email in valid_emails:
                        print(f"- {email}")
                        f.write(f"{email}\n")

                print(f"Full report saved in: {filepath}\n----------------")
                f.write('\n---------- INVALID EMAILS ----------\n')

                # Get invalid emails
                invalid_emails = [email for email, is_valid in emails.items() if not is_valid]
                for email in invalid_emails:
                    f.write(f"{email}\n")

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
        print("\nProcess interrupted by user.")
        pass
