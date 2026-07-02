# 📝 Quiz Master Application

Quiz Master is a multi-user web application that serves as an online examination and quiz preparation platform. It enables administrators to create and manage subjects, chapters, quizzes, and questions, while allowing users to register, attempt quizzes, and track their performance.

The project demonstrates the development of a complete web application using Flask, Jinja2 templating, SQLAlchemy ORM, and SQLite.

---

## Features

### Administrator (Quiz Master)

- Secure administrator login
- Manage subjects
- Create and manage chapters
- Create, edit, and delete quizzes
- Add, edit, and remove MCQ questions
- Manage registered users
- Search users, subjects, and quizzes
- View application summary and analytics

### User

- User registration and login
- Browse available subjects and chapters
- Attempt quizzes
- Automatic score calculation
- View quiz history
- Track previous scores and performance

---

## Tech Stack

### Backend

- Python
- Flask
- SQLAlchemy
- SQLite

### Frontend

- Jinja2 Templates
- HTML5
- CSS3
- Bootstrap

---

## Project Highlights

- Full-stack web application
- Role-based authentication (Admin & User)
- CRUD operations for subjects, chapters, quizzes, and questions
- Quiz attempt workflow
- Automatic score calculation
- User performance tracking
- Responsive Bootstrap interface
- Relational database design using SQLAlchemy ORM

---

## Database Design

The application is built around the following core entities:

- Users
- Subjects
- Chapters
- Quizzes
- Questions
- Scores

The database is created programmatically using SQLAlchemy models.

---

## Project Structure

```
Quiz-Master-V1/
│
├── application/
│   ├── models/
│   ├── controllers/
│   ├── templates/
│   ├── static/
│   └── ...
│
├── instance/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/23f3003672/quiz-master-app.git
cd Quiz-Master-V1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at:

```
http://localhost:5000
```

---

## Learning Outcomes

This project demonstrates practical implementation of:

- Flask web development
- MVC-inspired application architecture
- SQLAlchemy ORM
- Relational database design
- User authentication
- CRUD application development
- Server-side rendering with Jinja2
- Bootstrap-based responsive UI
- Full-stack application development using Python
