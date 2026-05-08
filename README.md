# 📅 Event Management System

A full-featured, role-based event management web application built with **Python & Django**. The platform allows admins, organizers, and participants to manage events seamlessly — from creation to RSVP confirmation.

🌐 **Live Demo:** [event-management-project-orlo.onrender.com](https://event-management-project-orlo.onrender.com/)
&nbsp;&nbsp;|&nbsp;&nbsp;
💻 **GitHub:** [github.com/jjannat04/event-management](https://github.com/jjannat04/event-management)

---

## 📸 Preview

> _Add a screenshot of your homepage or dashboard here._
> `![App Screenshot](./screenshots/home.png)`

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Django |
| Frontend | HTML5, Tailwind CSS |
| Database | SQLite |
| Auth | Django Built-in Auth |
| Deployment | Render |

---

## ✨ Features

- 🔐 **Role-Based Access Control** — Three distinct roles: **Admin**, **Organizer**, and **Participant**, each with scoped permissions and a dedicated dashboard
- 📋 **Event CRUD** — Organizers can create, update, and delete events with full details (title, date, venue, capacity)
- 🗂️ **Category Management** — Events can be organized and filtered by category
- ✅ **RSVP System** — Participants can register for events; the system tracks and manages attendance
- 📧 **Email Confirmation** — Automated email sent to participants upon successful RSVP
- 👤 **Participant Dashboard** — Personalized view showing registered events and status

---

## 📦 Dependencies

```txt
Django>=4.2
Pillow
whitenoise
gunicorn
```

> Full list available in [`requirements.txt`](./requirements.txt)

---

## 🚀 Run Locally

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/jjannat04/event-management.git
cd event-management
```

### 2. Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Now open your browser and go to 👉 `http://127.0.0.1:8000`

> Admin panel available at `http://127.0.0.1:8000/admin`

---

## 🔗 Relevant Links

| Resource | Link |
|----------|------|
| 🌐 Live Demo | [event-management-project-orlo.onrender.com](https://event-management-project-orlo.onrender.com/) |
| 💻 GitHub Repo | [github.com/jjannat04/event-management](https://github.com/jjannat04/event-management) |
| 👤 Developer | [linkedin.com/in/jannatul-ferdous-b504831b3](https://www.linkedin.com/in/jannatul-ferdous-b504831b3/) |

---

## 👩‍💻 Author

**Jannatul Ferdous**
CSE Undergraduate @ CUET 

---

> ⭐ If you found this project useful, consider giving it a star!
