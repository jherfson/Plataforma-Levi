from flask import Flask

app = Flask(__name__)
#app.config.from_object('config.DevelopmentConfig')
#app.config['DEBUG'] = True

from app.controllers import default