#!/bin/bash

set -e

echo "🚀 Starting LitLoop Deployment..."

# 1. Environment Check
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with the required secrets."
    exit 1
fi

# 2. Update Code
echo "📥 Pulling latest changes..."
git pull origin main

# 3. Virtual Environment Setup
_VENV="env"
if [ ! -d "$_VENV" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv "$_VENV"
fi
source "$_VENV/bin/activate"

# 4. Install/Update Dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/base.txt

# 5. Database Migrations
echo "📂 Running database migrations..."
python manage.py migrate --noinput

# 6. Static Files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 7. Update systemd service files from deploy/
echo "🚦 Updating systemd service files..."
sed -i "s|/home/driptamine/litloop_backend_v2|$(pwd)|g" deploy/gunicorn/daphne.service
sed -i "s|User=driptamine|User=$USER|g" deploy/gunicorn/daphne.service
sudo cp deploy/gunicorn/daphne.service /etc/systemd/system/daphne.service

sed -i "s|/home/driptamine/litloop_backend_v2|$(pwd)|g" deploy/gunicorn/gunicorn_http.service
sed -i "s|User=driptamine|User=$USER|g" deploy/gunicorn/gunicorn_http.service
sudo cp deploy/gunicorn/gunicorn_http.service /etc/systemd/system/gunicorn_http.service

sudo systemctl daemon-reload

# 8. Restart Services
echo "🚦 Restarting services..."
for service in daphne gunicorn_http; do
    if systemctl is-active --quiet "$service"; then
        sudo systemctl restart "$service"
        echo "   ✅ $service restarted"
    else
        echo "   ⚠️ $service not active. Enabling and starting..."
        sudo systemctl enable "$service"
        sudo systemctl start "$service"
    fi
done

# 9. Update and restart Nginx
echo "🌐 Updating Nginx config..."
sed -i "s|/home/driptamine/litloop_backend_v2|$(pwd)|g" deploy/nginx/django.conf
sudo cp deploy/nginx/django.conf /etc/nginx/sites-available/litloop.conf
sudo nginx -t && sudo systemctl restart nginx

echo "✅ Deployment Successful!"
