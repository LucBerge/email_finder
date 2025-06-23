import smtplib

my_email = "lucas@bergeron.fr"
my_password = "M7%L7^8^f%8%4X"
email_to_check = "dd@dsd.fr"

mx_server = "mx1.mail.ovh.net"
smtp_server = "ssl0.ovh.net"

def check_email():
    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls()
        server.login(my_email, my_password)
        server.helo()
        code, message = server.mail(email_to_check)
        print(code, message)
        code, message = server.rcpt(email_to_check)
        print(code, message)

check_email()