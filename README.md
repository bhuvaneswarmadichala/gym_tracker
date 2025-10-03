# FitTrack – Simple Gym Membership & Workout Tracker

![FitTrack Logo](https://img.shields.io/badge/FitTrack-Fitness%20Tracker-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

Project Description:
A lightweight web-based application built with Flask that allows gym members to register, log their daily workouts, and view their progress through a comprehensive dashboard.

##  Features

- **Easy Member Registration**: Quick sign-up with multiple membership tiers
- **Workout Plans**: Pre-defined beginner, intermediate, and advanced workout routines
- **Daily Workout Logging**: Track exercises, duration, and calories burned
- **Interactive Dashboard**: Visualize progress with charts and statistics
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Statistics**: View total workouts, duration, and calories burned
- **Member Analytics**: Per-member workout statistics and progress tracking

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Setup Instructions

1. **Clone the repository** (or download the ZIP file):  
   git clone https://github.com/yourusername/fittrack.git  
   cd fittrack

2. **Create a virtual environment** (recommended):  
   Windows:  
   python -m venv .venv  
   .venv\Scripts\activate  

   macOS/Linux:  
   python3 -m venv .venv  
   source .venv/bin/activate

3. **Install dependencies**:  
   pip install -r requirements.txt

4. **Run the application**:  
   python app.py

5. **Open your browser** and navigate to:  
   http://localhost:5000

##  Usage

### 1. Register as a Member

- Navigate to the **Register** page
- Fill in your details: Name, Age, Email, and Membership Type
- Choose from Basic, Standard, Premium, or VIP membership
- Submit the form and note your Member ID

### 2. View Workout Plans

- Visit the **View Plans** page
- Browse through Beginner, Intermediate, and Advanced plans
- Each plan includes exercises, reps, and calorie estimates

### 3. Log Your Workouts

- Go to the **Log Workout** page
- Enter your Member ID
- Select the workout date and exercise type
- Input duration (in minutes) and calories burned
- Submit to save your workout

### 4. Track Your Progress

- Access the **Dashboard** to view:
  - Total members, workouts, duration, and calories
  - Visual charts showing daily progress
  - Member statistics and recent workout history
  - Per-member analytics

## Database Schema

### Members Table (members.db)

| Column           | Type      | Description                      |
|------------------|-----------|-----------------------------------|
| id              | INTEGER   | Primary key (auto-increment)     |
| name            | TEXT      | Member's full name              |
| age             | INTEGER   | Member's age                    |
| email           | TEXT      | Unique email address            |
| membership_type | TEXT      | Basic / Standard / Premium / VIP |
| created_at      | TIMESTAMP | Registration timestamp          |

---

### Workouts Table (workouts.db)

| Column           | Type      | Description                     |
|------------------|-----------|----------------------------------|
| id              | INTEGER   | Primary key (auto-increment)    |
| member_id       | INTEGER   | Foreign key to members table   |
| date            | TEXT      | Workout date                   |
| exercise        | TEXT      | Type of exercise               |
| duration        | INTEGER   | Duration in minutes            |
| calories_burned | INTEGER   | Calories burned                |
| created_at      | TIMESTAMP | Log timestamp                  |

##  Description
### Home Page
The landing page welcomes users with key features and quick navigation.

### Registration Form
Simple and intuitive form for new member registration with membership tier selection.

### Workout Plans
Three comprehensive workout plans (Beginner, Intermediate, Advanced) with detailed exercises.

### Workout Logging
Easy-to-use form for logging daily workouts with auto-calculated calorie estimates.

### Dashboard
Interactive dashboard with:
- Summary statistics cards
- Bar chart for daily calories burned
- Line chart for workout frequency
- Member statistics table
- Recent workouts history

##  Technologies Used

### Backend
- **Flask 2.3.3** - Python web framework
- **SQLite3** - Lightweight database
- **Werkzeug** - WSGI utility library

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling
- **Bootstrap 5.3.0** - Responsive CSS framework
- **jQuery 3.7.0** - JavaScript library
- **Chart.js 4.3.0** - Data visualization
- **Font Awesome 6.4.0** - Icons


##  Author

BHUVANESWAR MADICHARLA
- GitHub: https://github.com/bhuvaneswarmadichala
- Email: madicharlabanu123@gmail.com

## Acknowledgments

- Bootstrap  for the excellent CSS framework
- Font Awesome for the icon library
- Chart.js for data visualization
- Flask community for documentation and support



