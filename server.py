from flask import Flask, request, jsonify
import combinaison
from mailmeteor import MailMeteor

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
    
    valid = invalid = []
    emails = combinaison.generate_email_combinations(name, domain)
    for email in emails:
        is_valid = mailmeteor.verify_email(email)
        if is_valid:
            valid.append(email)
        else:
            invalid.append(email)

    return jsonify({
        'valid': valid,
        'invalid': invalid
    })

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'email is required'}), 400

    is_valid = mailmeteor.verify_email(email)
    return jsonify({'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=True)