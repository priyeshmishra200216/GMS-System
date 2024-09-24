from flask import Flask, render_template, redirect, url_for, request, flash
from config import db  # Import db from config.py
from models import Admin, Athlete, Match
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

@app.route('/')
def index():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    athletes = Athlete.query.all()
    return render_template('dashboard.html', athletes=athletes)

# Generate Tournament Draws Route
@app.route('/generate_draws', methods=['POST'])
@login_required
def generate_draws():
    athletes = Athlete.query.all()

    if len(athletes) % 2 != 0:
        flash("Odd number of athletes. One athlete will get a bye.", 'info')

    # Shuffle athletes and pair them into matches
    athlete_list = list(athletes)
    import random
    random.shuffle(athlete_list)

    for i in range(0, len(athlete_list) - 1, 2):
        match = Match(athlete1_id=athlete_list[i].id, athlete2_id=athlete_list[i + 1].id)
        db.session.add(match)
    
    if len(athlete_list) % 2 != 0:
        match = Match(athlete1_id=athlete_list[-1].id, athlete2_id=None)  # Give bye to the last athlete
        db.session.add(match)

    db.session.commit()
    flash("Tournament draws generated successfully!", 'success')
    return redirect(url_for('draws'))

# View Tournament Draws Route
@app.route('/draws')
@login_required
def draws():
    matches = Match.query.all()
    return render_template('draw.html', matches=matches)

# Update Match Scores Route
@app.route('/update_score', methods=['GET', 'POST'])
@login_required
def update_score():
    if request.method == 'POST':
        match_id = request.form.get('match_id')
        score = request.form.get('score')
        winner_id = request.form.get('winner_id')

        match = Match.query.get(match_id)
        if match:
            match.score = score
            match.winner = Athlete.query.get(winner_id).name
            db.session.commit()
            flash('Score and winner updated successfully!', 'success')

        return redirect(url_for('draws'))

    return render_template('update_score.html')

if __name__ == '__main__':
    app.run(debug=True)
