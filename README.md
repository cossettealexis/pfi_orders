# PFI Orders

A Django-based order management system for agents, staff, and admins.

---

## Setup Guide

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- PostgreSQL (or SQLite for testing)
- Node.js & npm (for frontend assets, optional)
- Git

---

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd pfi_orders
```

---

### 2. Create and Activate a Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Python Dependencies

```sh
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

- Copy `.env.example` to `.env` and update values as needed.
- Set your database credentials and secret key.

---

### 5. Set Up the Database

- Create a PostgreSQL database and user (or use SQLite for testing).
- Update your `DATABASES` setting in `settings.py` or `.env`.

---

### 6. Run Migrations

```sh
python manage.py migrate
```

---

### 7. Create a Superuser

```sh
python manage.py createsuperuser
```

---

### 8. (Optional) Load Initial Data

```sh
python manage.py loaddata initial_data.json
```

---

### 9. Run the Development Server

```sh
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

### 10. (Optional) Build Frontend Assets

If you have custom JS/CSS and use npm:

```sh
cd static
npm install
npm run build
```

---

### 11. Access the Admin Panel

Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials.

---

### 12. Running Tests

```sh
python manage.py test
```

---

### Troubleshooting

- Ensure your virtual environment is activated.
- Check your `.env` and database settings.
- Review error messages in the terminal for missing dependencies.

---

### Useful Commands

- **Run server:** `python manage.py runserver`
- **Make migrations:** `python manage.py makemigrations`
- **Apply migrations:** `python manage.py migrate`
- **Create superuser:** `python manage.py createsuperuser`
- **Collect static files:** `python manage.py collectstatic`

---

For further help, check the project documentation or contact the maintainer.
