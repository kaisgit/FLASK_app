from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import BucketList

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port='8080')
