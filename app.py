from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask server is running!'

@app.route('/check_connectivity')
def check_connectivity():
    try:
        response = requests.get('https://api.telegram.org')
        if response.status_code == 200:
            return 'Connectivity to Telegram API is OK!'
        else:
            return 'Failed to connect to Telegram API', 500
    except Exception as e:
        return f"Error checking connectivity: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
