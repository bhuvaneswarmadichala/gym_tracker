from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database initialization
def init_db():
    # Create members database
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT UNIQUE NOT NULL,
            membership_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
    # Create workouts database
    conn = sqlite3.connect('workouts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            duration INTEGER NOT NULL,
            calories_burned INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize databases on startup
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')
        membership_type = request.form.get('membership_type')
        
        try:
            conn = sqlite3.connect('members.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO members (name, age, email, membership_type)
                VALUES (?, ?, ?, ?)
            ''', (name, age, email, membership_type))
            conn.commit()
            member_id = cursor.lastrowid
            conn.close()
            flash(f'Registration successful! Welcome, {name}! Your Member ID is {member_id}.', 'success')
            return redirect(url_for('register'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/plans')
def plans():
    workout_plans = [
        {
            'name': 'Beginner Plan',
            'level': 'Beginner',
            'description': 'Perfect for those just starting their fitness journey',
            'exercises': [
                {'name': 'Walking/Jogging', 'reps': '20 minutes', 'calories': '150-200'},
                {'name': 'Push-ups', 'reps': '3 sets of 10', 'calories': '30-40'},
                {'name': 'Squats', 'reps': '3 sets of 15', 'calories': '50-70'},
                {'name': 'Plank', 'reps': '3 sets of 30 seconds', 'calories': '20-30'},
                {'name': 'Stretching', 'reps': '10 minutes', 'calories': '20-30'}
            ]
        },
        {
            'name': 'Intermediate Plan',
            'level': 'Intermediate',
            'description': 'For those with some fitness experience',
            'exercises': [
                {'name': 'Running', 'reps': '30 minutes', 'calories': '300-400'},
                {'name': 'Bench Press', 'reps': '4 sets of 12', 'calories': '80-100'},
                {'name': 'Deadlifts', 'reps': '4 sets of 10', 'calories': '100-120'},
                {'name': 'Pull-ups', 'reps': '3 sets of 8', 'calories': '60-80'},
                {'name': 'Lunges', 'reps': '3 sets of 12 each leg', 'calories': '70-90'},
                {'name': 'Core Work', 'reps': '15 minutes', 'calories': '50-70'}
            ]
        },
        {
            'name': 'Advanced Plan',
            'level': 'Advanced',
            'description': 'High-intensity training for experienced athletes',
            'exercises': [
                {'name': 'HIIT Running', 'reps': '45 minutes', 'calories': '500-600'},
                {'name': 'Heavy Squats', 'reps': '5 sets of 8', 'calories': '120-150'},
                {'name': 'Olympic Lifts', 'reps': '5 sets of 5', 'calories': '150-180'},
                {'name': 'Weighted Pull-ups', 'reps': '4 sets of 10', 'calories': '100-120'},
                {'name': 'Box Jumps', 'reps': '4 sets of 15', 'calories': '80-100'},
                {'name': 'Battle Ropes', 'reps': '4 sets of 1 minute', 'calories': '100-130'},
                {'name': 'Core Circuit', 'reps': '20 minutes', 'calories': '80-100'}
            ]
        }
    ]
    return render_template('plans.html', plans=workout_plans)

@app.route('/log', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        date = request.form.get('date')
        exercise = request.form.get('exercise')
        duration = request.form.get('duration')
        calories_burned = request.form.get('calories_burned')
        
        # Verify member exists
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM members WHERE id = ?', (member_id,))
        member = cursor.fetchone()
        conn.close()
        
        if not member:
            flash('Invalid Member ID. Please register first.', 'danger')
            return redirect(url_for('log_workout'))
        
        try:
            conn = sqlite3.connect('workouts.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO workouts (member_id, date, exercise, duration, calories_burned)
                VALUES (?, ?, ?, ?, ?)
            ''', (member_id, date, exercise, duration, calories_burned))
            conn.commit()
            conn.close()
            flash(f'Workout logged successfully for {member[0]}!', 'success')
            return redirect(url_for('log_workout'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('log_workout'))
    
    return render_template('log.html')

@app.route('/dashboard')
def dashboard():
    # Get all members
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, membership_type FROM members')
    members = cursor.fetchall()
    conn.close()
    
    # Get workout statistics
    conn = sqlite3.connect('workouts.db')
    cursor = conn.cursor()
    
    # Get all workouts with member info
    cursor.execute('''
        SELECT w.id, w.member_id, w.date, w.exercise, w.duration, w.calories_burned
        FROM workouts w
        ORDER BY w.date DESC
        LIMIT 50
    ''')
    workouts = cursor.fetchall()
    
    # Get summary statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_workouts,
            SUM(duration) as total_duration,
            SUM(calories_burned) as total_calories
        FROM workouts
    ''')
    stats = cursor.fetchone()
    
    # Get per-member statistics
    cursor.execute('''
        SELECT 
            member_id,
            COUNT(*) as workout_count,
            SUM(duration) as total_duration,
            SUM(calories_burned) as total_calories
        FROM workouts
        GROUP BY member_id
    ''')
    member_stats = cursor.fetchall()
    
    conn.close()
    
    # Create member lookup dictionary
    member_dict = {m[0]: {'name': m[1], 'email': m[2], 'membership': m[3]} for m in members}
    
    # Combine workout data with member names
    workout_list = []
    for w in workouts:
        member_info = member_dict.get(w[1], {'name': 'Unknown', 'email': '', 'membership': ''})
        workout_list.append({
            'id': w[0],
            'member_id': w[1],
            'member_name': member_info['name'],
            'date': w[2],
            'exercise': w[3],
            'duration': w[4],
            'calories': w[5]
        })
    
    # Combine member stats with member info
    member_stats_list = []
    for ms in member_stats:
        member_info = member_dict.get(ms[0], {'name': 'Unknown', 'email': '', 'membership': ''})
        member_stats_list.append({
            'member_id': ms[0],
            'name': member_info['name'],
            'membership': member_info['membership'],
            'workout_count': ms[1],
            'total_duration': ms[2],
            'total_calories': ms[3]
        })
    
    return render_template('dashboard.html', 
                         workouts=workout_list,
                         stats=stats,
                         member_stats=member_stats_list,
                         total_members=len(members))

@app.route('/api/chart-data')
def chart_data():
    conn = sqlite3.connect('workouts.db')
    cursor = conn.cursor()
    
    # Get daily workout data for the last 7 days
    cursor.execute('''
        SELECT date, SUM(calories_burned) as calories, COUNT(*) as workouts
        FROM workouts
        GROUP BY date
        ORDER BY date DESC
        LIMIT 7
    ''')
    daily_data = cursor.fetchall()
    
    conn.close()
    
    # Reverse to show oldest to newest
    daily_data = list(reversed(daily_data))
    
    return jsonify({
        'dates': [d[0] for d in daily_data],
        'calories': [d[1] for d in daily_data],
        'workouts': [d[2] for d in daily_data]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
