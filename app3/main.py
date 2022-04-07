from flask import Flask, render_template
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Flask App."

@app.route('/user/')
def user():
    users = ['frank','steve','alice','bruce']
    posts = [
        {'author': 'Spike', 'body': '(Hardcoded) Test post #1'},
        {'author': 'Susan', 'body': '(Hardcoded) Test post #2'}
    ]
    return render_template('user.html', **locals())

@app.route('/chart/')
def chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('chart.html', values=temperatures, labels=times, legend=legend)

@app.route('/hello/<string:name>/')
def hello(name):
    quotes = [
        "This is random quote 1.",
        "This is random quote 2.",
        "This is random quote 3.",
        "This is random quote 4."
    ]
    randomNumber = randint(0,len(quotes)-1)
    quote = quotes[randomNumber]
    return render_template('hello.html', **locals())


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
