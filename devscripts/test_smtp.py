import smtplib
import DNS

def get_mx_record(domain):
    try:
        print("Performing MX lookup for:", domain)
        mx_records = DNS.mxlookup(domain)
        return str(mx_records[0][1])
    except Exception as e:
        raise Exception(f"Error retrieving MX record: {e}") from e

email = input("Enter email to verify: ")
domain = email.split('@')[1]
mx_server = get_mx_record(domain)

print("Using MX server:", mx_server)
smtp_server = smtplib.SMTP(mx_server, 25, timeout=10)
smtp_server.ehlo_or_helo_if_needed()
smtp_server.mail('')
r = smtp_server.rcpt(email)
print(r)
smtp_server.quit()
