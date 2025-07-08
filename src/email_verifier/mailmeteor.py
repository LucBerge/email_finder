from DrissionPage import ChromiumPage, ChromiumOptions
from .abstract_email_verifier import AbstractEmailVerifier

class Mailmeteor(AbstractEmailVerifier):

    DELAY_BETWEEN_THREADS = 8  # seconds

    def __init__(self):
        super().__init__(Mailmeteor.DELAY_BETWEEN_THREADS)
        self.driver = None

    def close(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def verify_email(self, email: str) -> bool:
        return self.__verify_email(email, 2)

    def __verify_email(self, email: str, check: int = 0) -> bool:
        if not self.driver:
            options = ChromiumOptions().auto_port()
            options.headless(False)
            self.driver = ChromiumPage(options)

        self.driver.get(f'https://mailmeteor.com/email-checker?email={email.replace('@', '%40')}')
        text = self.driver.ele('xpath://div[contains(@class, "result-header")]/div/h3[not(contains(text(), "Checking"))]', timeout=30).text
        valid = (text == "Valid")

        if valid and check > 0:
            print(f"Email {email} appears valid. Checking again just to be sure...")
            return self.__verify_email(email, check - 1)
        else:
            return valid
