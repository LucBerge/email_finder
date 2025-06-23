from flask import Flask, request, jsonify
import combinaison
from mailmeteor import MailMeteor
from threading import Thread
import requests

app = Flask(__name__)
mailmeteor = MailMeteor()

@app.route('/find', methods=['POST'])
def find():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'domain is required'}), 400
    callback = data.get('callback')
    if not callback:
        return jsonify({'error': 'callback is required'}), 400

    def process_find(name, domain, callback):
        print(f"Finding emails for {name} at {domain}...")

        valid = []
        invalid = []
        emails = combinaison.generate_email_combinations(name, domain)
        for idx, email in enumerate(emails):
            print(f"Checking email: {email} ({idx + 1}/{len(emails)})")
            is_valid = mailmeteor.verify_email(email)
            if is_valid:
                valid.append(email)
            else:
                invalid.append(email)
        
        result = {
            'valid': valid,
            'invalid': invalid
        }

        print(f"Finished finding emails for {name} at {domain}. Valid: {len(valid)}, Invalid: {len(invalid)}")
        print(f"Sending results to callback URL: {callback}")
        requests.post(callback, json=result)

    Thread(target=process_find, args=(name, domain, callback)).start()
    return '', 200

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'email is required'}), 400

    print(f"Checking email: {email}")

    is_valid = mailmeteor.verify_email(email)
    print(f"Email {email} is {'valid' if is_valid else 'invalid'}")
    return jsonify({'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=False, port=5000)