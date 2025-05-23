# Projet-9 - Application Web Django LITRevu

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Touitoui/Projet-9.git
cd Projet-9
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # On Linux: source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Generate a new Django secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. Update the `SECRET_KEY` in your `.env` file with the generated key

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user
```

### 6. Run the development server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key (required for production) | Auto-generated for development |
| DEBUG | Enable debug mode | True |
