from DrissionPage import ChromiumPage

class MailMeteor:
    def __init__(self):
        self.driver = None

    def close(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def verify_email(self, email: str, check: int = 0) -> bool:
        if not self.driver:
            self.driver = ChromiumPage()

        self.driver.get(f'https://mailmeteor.com/email-checker?email={email.replace('@', '%40')}')
        text = self.driver.ele('xpath://div[contains(@class, "result-header")]/div/h3[not(contains(text(), "Checking"))]', timeout=30).text
        valid = (text == "Valid")

        if valid and check >= 0:
            print(f"Email {email} is valid. Checking again just to be sure...")
            return self.verify_email(email, check - 1)
        else:
            return valid
