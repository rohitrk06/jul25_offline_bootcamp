from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    # __tablename__ = 'userInMyApplicaiton'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    roles = db.relationship('Role', secondary='user_role')

    # def __repr__(self):
    #     return f'<User {self.email}>'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # def __repr__(self):
    #     return f'<Role {self.name}>'

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    category = db.relationship('Category')

    def __repr__(self):
        return f'<Product {self.name}>'

def create_tables():
    with app.app_context():
        db.create_all()
        user_role = Role.query.filter_by(name='user').first()
        admin_role = Role.query.filter_by(name='admin').first()

        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)

        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)

        db.session.commit()


        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin_role = Role.query.filter_by(name='admin').first()
            admin = User(
                email = 'admin@gmail.com',
                password = 'admin123',
                roles=[admin_role]
            )
            db.session.add(admin)

            # get_admin = User.query.filter_by(email="admin@gmail.com").first()
            # admin_role = Role.query.filter_by(name='admin').first()
            
            # user_role = UserRole(user_id=get_admin.id, role_id=admin_role.id)
            # db.session.add(user_role)

        db.session.commit()


        # User.query.all()
        # User.query.filter_by().all()
        # User.query.filter_by().first()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True) 