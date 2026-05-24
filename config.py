import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"
PDFS_DIR = OUTPUT_DIR / "pdfs"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA0rcX3XfzviucaGlbelJbxZnJPLMW3otM")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ── 10 Trending Niches (2026) ──
NICHES = [
    {
        "id": "ai-side-hustles",
        "title": "AI Side Hustles",
        "subtitle": "ChatGPT Money Blueprint",
        "emoji": "🤖",
        "color": "#10b981",
        "pdf_cost": 10,
        "tag": "🔥 Hot",
        "description": "Make money with AI tools — no experience needed.",
        "prompt": "Write a detailed guide on making money with ChatGPT and AI tools in 2026. Cover: freelance AI services, AI-generated content shops, AI automation consulting, AI art sales. Include specific platforms, pricing strategies, and step-by-step workflows. 800-1000 words.",
        "filename": "chatgpt_money_blueprint.pdf",
    },
    {
        "id": "crypto-defi",
        "title": "Crypto & DeFi",
        "subtitle": "Passive Income Guide",
        "emoji": "₿",
        "color": "#f59e0b",
        "pdf_cost": 20,
        "tag": "💰 High Value",
        "description": "Crypto passive income strategies for 2026.",
        "prompt": "Write a beginner-friendly guide to passive income in crypto and DeFi for 2026. Cover: staking, yield farming, liquidity pools, crypto lending, airdrop farming, and risk management. Explain each strategy simply. 800-1000 words.",
        "filename": "crypto_passive_income.pdf",
    },
    {
        "id": "health-biohacking",
        "title": "Health & Biohacking",
        "subtitle": "Longevity Protocol",
        "emoji": "🧬",
        "color": "#8b5cf6",
        "pdf_cost": 15,
        "tag": "⭐ Top Rated",
        "description": "Science-backed longevity and optimization.",
        "prompt": "Write a practical biohacking guide for 2026. Cover: morning optimization protocol, sleep hacking, nootropics, intermittent fasting, cold exposure, red light therapy, and supplements. Give specific routines. 800-1000 words.",
        "filename": "longevity_protocol.pdf",
    },
    {
        "id": "ai-ecommerce",
        "title": "AI E-Commerce",
        "subtitle": "Automated Store System",
        "emoji": "🛒",
        "color": "#ef4444",
        "pdf_cost": 20,
        "tag": "🔥 Hot",
        "description": "AI-powered dropshipping and store automation.",
        "prompt": "Write a complete guide to building an AI-powered e-commerce store in 2026. Cover: AI product research, automated customer service with chatbots, AI listing optimization, predictive inventory, and AI marketing. 800-1000 words.",
        "filename": "ai_ecommerce_system.pdf",
    },
    {
        "id": "viral-content",
        "title": "Viral Content Machine",
        "subtitle": "Social Media Growth 2026",
        "emoji": "📱",
        "color": "#3b82f6",
        "pdf_cost": 30,
        "tag": "🔥 Hot",
        "description": "Grow on TikTok, IG, and YouTube with AI.",
        "prompt": "Write a guide to creating viral social media content in 2026 using AI tools. Cover: AI video generation, trending audio strategies, hook formulas, posting schedules, niche selection, and analytics. 800-1000 words.",
        "filename": "viral_content_machine.pdf",
    },
    {
        "id": "digital-real-estate",
        "title": "Digital Real Estate",
        "subtitle": "Website Flipping Playbook",
        "emoji": "🌐",
        "color": "#14b8a6",
        "pdf_cost": 25,
        "tag": "💰 High Value",
        "description": "Buy, build, and flip websites for profit.",
        "prompt": "Write a comprehensive guide to digital real estate and website flipping in 2026. Cover: finding undervalued sites, SEO improvement, content strategies, monetization methods, valuation, and exit strategies. 800-1000 words.",
        "filename": "website_flipping_playbook.pdf",
    },
    {
        "id": "dating-optimization",
        "title": "Online Dating",
        "subtitle": "Dating App Optimization",
        "emoji": "💘",
        "color": "#ec4899",
        "pdf_cost": 8,
        "tag": "⭐ Top Rated",
        "description": "AI-optimized profiles and messaging.",
        "prompt": "Write a practical guide to optimizing dating app profiles in 2026. Cover: photo selection AI tools, bio formulas, messaging strategies, app selection, and common mistakes. Include specific templates and examples. 800-1000 words.",
        "filename": "dating_app_optimization.pdf",
    },
    {
        "id": "productivity-hacks",
        "title": "Productivity Hacks",
        "subtitle": "ADHD Hacker System",
        "emoji": "⚡",
        "color": "#f97316",
        "pdf_cost": 0,
        "tag": "🎯 Free",
        "description": "Hyperfocus and workflow optimization.",
        "prompt": "Write a productivity guide for people who struggle with focus. Cover: the ADHD hacker method, deep work protocols, time blocking, AI task management, dopamine detox, and environment design. 800-1000 words.",
        "filename": "adhd_hacker_system.pdf",
    },
    {
        "id": "home-fitness",
        "title": "Home Fitness",
        "subtitle": "No-Gym Workout Bible",
        "emoji": "💪",
        "color": "#22c55e",
        "pdf_cost": 0,
        "tag": "🎯 Free",
        "description": "Build muscle at home with zero equipment.",
        "prompt": "Write a complete home workout guide requiring zero equipment. Cover: bodyweight progressions, resistance band routines, calisthenics, nutrition basics, recovery, and habit building. Include a 4-week program. 800-1000 words.",
        "filename": "home_workout_bible.pdf",
    },
    {
        "id": "remote-freedom",
        "title": "Remote Work Freedom",
        "subtitle": "Digital Nomad Starter Kit",
        "emoji": "🏝️",
        "color": "#06b6d4",
        "pdf_cost": 35,
        "tag": "⭐ Top Rated",
        "description": "Escape the 9-5 and work from anywhere.",
        "prompt": "Write a guide to becoming a digital nomad in 2026. Cover: remote job types, location selection, visa strategies, income tools, productivity while traveling, cost optimization, and community building. 800-1000 words.",
        "filename": "digital_nomad_starter.pdf",
    },
]

