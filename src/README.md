# Qt6 Python App Setup

## Add in .env:

```yml
# Application Configuration
APP_NAME=QtApp
APP_VERSION=0.0.8beta
UI_FILE=main_window.ui

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_db
DB_USER=postgres
DB_PASSWORD=secret
```

## Initial Setup and RUN

Dependencies: **Git**, **Docker**, **Python** ***(3.11+)***, Qt Designer (optional)

```bash
cd deploy
docker-compose --env-file ../.env up -d --build  # Create storages
cd ..
python -m venv venv           # Create virtual environment
venv\Scripts\activate         # Activate on Windows
source venv/bin/activate      # Activate on Linux/Mac

python -m pip install --upgrade pip
pip install -r requirements.txt # Or pip install PyQt6 python-dotenv psycopg2-binary bcrypt

cd src
python -m app.core.utils.convert_ui
python -m app.main
```

# For Developers (FOR EDIT PROJECT)

## Download QT Designer on Folder 'designer':

### https://build-system.fman.io/qt-designer-download

## Run 'designer/designer.exe'

### Save UI files in 'design/ui' folder, update .env

### Or edit file **design/ui/main_window.ui**

## For transform UI to PY and RUN:

```bash
python -m app.core.utils.convert_ui
python -m app.main
```

## Admin account:

```bash
login, password:
admin@example.com
adminpass
```
