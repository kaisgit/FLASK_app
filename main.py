from flask import Flask, make_response, redirect, request, render_template, url_for, flash, session
from flask_script import Manager, Command, Shell
from forms import ContactForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

#########################################################################
#
# This is a working script. Views, config, models, are all in this file.
#
#########################################################################

app = Flask(__name__)
app.debug = True
#app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # to suppress warnings that outputs to the shell

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

### MAIN ############################

@app.route('/')
def index():
    return render_template('index.html', name='Jerry')

@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return "Profile page of user: {}" . format(user_id)

@app.route('/books/<genre>/')
def books(genre):
    res = make_response("All Books in {} category" . format(genre))
    return res

@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(f_User).filter(f_User.username == form.username.data).first()
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

### MODELS ############################

class f_Category(db.Model):
    __tablename__ = 'f_categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('f_Post', backref='f_category', cascade='all, delete-orphan')
 
    def __repr__(self):
        return "<{}:{}>".format(id, self.name)

f_post_tags = db.Table('f_post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('f_posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('f_tags.id'))
)

class f_Post(db.Model):
    __tablename__ = 'f_posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)    
    category_id = db.Column(db.Integer(), db.ForeignKey('f_categories.id'))
 
    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])

class f_Tag(db.Model):
    __tablename__ = 'f_tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('f_Post', secondary=f_post_tags, backref='f_tags')
 
    def __repr__(self):
        return "<{}:{}>".format(id, self.name)

class f_Feedback(db.Model):
    __tablename__ = 'f_feedbacks'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>" . format(self.id, self.name)

### USER AUTHENTICATION ###############
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager(app)
login_manager.login_view = 'login' # url for endpoint 'login'

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(f_User).get(user_id)

class f_User(db.Model, UserMixin):
    __tablename__ = 'f_users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
 
    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    # username/password: spike/spike, tyke/tyke
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

### EXTENDING FLASK ###################
class Faker(Command):
    def run(self):
        print('Fake data entered')
manager.add_command('faker', Faker())

@manager.command
def foo():
    print('foo command executed')

def shell_context():
    import os, sys
    return dict(app=app, os=os, sys=sys)
manager.add_command("shell", Shell(make_context=shell_context))

#######################################

if __name__ == "__main__":
    #app.run(debug=True)
    manager.run()