# ── Coin System ──
COIN_PACKS = [
    {"id": "starter", "coins": 10, "price": 9.00, "bonus": 0},
    {"id": "popular", "coins": 25, "price": 19.00, "bonus": 3},
    {"id": "advanced", "coins": 75, "price": 49.00, "bonus": 10},
    {"id": "elite", "coins": 200, "price": 99.00, "bonus": 40},
]

# ── Gamification ──
DAILY_LOGIN_COINS = 5
STREAK_BONUS = {3: 8, 7: 25, 14: 50, 30: 100}
REFERRAL_COINS = 10

BADGES = [
    {"id": "first_download", "name": "First Download", "icon": "🎯", "desc": "Download your first PDF"},
    {"id": "collector", "name": "Collector", "icon": "📚", "desc": "Download 5 PDFs", "target": 5},
    {"id": "scholar", "name": "Scholar", "icon": "🎓", "desc": "Download 10 PDFs", "target": 10},
    {"id": "master", "name": "Master", "icon": "👑", "desc": "Download all PDFs", "target": 10},
    {"id": "streak_3", "name": "Streaker", "icon": "🔥", "desc": "3-day login streak"},
    {"id": "streak_7", "name": "Addict", "icon": "💎", "desc": "7-day login streak"},
    {"id": "streak_30", "name": "Dedicated", "icon": "⭐", "desc": "30-day login streak"},
    {"id": "referrer", "name": "Referrer", "icon": "🤝", "desc": "Refer your first friend"},
]

WHATSAPP_NUMBER = "14073015305"

# ── Stripe ──
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
CREDITS_PER_DOLLAR = 1.2  # e.g. $10 → 12 credits (before pack bonuses)

# ── SMTP / Email ──
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "clearance@nemoclaw.network")
EMAIL_FROM_NAME = "NemoClaw Clearance"

# ── Domain / Deployment ──
PUBLIC_URL = os.getenv("PUBLIC_URL", "http://localhost:8765")
DOMAIN = os.getenv("DOMAIN", "localhost:8765")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8765"))
USE_SSL = os.getenv("USE_SSL", "").lower() in ("1", "true", "yes")

# ── PDF Preview (PyMuPDF) ──
PDF_PREVIEW_ENABLED = True
PREVIEW_CACHE_DIR = PDFS_DIR / "previews"
