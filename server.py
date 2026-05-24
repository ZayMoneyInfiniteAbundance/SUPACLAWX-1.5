#!/usr/bin/env python3
import json
import os
import sys
import time
import uuid
import queue
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"
sys.path.insert(0, str(PROJECT_DIR))
os.chdir(str(OUTPUT_DIR))

from pdf_generator import generate_professional_pdf_bytes
from pdf_preview import extract_first_page_as_png
from config import (
    NICHES, COIN_PACKS, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY,
    STRIPE_WEBHOOK_SECRET, PUBLIC_URL, DOMAIN,
    SMTP_HOST, GEMINI_API_KEY, PDF_PREVIEW_ENABLED,
)
from email_sender import send_clearance_packet

REQUEST_LOG = []
SERVER_START = time.time()
CAPTURED_EMAILS = []

SSE_CLIENTS = []
SSE_LOCK = threading.Lock()
ACTIVITY_QUEUE = queue.Queue()

STRIPE_AVAILABLE = bool(STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY)
if STRIPE_AVAILABLE:
    import stripe
    stripe.api_key = STRIPE_SECRET_KEY

PACK_MAP = {p["id"]: p for p in COIN_PACKS}
PACK_PRICE_MAP = {p["id"]: int(p["price"] * 100) for p in COIN_PACKS}  # cents for Stripe


def broadcast_event(event_type, data):
    msg = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
    with SSE_LOCK:
        dead = []
        for q in SSE_CLIENTS:
            try:
                q.put_nowait(msg)
            except Exception:
                dead.append(q)
        for q in dead:
            SSE_CLIENTS.remove(q)


