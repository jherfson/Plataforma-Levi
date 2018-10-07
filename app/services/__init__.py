from flask import Flask, jsonify

app = Flask(__name__)

app.config.from_object('services.config.DevelopmentConfig')

@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'Levi'
    })

