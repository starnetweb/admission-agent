# Scholarship & Admissions News Agent

An automated agent that searches for scholarship and admissions news in Nigeria and sends updates to subscribers via WhatsApp.

## Features

- 🔍 Automated web search for Nigeria scholarship and admissions news
- 📱 WhatsApp messaging via Meta Business API
- 👥 Subscriber management from Facebook lead forms
- ⏰ Scheduled daily news distribution
- 📊 Admin dashboard with statistics
- 🐳 Docker containerized deployment
- 🚀 GitHub Actions CI/CD pipeline
- 📊 Message tracking and logging

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Task Scheduling**: APScheduler
- **Container**: Docker + Docker Compose
- **CI/CD**: GitHub Actions → GHCR
- **Proxy**: Nginx
- **News Source**: NewsAPI.org
- **Messaging**: Meta WhatsApp Business API

## Project Structure

```
scholarship-agent/
├── src/
│   ├── server.py              # FastAPI application
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── agent.py               # Scheduler & news distribution
│   ├── newsapi.py             # News search logic
│   ├── whatsapp.py            # WhatsApp API integration
│   ├── routes/
│   │   ├── webhooks.py        # Facebook webhook endpoint
│   │   ├── subscribers.py     # Subscriber management
│   │   └── admin.py           # Admin endpoints
│   └── __init__.py
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Local development setup
├── nginx.conf                 # Nginx configuration
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions CI/CD
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Prerequisites

### For Local Development

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### For VPS Deployment

- Ubuntu 22.04 LTS
- Docker & Docker Compose
- Nginx
- Let's Encrypt (SSL certificates)
- SSH access

### Required Accounts

1. **WhatsApp Business API**
   - Meta Business Account
   - Verified WhatsApp Business number
   - API token and Phone ID

2. **NewsAPI.org**
   - Free tier account (100 requests/day)
   - API key

3. **GitHub**
   - Repository access
   - SSH keys configured on VPS

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd scholarship-agent
```

### 2. Create `.env` file

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```
DB_PASSWORD=your-secure-password
WHATSAPP_API_TOKEN=your-token
WHATSAPP_PHONE_ID=your-phone-id
NEWSAPI_KEY=your-key
WEBHOOK_TOKEN=your-secret-token
```

### 3. Run with Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- FastAPI app on port 3000
- Nginx on port 80

### 4. Verify it's running

```bash
curl http://localhost:3000/health
```

### 5. Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (or use Docker)
# Then run:
python -m uvicorn src.server:app --reload --host 0.0.0.0 --port 3000
```

## API Endpoints

### Webhooks
- `POST /api/webhooks/facebook` - Receive subscriber data from Facebook
- `GET /api/webhooks/verify?token=xxx` - Verify webhook token

### Subscribers
- `POST /api/subscribers/` - Create subscriber
- `GET /api/subscribers/` - List all subscribers
- `GET /api/subscribers/{id}` - Get specific subscriber
- `PUT /api/subscribers/{id}` - Update subscriber
- `DELETE /api/subscribers/{id}` - Deactivate subscriber

### Admin
- `GET /api/admin/stats` - Get statistics
- `POST /api/admin/run-agent` - Manually run news agent
- `GET /api/admin/news/recent` - Get recent news
- `GET /api/admin/messages/recent` - Get recent messages
- `GET /api/admin/messages/failed` - Get failed messages

## VPS Deployment (Hostinger)

### 1. Initial VPS Setup

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker

# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y

# Create project directory
sudo mkdir -p /home/scholarship-agent
cd /home/scholarship-agent

# Clone your repository
git clone <your-repo-url> .
```

### 2. Configure Environment Variables

```bash
cd /home/scholarship-agent
cp .env.example .env
nano .env
# Fill in your actual credentials
```

### 3. Configure Nginx with SSL

```bash
# Create Nginx config for your domain
sudo nano /etc/nginx/sites-available/scholarship

# Add this content:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable the site
sudo ln -s /etc/nginx/sites-available/scholarship /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### 4. Start Docker Containers

```bash
cd /home/scholarship-agent
docker-compose up -d

# Verify it's running
docker-compose logs -f
```

### 5. Setup GitHub Secrets

In your GitHub repository settings, add these secrets:

```
VPS_HOST          = your-vps-ip
VPS_USER          = root (or your SSH user)
VPS_SSH_KEY       = your-private-ssh-key
VPS_PROJECT_PATH  = /home/scholarship-agent
SLACK_WEBHOOK     = (optional)
```

### 6. GitHub Actions Deployment

Every push to `main` branch will:
1. Build Docker image
2. Push to GitHub Container Registry
3. SSH into VPS
4. Pull latest image and restart containers

## Scheduling

The agent runs daily at **8:00 AM (UTC)** by default.

To change the schedule, edit `src/agent.py`:

```python
def start_scheduler():
    cron_schedule = "0 8 * * *"  # Change this
    # Format: minute hour day month day-of-week
    # Example: "0 9 * * 1-5" = 9 AM on weekdays
```

## Database Migrations

Migrations are created automatically on startup. To manually reset the database:

```bash
docker-compose down -v
docker-compose up -d
```

## Monitoring

### Check Logs

```bash
# Container logs
docker-compose logs -f app

# Nginx logs
docker-compose logs -f nginx

# Database logs
docker-compose logs -f db
```

### Admin Dashboard

Access statistics at:
```
GET http://your-domain/api/admin/stats
```

## Troubleshooting

### WhatsApp Messages Not Sending

1. Check API token is valid
2. Verify phone number format (should be E.164: +234XXX)
3. Check message logs: `GET /api/admin/messages/failed`

### News Not Being Fetched

1. Verify NEWSAPI_KEY is valid
2. Check scheduler is running
3. Manually trigger: `POST /api/admin/run-agent`
4. Check logs for API errors

### Database Connection Issues

```bash
# Test connection
docker-compose exec db psql -U postgres -d scholarship_db -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Container Won't Start

```bash
# Check logs
docker-compose logs app

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

## Security Best Practices

1. ✅ Use strong database passwords
2. ✅ Keep `.env` file secret (never commit)
3. ✅ Use HTTPS only (Let's Encrypt)
4. ✅ Rotate API tokens regularly
5. ✅ Enable firewall on VPS
6. ✅ Use SSH keys (no password auth)
7. ✅ Regular backups of database
8. ✅ Monitor failed messages

## Cost Optimization

- **NewsAPI.org**: Free tier = 100 requests/day (sufficient for 1x daily run)
- **PostgreSQL**: Self-hosted (free)
- **WhatsApp**: Pay per message ($0.01-0.08 per message depending on region)
- **Hostinger VPS**: ~$2.99/month (cheapest tier)

## Contributing

1. Create a feature branch
2. Make changes
3. Test locally with Docker
4. Push to GitHub
5. GitHub Actions will auto-deploy on merge to main

## License

MIT License - feel free to use and modify

## Support

For issues, create a GitHub issue in the repository.

---

Built with ❤️ for Nigerian students
