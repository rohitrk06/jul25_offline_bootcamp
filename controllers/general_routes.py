from app import app

from flask import render_template, request, flash, redirect, url_for, session
from controllers.models import *


@app.route('/')
def home():
    categories = Category.query.all()

    return render_template('home.html', categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #data validation

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login'))
        
        if user.password != password:
            flash('Incorrect password.', 'error')
            return redirect(url_for('login'))
        
        session['email'] = user.email
        session['roles'] = [role.name for role in user.roles]

        print(type(session['roles'])) 

        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('roles', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        #data validation
        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        
        user_role = Role.query.filter_by(name='user').first()
        user = User(
            email=email,
            password=password,
            roles=[user_role]
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
        
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'GET':
        return render_template('add_category.html')
    
    if request.method == 'POST':
        name = request.form.get('name')

        #data validation
        if not name:
            flash('Category name is required.', 'error')
            return redirect(url_for('add_category'))
        
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash('Category already exists.', 'error')
            return redirect(url_for('add_category'))
        
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('home'))
    
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('add_product.html', categories = categories)
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category_id = request.form.get('category_id')

        #data validation
        if not name or not price or not category_id:
            flash('All fields are required.', 'error')
            return redirect(url_for('add_product'))
        
        try:
            price = float(price)
        except ValueError:
            flash('Price must be a number.', 'error')
            return redirect(url_for('add_product'))
        
        category = Category.query.get(category_id)
        if not category:
            flash('Invalid category selected.', 'error')
            return redirect(url_for('add_product'))
        
        product = Product(name=name, price=price, category=category)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('home'))
    

@app.route('/category/<int:category_id>/delete', methods=['GET'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        flash('Category not found.', 'error')
        return redirect(url_for('home'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        flash('Category not found.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('edit_category.html', category=category)
    
    if request.method == 'POST':
        name = request.form.get('name')

        #data validation
        if not name:
            flash('Category name is required.', 'error')
            return redirect(url_for('edit_category', category_id=category.id))
        
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category and existing_category.id != category.id:
            flash('Category already exists.', 'error')
            return redirect(url_for('edit_category', category_id=category.id))
        
        category.name = name
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('home'))