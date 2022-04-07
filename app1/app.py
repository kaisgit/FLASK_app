from flask import Flask
from models import db

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

@app.route('/')
def main():
    return 'Hello world peace'

if __name__ == '__main__':
    app.run()
