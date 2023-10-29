"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db,User
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///boggly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Set to True if you want to intercept redirects
# toolbar = DebugToolbarExtension(app)


with app.app_context():
    
    connect_db(app)
    db.create_all()

@app.route('/')
def homepage():
    return redirect('/users')

@app.route('/users')
def show_users():
    users=User.query.all()
    return render_template('/base.html',users=users)


@app.route('/users/new')
def show_user_form():
    
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get(user_id)
    return render_template('user_details.html', user = user)
    


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    
    return render_template('edit_user.html', user=user, user_id = user_id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def save_edit_user(user_id):
    user = User.query.get(user_id)

    updated_first_name = request.form['first_name']
    updated_last_name = request.form['last_name']
    updated_image_url = request.form['image_url']
    
    if user:
        user.first_name = updated_first_name
        user.last_name = updated_last_name
        user.image_url = updated_image_url
        
        db.session.commit()
        
    
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    return f"User with ID {user_id} not found."
    
    
    
