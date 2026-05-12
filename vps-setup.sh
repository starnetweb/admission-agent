#!/bin/bash

# Scholarship Agent VPS Setup Script
# Run this on your Hostinger VPS as root

set -e

echo "🚀 Starting Scholarship Agent VPS Setup..."

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
apt install -y docker.io docker-compose
usermod -aG docker $USER
newgrp docker

# Verify Docker
docker --version
docker-compose --version

# Install Nginx
echo "🌐 Installing Nginx..."
apt install -y nginx

# Install Certbot for SSL
echo "🔐 Installing Certbot..."
apt install -y certbot python3-certbot-nginx

# Install Git
echo "📚 Installing Git..."
apt install -y git

# Create project directory
echo "📁 Creating project directory..."
PROJECT_DIR="/home/scholarship-agent"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo ""
echo "✅ Initial setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Clone your repository:"
echo "   git clone <your-repo-url> ."
echo ""
echo "2. Create and configure .env file:"
echo "   cp .env.example .env"
echo "   nano .env"
echo ""
echo "3. Configure Nginx and SSL:"
echo "   sudo nano /etc/nginx/sites-available/scholarship"
echo "   Add proxy configuration to your-domain.com"
echo ""
echo "4. Setup SSL:"
echo "   sudo certbot --nginx -d your-domain.com"
echo ""
echo "5. Start containers:"
echo "   docker-compose up -d"
echo ""
echo "6. Verify it's running:"
echo "   curl http://localhost:3000/health"
echo ""
