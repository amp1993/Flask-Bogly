"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db,User, Post
from flask_migrate import Migrate
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Set to True if you want to intercept redirects
# toolbar = DebugToolbarExtension(app)

migrate = Migrate(app, db)

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
    
    return render_template('users/create_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    
    new_user= User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)
    

    db.session.add(new_user)
    db.session.commit()
    
    print(User.image_url)
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('users/user_details.html', user = user, posts=posts)
    


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    return render_template('users/edit_user.html', user=user, user_id = user_id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def save_edit_user(user_id):
    user = User.query.get_or_404(user_id)

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
    user = User.query.get_or_404(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    return f"User with ID {user_id} not found."

#######   POST ROUTES #######

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['post-title'],
        content = request.form['post-content'],
        user=user)
    
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('posts/post_details.html',post=post)
    
@app.route('/posts/<int:post_id>/edit',)
def show_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html',post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_form(post_id):
    
    post=Post.query.get_or_404(post_id)
    post.title = request.form['edit-title'],
    post. content = request.form['edit-content']
    
    db.session.add(post)
    db.session.commit()
    
    return redirect (f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(f'/users/{post.user_id}')

if __name__ == '__main__':
    app.run()
    
    
    
