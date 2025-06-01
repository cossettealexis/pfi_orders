# PFI Orders

A Django-based order management system for agents, staff, and admins.

---

## Setup Guide

### Prerequisites

- Python latest lts
- pip
- virtualenv (recommended)
- PostgreSQL 
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

- Create a PostgreSQL database and user.
- Update your `.env`.

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

---

### 10. (Optional) Build Frontend Assets (Tailwind CSS)

If you are using Tailwind CSS (recommended for this project):

1. Make sure you have `Node.js` and `npm` installed.
2. Install frontend dependencies:

    ```sh
    cd static
    npm install
    ```

3. Build Tailwind CSS for development:

    ```sh
    npx tailwindcss -i ./src/input.css -o ./css/output.css --watch
    ```

    Or for production (minified):

    ```sh
    npx tailwindcss -i ./src/input.css -o ./css/output.css --minify
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
