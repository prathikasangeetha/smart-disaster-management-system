# Smart Disaster Management and Alert System

A complete, production-ready, full-stack web application designed for real-time disaster reporting, automated risk analysis, emergency broadcast alerts dispatching, shelter availability tracking, and administrative oversight.

---

## 🌟 Key Features

1. **User Authentication & Management**:
   - Secure user registration and login using Flask-Login and Werkzeug password hashing.
   - Profile management with personal incident report history.

2. **Disaster Incident Reporting & Risk Analysis**:
   - Multi-category disaster reporting (Flood, Cyclone, Earthquake, Fire, Landslide, Tsunami, Drought, Other).
   - GPS coordinate auto-detection & evidence image upload.
   - **Automated Risk Analysis Engine**: Calculates threat levels (`CRITICAL`, `HIGH`, `MODERATE`, `LOW`) and generates tailored safety recommendations.

3. **Analytics Dashboard**:
   - Live KPI summary counters (Total Reports, Active Hazards, Resolved Incidents, Shelters, Users).
   - Interactive visualizations with **Chart.js** (Disasters by Type Doughnut Chart, Status Distribution Pie Chart, Severity Breakdown Bar Chart).

4. **Emergency Broadcast Alerts System**:
   - High-priority emergency alerts feed with affected zone advisories and mandatory evacuation directives.
   - Emergency hotline contacts directory (Disaster Helpline, Fire, Ambulance, Police).

5. **Shelter Management & Live Mapping**:
   - Live capacity tracking (Total capacity vs Available spaces) with dynamic progress bars.
   - One-click direct Google Maps navigation links for each relief center.

6. **Safety Guidelines & Interactive Survival Checklist**:
   - Comprehensive preparedness guidelines for Before, During, and After disaster phases.
   - First Aid protocols and interactive, local-storage saved emergency go-bag checklist.

7. **Comprehensive Admin Panel**:
   - Secure Admin Portal with `admin_required` authorization protection.
   - Manage Incident Reports (Approve / Set Active / Mark Resolved / Delete).
   - Manage Relief Shelters (Add / Edit capacity & available beds / Delete).
   - Manage Emergency Alerts (Broadcast new / Activate or Deactivate / Delete).
   - Manage User Roles (Promote citizen to Admin / Demote / Delete).

8. **Advanced Search & Multi-Criteria Filtering**:
   - Keyword search across locations and descriptions.
   - Filter by Disaster Type, Severity Level, Status, and Date.

---

## 💻 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Font Awesome 6, Chart.js
- **Backend**: Python 3.x, Flask Web Framework
- **Database**: MySQL / SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-Login, Werkzeug Security
- **File Processing**: Werkzeug Secure Uploads, Pillow (PIL)

---

## 📁 Project Folder Structure

```
Smart_Disaster_Management/
│── app.py                    # Flask application entry point & database initialization
│── config.py                 # Application configuration settings
│── requirements.txt          # Python library dependencies
│── README.md                 # Project documentation & setup instructions
│── database.sql              # MySQL database schema & sample seed data script
│
├── models/                   # SQLAlchemy ORM Data Models
│   ├── __init__.py
│   ├── user.py               # User & Admin authentication model
│   ├── report.py             # Disaster report & Risk Analysis model
│   ├── shelter.py            # Shelter capacity tracking model
│   ├── alert.py              # Emergency broadcast alert model
│   └── guideline.py          # Safety & First Aid guidelines model
│
├── routes/                   # Flask Blueprints & HTTP Request Handlers
│   ├── __init__.py
│   ├── main_routes.py        # Public landing, analytics dashboard, search API
│   ├── auth_routes.py        # Registration, login, logout, profile
│   ├── report_routes.py      # Incident reporting & detail view
│   ├── shelter_routes.py     # Relief shelter finder
│   ├── alert_routes.py       # Emergency alerts feed
│   ├── guideline_routes.py   # Safety guidelines & checklist
│   └── admin_routes.py       # Admin panel management routes
│
├── controllers/              # Business Logic & Controller Layer
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── report_controller.py
│   ├── shelter_controller.py
│   ├── alert_controller.py
│   └── admin_controller.py
│
├── utils/                    # Utilities & Helper Functions
│   ├── __init__.py
│   ├── helpers.py            # Risk Analysis calculation & Image upload helper
│   └── seed_data.py          # Automatic database seed populator
│
├── static/                   # Static Assets
│   ├── css/
│   │   └── style.css         # Modern design tokens, glassmorphism, responsive styles
│   ├── js/
│   │   ├── main.js           # Client-side validation, GPS helper, checklist storage
│   │   └── dashboard.js      # Chart.js visualization initialization
│   ├── images/               # Sample visuals
│   └── uploads/              # Uploaded incident evidence photos
│
└── templates/                # Jinja2 HTML Templates
    ├── base.html             # Master layout with top emergency banner & footer
    ├── index.html            # Public home page
    ├── login.html            # Login screen
    ├── register.html         # User registration screen
    ├── dashboard.html        # Analytics dashboard & search filter page
    ├── report.html           # Incident reporting form
    ├── report_detail.html    # Detailed report & risk analysis view
    ├── shelters.html         # Shelter directory & mapping
    ├── alerts.html           # Emergency broadcasts feed
    ├── guidelines.html       # Safety guidelines & survival kit
    ├── profile.html          # User profile & personal report history
    ├── 404.html              # Custom 404 error page
    ├── 500.html              # Custom 500 error page
    └── admin/
        ├── base_admin.html   # Admin layout with sidebar navigation
        ├── dashboard.html    # Admin analytics overview
        ├── users.html        # Manage users & roles
        ├── reports.html      # Manage & approve disaster reports
        ├── shelters.html     # Manage shelters & capacity
        └── alerts.html       # Broadcast & toggle emergency alerts
```

---

## 🚀 Quick Setup & Installation Guide

### Prerequisites
- Python 3.8 or higher installed on your system.
- (Optional) MySQL Server installed and running locally.

---

### Step 1: Install Dependencies
Open your terminal/command prompt in the `Smart_Disaster_Management` directory and run:

```bash
pip install -r requirements.txt
```

---

### Step 2: Database Setup

#### Option A: Using MySQL (Recommended for Production)
1. Start your local MySQL Server (e.g. XAMPP, WAMP, or MySQL Workbench).
2. Create database and import `database.sql`:
   ```bash
   mysql -u root -p < database.sql
   ```
3. (Optional) Configure environment variables in `config.py` if your MySQL username/password differ from default `root`/`root`.

#### Option B: Automatic SQLite Fallback (Zero Configuration)
If MySQL is not installed, the application will **automatically fallback to local SQLite database** (`disaster_management.db`) upon launch, creating all required tables and populating demo seed data seamlessly!

---

### Step 3: Run the Application
Execute `app.py`:

```bash
python app.py
```

The application will start on: **http://127.0.0.1:5000/**

---

## 🔑 Demo Login Credentials

| Role | Username / Login ID | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Full access to Admin Panel (`/admin`), user roles, report approval, shelter & alert management |
| **Citizen / User** | `johndoe` | `user123` | Report disasters, view risk analysis, profile history, shelter finder |
| **Citizen / User** | `sarah_smith` | `user123` | Report disasters, view risk analysis, profile history, shelter finder |

---

## 📄 License & Credits
Developed as an open-source, full-stack Smart Disaster Management solution. Built with Python Flask, Bootstrap 5, Font Awesome, and Chart.js.
