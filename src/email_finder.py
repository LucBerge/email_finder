import combinaison
import threading
import time
from email_verifier.email_verifier_factory import EmailVerifierFactory

class EmailFinder:
    def __init__(self, verifier_type: str):
        self.verifier_type = verifier_type

    def find_email(self, name: str, domain: str) -> dict[str, bool]:

        # Check if verifier is compatible with the domain
        verifier = EmailVerifierFactory.create(self.verifier_type)
        try:
            if verifier.verify_email(f"this_is_a_random_email@{domain}"):
                raise ValueError(f"Domain {domain} is not compatible with {self.verifier_type}: The answer is always True.")
        finally:
            verifier.close()

        # Generate all combinations of the name and domain
        emails: dict[str, bool | None] = {}
        for email in combinaison.generate_email_combinations(name, domain):
            emails[email] = None
        print(f"Generated {len(emails)} email combinations for {name} at {domain}.")

        # While at least one email is None, we will keep checking
        while any(is_valid is None for is_valid in emails.values()):
            threads: list[EmailVerifierThread] = []
            for idx, (email, is_valid) in enumerate(emails.items()):
                if is_valid is None:
                    print(f"Checking email: {email} ({idx + 1}/{len(emails)})")
                    thread = EmailVerifierThread(email, self.verifier_type)
                    thread.start()
                    threads.append(thread)
                    time.sleep(verifier.delay_between_threads)

            for thread in threads:
                thread.join()
                if thread.is_valid is not None:
                    emails[thread.email] = thread.is_valid
        
        return emails

        
class EmailVerifierThread(threading.Thread):

    def __init__(self, email, verifier_type):
        super().__init__()
        self.email = email
        self.verifier_type = verifier_type
        self.is_valid = None

    def run(self):
        verifier = EmailVerifierFactory.create(self.verifier_type)
        try:
            self.is_valid = verifier.verify_email(self.email)
            if self.is_valid:
                print(f"{self.email} is valid!")
        finally:
            verifier.close()
        