def _log_activity(msg, detail=""):
    entry = {
        "time": time.time(),
        "msg": msg,
        "detail": detail,
    }
    broadcast_event("activity", entry)
    while len(REQUEST_LOG) > 500:
        REQUEST_LOG.pop(0)


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/admin":
            return self.serve_admin_page()
        elif path == "/admin-api/stats":
            return self.serve_admin_stats()
        elif path == "/events":
            return self.serve_sse()
        elif path.startswith("/preview-pdf/"):
            niche_id = path.split("/preview-pdf/", 1)[1]
            return self.serve_preview_pdf(niche_id)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if path == "/generate-pdf":
            return self.handle_generate_pdf(body)
        elif path == "/create-checkout-session":
            return self.handle_create_checkout(body)
        elif path == "/verify-session":
            return self.handle_verify_session(body)
        elif path == "/capture-email":
            return self.handle_capture_email(body)
        elif path == "/admin-api/generate-pdf":
            return self.handle_admin_generate_pdf(body)
        elif path == "/stripe-webhook":
            return self.handle_stripe_webhook(body)
        else:
            self.send_json(404, {"error": "Not found"})

    # ── SSE ──

    def serve_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Send initial replay of recent activity
        recent = [
            {"time": r["time"], "msg": r.get("msg", ""), "detail": r.get("detail", "")}
            for r in REQUEST_LOG[-20:]
        ]
        self.wfile.write(f"event: init\ndata: {json.dumps(recent)}\n\n".encode())
        self.wfile.flush()

        q = queue.Queue()
        with SSE_LOCK:
            SSE_CLIENTS.append(q)
        try:
            while True:
                try:
                    msg = q.get(timeout=30)
                    self.wfile.write(msg.encode())
                    self.wfile.flush()
                except queue.Empty:
                    self.wfile.write(b": heartbeat\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            with SSE_LOCK:
                if q in SSE_CLIENTS:
                    SSE_CLIENTS.remove(q)

    # ── PDF Preview ──

    def serve_preview_pdf(self, niche_id):
        niche = next((n for n in NICHES if n["id"] == niche_id), None)
        if not niche:
            return self.send_json(404, {"error": "Niche not found"})
        # Check cache first
        from config import PREVIEW_CACHE_DIR
        cache_path = PREVIEW_CACHE_DIR / f"{niche_id}.png"
        if cache_path.exists():
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "max-age=86400")
            self.send_header("Content-Length", str(cache_path.stat().st_size))
            self.end_headers()
            self.wfile.write(cache_path.read_bytes())
            return
        # Generate PDF on the fly for preview
        try:
            pdf_bytes = generate_professional_pdf_bytes(niche)
            img_bytes = extract_first_page_as_png(pdf_bytes, niche_id)
            if img_bytes:
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Cache-Control", "max-age=86400")
                self.send_header("Content-Length", str(len(img_bytes)))
                self.end_headers()
                self.wfile.write(img_bytes)
            else:
                self.send_json(404, {"error": "Preview unavailable"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    # ── Generate PDF ──

    def handle_generate_pdf(self, body):
        niche_id = body.get("niche_id")
        niche = next((n for n in NICHES if n["id"] == niche_id), None)
        email = body.get("email", "")
        client_ip = self.client_address[0]

        REQUEST_LOG.append({
            "time": time.time(),
            "niche_id": niche_id,
            "ip": client_ip,
            "ua": self.headers.get("User-Agent", ""),
            "msg": "",
            "detail": "",
        })

        if not niche:
            REQUEST_LOG[-1]["status"] = "error"
            return self.send_json(404, {"error": "Niche not found"})

        try:
            pdf_bytes = generate_professional_pdf_bytes(niche)
            REQUEST_LOG[-1]["status"] = "ok"
            REQUEST_LOG[-1]["size"] = len(pdf_bytes)

            # Broadcast deployment event
            sys_name = niche.get("title", niche_id)
            _log_activity(
                f"Operator deployed {sys_name}",
                f"system deployed — {len(pdf_bytes)} bytes"
            )

            # Generate preview in background
            if PDF_PREVIEW_ENABLED:
                try:
                    extract_first_page_as_png(pdf_bytes, niche_id)
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'attachment; filename="{niche["filename"]}"')
            self.send_header("Content-Length", str(len(pdf_bytes)))
            self.end_headers()
            self.wfile.write(pdf_bytes)
        except Exception as e:
            REQUEST_LOG[-1]["status"] = "error"
            REQUEST_LOG[-1]["error"] = str(e)
            self.send_json(500, {"error": str(e)})

    # ── Stripe Checkout ──

    def handle_create_checkout(self, body):
        pack_id = body.get("pack_id")
        pack = PACK_MAP.get(pack_id)
        if not pack:
            return self.send_json(400, {"error": "Invalid pack"})

        if not STRIPE_AVAILABLE:
            return self.send_json(200, {
                "simulated": True,
                "pack_id": pack_id,
                "credits": pack["coins"] + pack["bonus"],
            })

        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"{pack['coins']} Intel Credits" + (f" (+{pack['bonus']} free)" if pack["bonus"] else ""),
                            "description": f"NemoClaw Operational Intelligence Network — Credit Pack",
                        },
                        "unit_amount": PACK_PRICE_MAP[pack_id],
                    },
                    "quantity": 1,
                }],
                success_url=f"{PUBLIC_URL}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{PUBLIC_URL}/?checkout=cancel",
                metadata={"pack_id": pack_id, "credits": str(pack["coins"] + pack["bonus"])},
            )
            return self.send_json(200, {"url": session.url, "session_id": session.id})
        except Exception as e:
            return self.send_json(500, {"error": str(e)})

    def handle_verify_session(self, body):
        session_id = body.get("session_id")
        pack_id = body.get("pack_id")
        if session_id and STRIPE_AVAILABLE:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                if session.payment_status == "paid":
                    credits = int(session.metadata.get("credits", 0))
                    return self.send_json(200, {"verified": True, "credits": credits})
                return self.send_json(200, {"verified": False})
            except Exception as e:
                return self.send_json(500, {"error": str(e)})
        elif pack_id:
            pack = PACK_MAP.get(pack_id)
            if pack:
                return self.send_json(200, {
                    "simulated": True,
                    "credits": pack["coins"] + pack["bonus"],
                })
        return self.send_json(400, {"error": "Invalid request"})

    def handle_stripe_webhook(self, body):
        if not STRIPE_AVAILABLE:
            return self.send_json(200, {"status": "ignored"})
        payload = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        sig_header = self.headers.get("Stripe-Signature", "")
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        except Exception:
            return self.send_json(400, {"error": "Invalid signature"})

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            credits = int(session["metadata"].get("credits", 0))
            _log_activity(
                f"Credits purchased — {credits} intel credits added to vault",
                f"checkout session {session['id']}"
            )

        return self.send_json(200, {"status": "ok"})

    # ── Email Capture ──

    def handle_capture_email(self, body):
        email = body.get("email", "").strip()
        if not email or "@" not in email:
            return self.send_json(400, {"error": "Valid email required"})

        CAPTURED_EMAILS.append({"email": email, "time": time.time()})

        # Try to send clearance packet
        free_niche = next((n for n in NICHES if n["pdf_cost"] == 0), None)
        pdf_bytes = None
        if free_niche and SMTP_HOST:
            try:
                pdf_bytes = generate_professional_pdf_bytes(free_niche)
            except Exception:
                pdf_bytes = None

        sent = False
        if SMTP_HOST:
            sent = send_clearance_packet(email, pdf_bytes)

        status = "sent" if sent else "captured"
        _log_activity(f"Email captured: {email} — clearance packet {status}", f"email {status}")

        return self.send_json(200, {
            "status": status,
            "credits": 5,
            "xp": 10,
            "message": "Clearance packet sent" if sent else "Email captured. SMTP not configured."
        })

    # ── Admin ──

    def handle_admin_generate_pdf(self, body):
        niche_id = body.get("niche_id")
        niche = next((n for n in NICHES if n["id"] == niche_id), None)
        if not niche:
            return self.send_json(404, {"error": "Niche not found"})
        try:
            pdf_bytes = generate_professional_pdf_bytes(niche)
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'attachment; filename="{niche["filename"]}"')
            self.send_header("Content-Length", str(len(pdf_bytes)))
            self.end_headers()
            self.wfile.write(pdf_bytes)
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    # ── Admin Page ──

    def serve_admin_page(self):
        admin_path = OUTPUT_DIR / "admin.html"
        if admin_path.exists():
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(admin_path.read_bytes())
        else:
            self.send_json(404, {"error": "Admin page not found. Run main.py first."})

    def serve_admin_stats(self):
        total = len([r for r in REQUEST_LOG if r.get("status") == "ok"])
        niche_counts = {}
        for r in REQUEST_LOG:
            nid = r.get("niche_id", "unknown")
            niche_counts[nid] = niche_counts.get(nid, 0) + 1
        niche_names = {n["id"]: n["title"] for n in NICHES}
        breakdown = {}
        for nid, count in sorted(niche_counts.items(), key=lambda x: -x[1]):
            breakdown[niche_names.get(nid, nid)] = count
        recent_log = [
            {
                "time": r["time"],
                "niche": niche_names.get(r.get("niche_id", ""), r.get("niche_id", "")),
                "ip": r.get("ip", ""),
                "status": r.get("status", ""),
            }
            for r in REQUEST_LOG[-50:]
        ][::-1]
        uptime_secs = int(time.time() - SERVER_START)
        hours, remainder = divmod(uptime_secs, 3600)
        mins, secs = divmod(remainder, 60)
        uptime = f"{hours}h {mins}m {secs}s"

        # Compute average pdf size, error rate
        ok_count = len([r for r in REQUEST_LOG if r.get("status") == "ok"])
        error_count = len([r for r in REQUEST_LOG if r.get("status") == "error"])
        avg_size = 0
        sizes = [r.get("size", 0) for r in REQUEST_LOG if r.get("size")]
        if sizes:
            avg_size = sum(sizes) // len(sizes)

        self.send_json(200, {
            "total": total,
            "niche_breakdown": breakdown,
            "recent": recent_log,
            "uptime": uptime,
            "uptime_secs": uptime_secs,
            "total_requests": len(REQUEST_LOG),
            "ok_count": ok_count,
            "error_count": error_count,
            "avg_size": avg_size,
            "emails_captured": len(CAPTURED_EMAILS),
            "stripe_enabled": STRIPE_AVAILABLE,
            "smtp_enabled": bool(SMTP_HOST),
            "gemini_configured": bool(GEMINI_API_KEY),
        })

    # ── Helpers ──

    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Stripe-Signature")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # quieter logs


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8765
    server = HTTPServer((host, port), Handler)
    print(f"NemoClaw Intelligence Server: http://localhost:{port}")
    print(f"Static files: {OUTPUT_DIR}")
    print(f"Admin panel: http://localhost:{port}/admin")
    print(f"Stripe: {'ENABLED' if STRIPE_AVAILABLE else 'DISABLED (set STRIPE_SECRET_KEY)'}")
    print(f"SMTP: {'ENABLED' if SMTP_HOST else 'DISABLED (set SMTP_HOST)'}")
    print(f"PDF Preview: {'ENABLED' if PDF_PREVIEW_ENABLED else 'DISABLED'}")
    print(f"Gemini: {'ENABLED' if GEMINI_API_KEY else 'DISABLED'}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()
