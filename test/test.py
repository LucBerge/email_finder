import socket
import dns.resolver
import smtplib

def get_mx_record(domain):
    try:
        # Retrieve MX records for the domain
        mx_records = dns.resolver.query(domain, 'MX')
        # Return the mail server with the highest priority (lowest preference number)
        return str(mx_records[0].exchange)
    except Exception as e:
        print(f"Error retrieving MX record: {e}")
        return None

def verify_email(email):
    # Extract the domain from the email address
    domain = email.split('@')[1]

    # Get the mail server from the MX record
    mail_server = get_mx_record(domain)
    print(mail_server)
    mail_server = "mx3.mail.ovh.net"
    if not mail_server:
        print("Could not retrieve mail server.")
        return False

    
    smtplib.SMTP(host='', port=0, local_hostname=None, source_address=None)


    try:
        # Connect to the mail server on port 25
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((mail_server, 25))
            sock.recv(1024)  # Receive the server's greeting

            # Send HELO command
            sock.sendall(b'HELO yourdomain.com\r\n')
            sock.recv(1024)

            # Send MAIL FROM command
            sock.sendall(b'MAIL FROM:<fake@yourdomain.com>\r\n')
            sock.recv(1024)

            # Send RCPT TO command
            sock.sendall(f'RCPT TO:<{email}>\r\n'.encode())
            response = sock.recv(1024).decode()

            # Check the response code
            if '250' in response:
                print(f"Email address {email} exists.")
                return True
            else:
                print(f"Email address {email} does not exist.")
                return False
    except Exception as e:
        print(f"Error connecting to mail server: {e}")
        return False

# Example usage
email_to_verify = 'lucas@bergeron.fr'
verify_email(email_to_verify)
