from flask import Flask, request
import requests
import random
import string

app = Flask(__name__)
cryptobot_domain = 'pay.crypt.bot'
cryptopay_token = '289394:AAWzXKWnxmoYm2rkpNNsdINkk4UfK93NfHo'

headers = {'Crypto-Pay-API-Token': cryptopay_token}

def generate_random_code(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route('/createInvoiceWeb', methods=['POST'])
def create_invoice_web():
    amount = request.form.get('amount')
    user_id = request.form.get('userID')
    game_type = request.form.get('gameType')
    game_outcome = request.form.get('gameOutcome')
    name = request.form.get('name')

    data = {
        'currency_type': 'fiat',
        'fiat': 'USD',
        'amount': amount,
        'description': 'Ставка в RiasBet',
        'allow_comments': False,
        'payload': f"user_id={user_id};type={game_type};game={game_outcome};name={name}",
        'allow_anonymous': False
    }

    r = requests.post(f"https://{cryptobot_domain}/api/createInvoice", data=data, headers=headers).json()

    return r['result']['bot_invoice_url']

@app.route('/createInvoice', methods=['POST'])
def create_invoice():
    amount = request.form.get('amount')

    data = {
        'currency_type': 'fiat',
        'fiat': 'USD',
        'accepted_assets': ['USDT'],
        'amount': amount,
        'allow_comments': False,
        'allow_anonymous': False
    }

    r = requests.post(f"https://{cryptobot_domain}/api/createInvoice", data=data, headers=headers).json()

    return r

@app.route('/createCheck', methods=['POST'])
def create_check():
    amount = request.form.get('amount')

    data = {
        'asset': 'USDT',
        'amount': amount
    }

    r = requests.post(f"https://{cryptobot_domain}/api/createCheck", data=data, headers=headers).json()

    return r

@app.route('/transfer', methods=['POST'])
def transfer():
    amount = request.form.get('amount')
    user_id = request.form.get('userID')

    data = {
        'user_id': user_id,
        'asset': 'USDT',
        'amount': amount,
        'spend_id': generate_random_code(7)
    }

    r = requests.post(f"https://{cryptobot_domain}/api/transfer", data=data, headers=headers).json()

    return r

@app.route('/getInvoices', methods=['GET'])
def get_invoices():
    r = requests.get(f"https://{cryptobot_domain}/api/getInvoices", data={'status': 'paid'}, headers=headers).json()

    return r

if __name__ == "__main__":
    app.run(port=1337)