# Hospital Appointment System

A Django-based web application that allows patients to browse doctors, book appointments, and manage their appointment history.

---

## Features

- **User Authentication** — Sign up, log in, and log out securely
- **Doctor Directory** — Browse all available doctors with search by name and filter by department
- **Appointment Booking** — Book an appointment with any doctor by selecting a date and time
- **Appointment History** — View all past and upcoming appointments
- **Cancel Appointments** — Cancel a scheduled appointment with a confirmation step
- **Duplicate Prevention** — Prevents double-booking the same doctor at the same date/time

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default)
- **Frontend:** HTML templates (Django templating engine)

---

## Project Structure

```
Hospital Appointment System/
├── mokshang/
│   ├── manage.py
│   ├── mokshang/          # Project settings & config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── project/           # Main app
│       ├── models.py      # Doctor, Patient, Appointment models
│       ├── views.py       # All view logic
│       ├── forms.py       # Signup & Appointment forms
│       ├── urls.py        # App URL routes
│       ├── admin.py
│       ├── migrations/
│       └── templates/
│           ├── base.html
│           ├── login.html
│           ├── signup.html
│           ├── doctors.html
│           ├── book.html
│           ├── appointments.html
│           └── cancel_confirm.html
└── .gitignore
```

---

## Models

| Model | Fields |
|-------|--------|
| `Doctor` | name, department, specialization |
| `Patient` | user (OneToOne), age, contact |
| `Appointment` | doctor, patient, date_time, status (Scheduled / Cancelled) |

---

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | home | Redirects to doctor list |
| `/signup/` | signup_view | Patient registration |
| `/login/` | login_view | User login |
| `/logout/` | logout_view | User logout |
| `/doctors/` | doctor_list | Browse & search doctors |
| `/book/<doctor_id>/` | book_appointment | Book an appointment |
| `/appointments/` | appointment_history | View your appointments |
| `/appointments/<id>/cancel/` | cancel_appointment | Cancel an appointment |

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/gajeramokshang-droid/Hospital-Appointment-System-.git
cd "Hospital Appointment System/mokshang"

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install django

# Apply migrations
python manage.py migrate

# Create a superuser (to add doctors via admin panel)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Adding Doctors

Log in to the Django admin panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) using your superuser credentials and add doctors from there.

---

## License

This project is open source and available under the [MIT License](LICENSE).
