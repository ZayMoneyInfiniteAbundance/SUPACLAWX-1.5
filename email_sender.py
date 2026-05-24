import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM, EMAIL_FROM_NAME, OUTPUT_DIR


def _send_raw(to_email: str, subject: str, html_body: str, attachment_bytes: bytes = None, attachment_name: str = None) -> bool:
    if not SMTP_HOST:
        return False
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))
    if attachment_bytes and attachment_name:
        part = MIMEApplication(attachment_bytes, _subtype="pdf")
        part.add_header("Content-Disposition", f'attachment; filename="{attachment_name}"')
        msg.attach(part)
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as s:
            s.starttls(context=ctx)
            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(EMAIL_FROM, [to_email], msg.as_string())
        return True
    except Exception:
        return False


def send_clearance_packet(to_email: str, pdf_bytes: bytes = None) -> bool:
    subject = "Your Recruit Clearance Packet — NemoClaw Network"
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#0D0D0F;color:#E8E8EC;padding:32px}}
h1{{color:#00D4AA;font-size:22px;margin-bottom:8px}}
p{{color:#8B8B96;font-size:14px;line-height:1.6}}
.cta{{display:inline-block;margin-top:16px;padding:12px 28px;background:#00D4AA;color:#0D0D0F;border-radius:12px;text-decoration:none;font-weight:600;font-size:14px}}
.footer{{margin-top:32px;font-size:11px;color:#4A4A52;border-top:1px solid #1A1A20;padding-top:16px}}
</style></head>
<body>
<h1>Clearance Packet Enclosed</h1>
<p>Welcome to the network, operator. Your Recruit Clearance Packet includes the Analyst Starter System and 5 intel credits to begin deploying.</p>
<p>This packet contains:<br>
- Analyst tier system deployment guide<br>
- First operational framework<br>
- Intelligence network access instructions</p>
<p>Deploy your first system within 48 hours to activate full clearance.</p>
<a class="cta" href="https://wa.me/14073015305">Contact Support</a>
<div class="footer">NemoClaw Operational Intelligence Network &middot; Clearance Division</div>
</body>
</html>"""
    return _send_raw(to_email, subject, html, attachment_bytes, "Recruit_Clearance_Packet.pdf")
