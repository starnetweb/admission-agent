# Quick Start Guide

Get the scholarship agent running in 5 minutes!

## Option 1: Docker Compose (Easiest)

### Prerequisites
- Docker & Docker Compose installed
- Copy `.env.example` to `.env` and fill in your credentials

### Steps

```bash
# 1. Start all services
docker-compose up -d

# 2. Verify it's running
curl http://localhost:3000/health
# Should return: {"status":"healthy"}

# 3. Create a test subscriber
curl -X POST http://localhost:3000/api/subscribers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+2348012345678"
  }'

# 4. View all subscribers
curl http://localhost:3000/api/subscribers/

# 5. Check admin stats
curl http://localhost:3000/api/admin/stats

# 6. Manually trigger news agent
curl -X POST http://localhost:3000/api/admin/run-agent
```

### View Logs

```bash
# App logs
docker-compose logs -f app

# Database logs
docker-compose logs -f db

# Nginx logs
docker-compose logs -f nginx
```

### Stop Services

```bash
docker-compose down
```

---

## Option 2: Local Python Development

### Prerequisites
- Python 3.11+
- PostgreSQL running (via Docker or locally)

### Steps

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup PostgreSQL (if using Docker)
docker run -d \
  --name scholarship_db \
  -e POSTGRES_DB=scholarship_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15-alpine

# 4. Create .env file
cp .env.example .env
# Edit .env with your credentials

# 5. Run the app
python -m uvicorn src.server:app --reload --host 0.0.0.0 --port 3000
```

### Testing the API

```bash
# Health check
curl http://localhost:3000/health

# Create subscriber
curl -X POST http://localhost:3000/api/subscribers/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","phone":"+2349012345678"}'

# Get admin stats
curl http://localhost:3000/api/admin/stats
```

---

## Testing Facebook Webhook

```bash
curl -X POST http://localhost:3000/api/webhooks/facebook \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "+2348012345678"
  }'
```

## Testing Manual News Agent

```bash
curl -X POST http://localhost:3000/api/admin/run-agent
```

Check the logs to see news fetching and WhatsApp message sending!

## Environment Variables Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then edit `.env` and provide:

- `DB_PASSWORD` - PostgreSQL password
- `WHATSAPP_API_TOKEN` - From Meta Business
- `WHATSAPP_PHONE_ID` - Your WhatsApp business phone ID
- `NEWSAPI_KEY` - From NewsAPI.org
- `WEBHOOK_TOKEN` - Any secure string for webhook verification

## Database Operations

### Access PostgreSQL directly

```bash
# Via Docker
docker-compose exec db psql -U postgres -d scholarship_db

# Common commands
\dt                    # List tables
SELECT * FROM subscribers;
SELECT * FROM news_records;
SELECT * FROM message_logs;
\q                     # Exit
```

### Reset Database

```bash
# Stop and remove volumes
docker-compose down -v

# Restart (creates fresh database)
docker-compose up -d
```

## Common Issues

### Port Already in Use

```bash
# Change ports in docker-compose.yml or:
docker-compose down
# Then remove the conflicting container
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs db
```

### WhatsApp Messages Not Sending

1. Verify `WHATSAPP_API_TOKEN` is valid
2. Check phone number format (E.164: +234XXXXXXXXXX)
3. View failed messages: `curl http://localhost:3000/api/admin/messages/failed`

### News Not Fetching

1. Verify `NEWSAPI_KEY` is valid
2. Check your API rate limit (free tier: 100 requests/day)
3. Check logs: `docker-compose logs -f app`

## Next Steps

1. ✅ Test locally with Docker Compose
2. ✅ Verify API endpoints work
3. ✅ Test with real WhatsApp credentials
4. ✅ Set up GitHub repository
5. ✅ Configure GitHub secrets
6. ✅ Deploy to Hostinger VPS
7. ✅ Configure custom domain with SSL

See [README.md](README.md) for complete deployment guide.

---

**Need help?** Check the logs and error messages in `docker-compose logs app`
