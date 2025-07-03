from app import app

from flask import render_template, request, flash, redirect, url_for, session
from controllers.models import *


@app.route('/')
def home():
    return render_template('home.html')

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

        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('roles', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


