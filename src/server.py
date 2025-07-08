from flask import Flask, request, jsonify
from email_verifier.email_verifier_factory import EmailVerifierFactory
from email_finder import EmailFinder
from threading import Thread
import requests
import os

app = Flask(__name__)

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', None)

@app.route('/find', methods=['POST'])
def find():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'domain is required'}), 400
    verifier = data.get('verifier')
    if not verifier:
        return jsonify({'error': 'verifier is required'}), 400
    
    callback = data.get('callback')
    # If not callback provided, blocking call, return results directly
    if not callback:
        emails = EmailFinder(verifier).find_email(name, domain)
        return jsonify(emails), 200
    # If callback provided, run in a separate thread, return results later to callback
    else:
        def process_find(name, domain, callback):
            emails = EmailFinder(verifier).find_email(name, domain)
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
    verifier = data.get('verifier')
    if not verifier:
        return jsonify({'error': 'verifier is required'}), 400

    print(f"Checking email: {email}")

    verifier = EmailVerifierFactory.create(verifier)
    is_valid = verifier.verify_email(email)
    verifier.close()
    print(f"Email {email} is {'valid' if is_valid else 'invalid'}")
    return jsonify({'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=False, host=HOST, port=PORT)