# NemoClaw Production Deployment

## Prerequisites
- Ubuntu 22.04+ server
- Python 3.9+
- Domain (nemoclaw.network) with DNS pointing to server
- Stripe account (for payments)
- SMTP credentials (for email)

## Quick Start

```bash
# 1. Clone/copy project to /var/www/nemoclaw
sudo mkdir -p /var/www/nemoclaw
sudo cp -r . /var/www/nemoclaw
sudo chown -R www-data:www-data /var/www/nemoclaw

# 2. Install dependencies
cd /var/www/nemoclaw
pip3 install -r requirements.txt

# 3. Set environment variables in /etc/systemd/system/nemoclaw.service
# Edit the service file with your Stripe keys, SMTP creds, and Gemini key:
sudo nano /var/www/nemoclaw/deploy/nemoclaw.service

# 4. Build static files
python3 main.py

# 5. Install systemd service
sudo cp deploy/nemoclaw.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nemoclaw
sudo systemctl start nemoclaw
sudo systemctl status nemoclaw

# 6. Set up nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/nemoclaw
sudo ln -s /etc/nginx/sites-available/nemoclaw /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 7. SSL with Certbot
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d nemoclaw.network -d www.nemoclaw.network
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `PUBLIC_URL` | Yes | `http://localhost:8765` | Public-facing URL |
| `DOMAIN` | Yes | `localhost:8765` | Domain for links |
| `STRIPE_SECRET_KEY` | For payments | `""` | Stripe secret key (sk_live_) |
| `STRIPE_PUBLISHABLE_KEY` | For payments | `""` | Stripe publishable key (pk_live_) |
| `STRIPE_WEBHOOK_SECRET` | For webhooks | `""` | Stripe webhook signing secret (whsec_) |
| `SMTP_HOST` | For email | `""` | SMTP server hostname |
| `SMTP_PORT` | No | `587` | SMTP port |
| `SMTP_USER` | For email | `""` | SMTP username |
| `SMTP_PASS` | For email | `""` | SMTP password |
| `EMAIL_FROM` | No | `clearance@nemoclaw.network` | From address |
| `GEMINI_API_KEY` | Yes | `AIzaSyA...` | Google Gemini API key |
| `SERVER_HOST` | No | `0.0.0.0` | Bind address |
| `SERVER_PORT` | No | `8765` | Bind port |

## Stripe Setup

1. Create Stripe account at https://stripe.com
2. Get API keys from Dashboard > Developers > API keys
3. Set up webhook endpoint: `https://nemoclaw.network/stripe-webhook`
4. Listen for: `checkout.session.completed`
5. Copy signing secret into `STRIPE_WEBHOOK_SECRET`

## Email Setup

Option A — SMTP (recommended):
- Use SendGrid, Mailgun, or any SMTP provider
- Set SMTP_HOST, SMTP_USER, SMTP_PASS

Option B — Local sendmail:
- Install sendmail/postfix on the server
- Leave SMTP_HOST empty — uses local MTA

## Monitoring

- Server logs: `sudo journalctl -u nemoclaw -f`
- Admin panel: https://nemoclaw.network/admin
- Server restart: `sudo systemctl restart nemoclaw`
