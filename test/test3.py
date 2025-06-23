import dns.resolver
import smtplib
import socket

addressToVerify = 'rickymartin@yahoo.com'
domainToVerify = 'yahoo.com'

records = dns.resolver.query(domainToVerify, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)
print(mxRecord)

server = smtplib.SMTP(host='', port=0, local_hostname=None, source_address=None, timeout=10)

server.set_debuglevel(0)
server.connect(mxRecord)
server.helo(server.local_hostname)
server.mail('me@domain.com')
code, message = server.rcpt(str(addressToVerify))
server.quit()

if code == 250:
    print('Valid')
else:
    print('Invalid')