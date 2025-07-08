import smtplib
from smtplib import *
import DNS
from .abstract_email_verifier import AbstractEmailVerifier

class Smtp(AbstractEmailVerifier):

    DELAY_BETWEEN_THREADS = 0.01  # seconds
    MX_CACHE = {}

    def get_mx(hostname: str) -> list[str]:
        if hostname not in Smtp.MX_CACHE:
            print("Performing MX lookup for:", hostname)
            mx_servers = DNS.mxlookup(hostname)
            mx_servers.sort(key=lambda x: x[0])
            mx_servers = [x[1] for x in mx_servers]
            Smtp.MX_CACHE[hostname] = mx_servers
        return Smtp.MX_CACHE[hostname]

    def __init__(self):
       super().__init__(Smtp.DELAY_BETWEEN_THREADS)
       self.smtp_server = None

    def open(self, domain: str) -> smtplib.SMTP:
        if self.smtp_server is None:
            mx_servers = Smtp.get_mx(domain)
            for mx_server in mx_servers:
                try:
                    smtp_server = smtplib.SMTP(mx_server, 25, timeout=10)
                    smtp_server.ehlo_or_helo_if_needed()
                    smtp_server.mail('')
                    self.smtp_server = smtp_server
                    return
                except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
                    continue
            raise ConnectionError("Could not connect to any SMTP server.")

    def verify_email(self, email: str) -> bool:
        # Open SMTP connection if not already open
        domain = email.split('@')[-1]
        self.open(domain)

        # Check if the email is valid by sending a MAIL TO command
        r = self.smtp_server.rcpt(email)

        # If the response code is 250, the email is valid
        if r[0] == 250:
            return True
                
        # GOOGLE RATE ERROR
        if 'https://support.google.com/mail/?p=ReceivingRatePerm' in str(r[1]):
            return True

        # SPAMHAUS FIREWALL
        if 'https://check.spamhaus.org/query/ip/' in str(r[1]):
            raise ConnectionRefusedError(f"Ip blocked by spamhaus.org. See https://check.spamhaus.org")

        # IF BLACKLISTED BY MAIL SERVER
        if 'Your access to this mail system has been rejected' in str(r[1]):
            raise ConnectionRefusedError(f"You have been blacklisted by the mail server")

        return False

    def close(self):
       self.smtp_server.quit()
