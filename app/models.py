from app import db, login_manager
from datetime import datetime
from flask_login import (LoginManager, UserMixin, login_required, login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash


class f_Category(db.Model):
    __tablename__ = 'f_categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('f_Post', backref='f_category', cascade='all, delete-orphan')
 
    def __repr__(self):
        return "<{}:{}>".format(id, self.name)

# This association table must appear before Post and Tag models.
#
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

#class f_Employee(db.Model):
    #__tablename__ = 'f_employees'
    #id = db.Column(db.Integer(), primary_key=True)
    #name = db.Column(db.String(255), nullable=False)
    #designation = db.Column(db.String(255), nullable=False)
    #doj = db.Column(db.Date(), nullable=False)    


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
