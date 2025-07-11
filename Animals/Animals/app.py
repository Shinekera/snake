import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import Config
from models import db, User, Animal
from forms import RegistrationForm, LoginForm, AnimalForm

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return redirect(url_for('animals'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('animals'))
        flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AnimalForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data and allowed_file(form.photo.data.filename):
            filename = secure_filename(form.photo.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(filepath)
        animal = Animal(
            name=form.name.data,
            species=form.species.data,
            age=form.age.data,
            city=form.city.data,
            description=form.description.data,
            photo=filename,
            contact=form.contact.data,
            owner=current_user
        )
        db.session.add(animal)
        db.session.commit()
        flash('Animal added successfully.')
        return redirect(url_for('animals'))
    return render_template('add_animal.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/animals')
def animals():
    species = request.args.get('species')
    city = request.args.get('city')
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)

    query = Animal.query
    if species:
        query = query.filter_by(species=species)
    if city:
        query = query.filter(Animal.city.ilike(f'%{city}%'))
    if min_age is not None:
        query = query.filter(Animal.age >= min_age)
    if max_age is not None:
        query = query.filter(Animal.age <= max_age)

    animals = query.all()
    return render_template('animals.html', animals=animals)

@app.route('/animal/<int:animal_id>')
def animal_detail(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return render_template('animal_detail.html', animal=animal)

@app.route('/animal/<int:animal_id>/delete', methods=['POST'])
@login_required
def delete_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    if animal.owner != current_user:
        abort(403)
    # Изтриваме снимката (ако има)
    if animal.photo:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], animal.photo))
        except OSError:
            pass
    db.session.delete(animal)
    db.session.commit()
    flash('Animal listing deleted.')
    return redirect(url_for('animals'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
