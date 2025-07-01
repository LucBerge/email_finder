from flask import Flask, request, jsonify
from email_verifier.email_verifier_factory import EmailVerifierFactory
from email_finder import EmailFinder
from threading import Thread
import requests
import os

app = Flask(__name__)

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', None)
EMAIL_VERIFIER = os.getenv('EMAIL_VERIFIER', 'mailmeteor')

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
        emails = EmailFinder(EMAIL_VERIFIER).find_email(name, domain)
        print(f"Finished finding emails for {name} at {domain}")
        print(f"Sending results to callback URL: {callback}")
        requests.post(callback, json=emails)

    Thread(target=process_find, args=(name, domain, callback)).start()
    return '', 200

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'email is required'}), 400

    print(f"Checking email: {email}")

    verifier = EmailVerifierFactory.create(EMAIL_VERIFIER)
    is_valid = verifier.verify_email(email)
    verifier.close()
    print(f"Email {email} is {'valid' if is_valid else 'invalid'}")
    return jsonify({'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)