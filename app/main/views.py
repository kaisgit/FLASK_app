from app import app, db
from . import main
from flask import Flask, request, render_template, redirect, url_for, flash, make_response, session
from flask_login import login_required, login_user, current_user, logout_user
from app.models import f_User, f_Post, f_Category, f_Feedback, db
from .forms import ContactForm, LoginForm
from app.utils import send_mail

#print(res.__dict__)
#print(request.form)    #prints request form-submitted data
#print(request.headers) #prints request header data
#print(request.__dict__) #prints all request data 
#print(form.data)       #prints form data

### MAIN ############################

@app.route('/')
def index():
    #name, age, profession = "Jerry", 24, "Programmer"
    #template_context = dict(name=name, age=age , profession=profession)
    #return render_template('index.html', **template_context)
    #return render_template('index.html', **{'name':name, 'age':age, 'profession':profession})

    return render_template('index.html', name='Jerry')

@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user: {}" . format(user_id)

@app.route('/books/<genre>/')
def books(genre):
    res = make_response("All Books in {} category" . format(genre))
    return res

#@app.route('/login/', methods=['post', 'get'])
#def login():
    #message = ''
    #if request.method == 'POST':
        #username = request.form.get('username')  # access the data inside 
        #password = request.form.get('password')
 
        #if username == 'root' and password == 'pass':
            #message = "Correct username and password"
        #else:
            #message = "Wrong username or password"
 
    #return render_template('login.html', message=message)

@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    form = LoginForm()
    if form.validate_on_submit():
        print('USER: ', form.username.data)
        user = db.session.query(f_User).filter(f_User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))
 
        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()    
    flash("You have been logged out.")
    return redirect(url_for('login'))

### FORMS ############################

@app.route('/contact/', methods=['get','post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        feedback = f_Feedback(name=name, email=email, message=message)
        db.session.add(feedback)
        db.session.commit()

        flash('Message Received', 'Success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

### COOKIE ############################

@app.route('/set-cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60*60*24*1)
    else:
        res = make_response("Value of cookie foo is {}" . format(request.cookies.get('foo')))
    return res

@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res

@app.route('/article/', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60*60*24*1)
        res.headers['location'] = url_for('article')
        return res, 302
    
    return render_template('article.html')

### SESSION ############################

@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1 # setting session data
    return "Total visits: {}".format(session.get('visits'))

@app.route('/session/')
def updating_session():
    res = str(session.items())
 
    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        #session.pop('cart_item', None)     #delete session
        session['cart_item']['pineapples'] = '100'
        session.modified = True     # tells flask to send the updated session cookie to the client
    else:
        session['cart_item'] = cart_item
 
    return res
 
@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None) # delete session: visits
    return 'Visits deleted'

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')
