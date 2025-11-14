#!/bin/bash
# Simple deployment script for Ubuntu/Linux VPS

echo "🚀 Starting Django LibraryProject deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx git -y

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Set environment variables (you'll need to customize these)
echo "🔧 Setting environment variables..."
export DEBUG=False
export ALLOWED_HOSTS='your-domain.com,www.your-domain.com'

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate

# Create superuser (you'll need to do this manually)
echo "👤 Create superuser (run manually):"
echo "python3 manage.py createsuperuser"

# Install Gunicorn
echo "🔧 Installing Gunicorn..."
pip3 install gunicorn

# Test Gunicorn
echo "🧪 Testing Gunicorn..."
gunicorn LibraryProject.wsgi:application --bind 0.0.0.0:8000 --daemon

echo "✅ Basic deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Configure Nginx (see HTTPS_DEPLOYMENT_GUIDE.md)"
echo "2. Get SSL certificate: sudo certbot --nginx -d your-domain.com"
echo "3. Set up Gunicorn service (see guide)"
echo "4. Configure firewall: sudo ufw allow 'Nginx Full'"
echo ""
echo "🌐 Visit your domain to test!"