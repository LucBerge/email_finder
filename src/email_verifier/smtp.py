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

    def verify_email(self, email: str) -> bool:
        domain = email.split('@')[-1]
        mx_servers = Smtp.get_mx(domain)
        
        for mx_server in mx_servers:
            try:
                smtpServer = smtplib.SMTP(mx_server, 25, timeout=10)
                smtpServer.ehlo_or_helo_if_needed()
                smtpServer.mail('')
                r = smtpServer.rcpt(email)
                smtpServer.quit()
                if r[0] == 250:
                    return True
                
                # GOOGLE RATE ERROR
                if 'https://support.google.com/mail/?p=ReceivingRatePerm' in str(r[1]):
                    return True

                # SPAMHAUS PROJECT
                if 'https://check.spamhaus.org/query/ip/' in str(r[1]):
                    raise ConnectionRefusedError(f"Ip blocked by spamhaus.org. See https://check.spamhaus.org")
            
                return False
            except smtplib.SMTPResponseException as e:
                pass

        return False
       
    def close(self):
       pass
