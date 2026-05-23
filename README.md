markdown# University Certificate Slot Booking System

A full-stack role-based certificate request and slot allocation platform built with Flask, SQLite, and Jinja2. Simulates a real-world university workflow with admin approval and conflict-safe scheduling.

## Live Demo

- Student Portal: https://slot-booking-flask.onrender.com/student

> Note: Backend is on Render's free tier — first request may take 30–60 seconds due to cold start.

## Tech Stack

**Backend:** Python, Flask

**Frontend:** HTML, CSS, Jinja2

**Database:** SQLite

**Server:** Gunicorn

**Deployment:** Render

## Features

**Student**
- Secure login and session management
- Apply for certificates
- Track request status
- View allocated slot and rejection remarks

**Admin**
- Role-based dashboard with pending request queue
- Approve requests with date-time slot allocation
- Reject requests with mandatory remarks
- Real-time queue updates

**System Logic**
- Slot conflict prevention
- Session-based authentication
- Flash feedback on all actions

## Project Structure

```
slot-booking-flask/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── student/
│   └── admin/
├── static/
└── README.md
```

## Local Setup

```bash
git clone https://github.com/karthiknani229-art/slot-booking-flask.git
cd slot-booking-flask
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

## Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | 123 |
| Student | stu1 | stu1 |

## Author

Penta Karthik — [GitHub](https://github.com/karthiknani229-art)
