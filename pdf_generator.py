import json
import re
import urllib.request
import urllib.error
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
from config import GEMINI_API_KEY, GEMINI_MODEL


def _call_gemini(prompt: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        body = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.9}
        }).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode())
        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
        return ""
    except urllib.error.HTTPError as e:
        return f"[Service temporarily unavailable. Please try again in a few seconds. Error: {e.code}]"
    except Exception as e:
        return f"[Content generation error. Please try again.]"


def _sanitize(text):
    """Strip emoji + replace non-Helvetica chars."""
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        "\U00002600-\U000026FF\U0000FE00-\U0000FE0F]+", re.UNICODE)
    text = emoji_pattern.sub('', text)
    replacements = {
        '\u2014': '-- ', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '-',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return ''.join(c if ord(c) < 256 else '?' for c in text)


def _parse_sections(raw_text):
    sections = []
    lines = raw_text.split('\n')
    current = None

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r'^#{1,3}\s+', s):
            title = re.sub(r'\*+', '', re.sub(r'^#{1,3}\s+', '', s)).strip()
            if current:
                sections.append(current)
            current = {'title': title, 'items': []}
        elif re.match(r'^\*\*(.+?)\*\*', s) and len(s) < 60:
            title = s.replace('**', '').strip()
            if current:
                sections.append(current)
            current = {'title': title, 'items': []}
        elif current is None:
            current = {'title': 'Introduction', 'items': []}
            current['items'].append({'type': 'text', 'text': s})
        else:
            if s.startswith('- ') or s.startswith('* '):
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', s[2:]).strip()
                if text:
                    current['items'].append({'type': 'bullet', 'text': text})
            elif re.match(r'^\d+[.)]\s+', s):
                text = re.sub(r'^\d+[.)]\s+', '', s)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text).strip()
                if text:
                    current['items'].append({'type': 'numbered', 'text': text})
            elif s.startswith('> '):
                current['items'].append({'type': 'quote', 'text': s[2:].strip()})
            else:
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
                if text:
                    if len(text) < 60 and text.endswith(':') and text.isupper():
                        current['items'].append({'type': 'subheader', 'text': text})
                    else:
                        current['items'].append({'type': 'text', 'text': text})

    if current:
        sections.append(current)
    return sections


class ProfessionalPDF(FPDF):
    def __init__(self, niche, accent_color):
        super().__init__('P', 'mm', 'A4')
        self.niche = niche
        self.accent_r, self.accent_g, self.accent_b = accent_color
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margin(20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_text_color(180, 180, 180)
        self.set_font('Helvetica', '', 7)
        self.cell(0, 6, _sanitize(self.niche['title']), align='R')
        self.ln(3)
        self.set_draw_color(220, 220, 220)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-18)
        self.set_draw_color(220, 220, 220)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(3)
        self.set_text_color(160, 160, 160)
        self.set_font('Helvetica', '', 7)
        self.cell(85, 8, 'NemoClaw Academy', align='L')
        self.cell(20, 8, f'- {self.page_no()} -', align='C')
        self.cell(85, 8, datetime.now().strftime('%B %Y'), align='R')


def _add_cover(pdf, niche):
    pdf.add_page()
    w = 170
    r, g, b = pdf.accent_r, pdf.accent_g, pdf.accent_b

    pdf.set_fill_color(r, g, b)
    pdf.rect(0, 0, 210, 95, 'F')

    pdf.set_y(12)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(w, 6, 'NEMOCLAW ACADEMY', align='C')

    pdf.set_y(25)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(230, 230, 230)
    pdf.cell(w, 7, _sanitize(niche['subtitle']).upper(), align='C')

    pdf.set_y(38)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(w, 13, _sanitize(niche['title']), align='C')

    pdf.set_y(pdf.get_y() + 4)
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.3)
    pdf.line(80, pdf.get_y(), 130, pdf.get_y())

    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(w, 5, _sanitize(niche.get('description', '')), align='C')

    pdf.set_y(130)
    pdf.set_text_color(120, 120, 120)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(w, 7, 'Prepared exclusively for you', align='C')

    pdf.set_y(142)
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.5)
    pdf.line(75, pdf.get_y(), 135, pdf.get_y())

    pdf.set_y(152)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(r, g, b)
    pdf.cell(w, 8, 'NemoClaw Academy', align='C')

    pdf.set_y(162)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(140, 140, 140)
    pdf.cell(w, 6, 'AI Knowledge Vault', align='C')

    pdf.set_y(172)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(160, 160, 160)
    pdf.cell(w, 6, datetime.now().strftime('%B %d, %Y'), align='C')


def _add_toc(pdf, sections):
    pdf.add_page()
    w = 170
    r, g, b = pdf.accent_r, pdf.accent_g, pdf.accent_b

    pdf.set_text_color(r, g, b)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(w, 10, 'Contents', align='L')
    pdf.ln(6)
    pdf.set_draw_color(r, g, b)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(8)

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)
    for i, sec in enumerate(sections, 1):
        title = _sanitize(sec['title'])
        if len(title) > 55:
            title = title[:52] + '...'
        pdf.cell(160, 7, f'{i}.  {title}')
        pdf.ln(7)

    pdf.ln(5)
    pdf.set_text_color(160, 160, 160)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.multi_cell(w, 5, _sanitize('This guide was generated fresh just for you using AI. Content is for educational purposes and does not constitute professional advice.'))


def _add_section(pdf, section, section_num):
    w = 170
    r, g, b = pdf.accent_r, pdf.accent_g, pdf.accent_b

    pdf.ln(2)
    pdf.set_text_color(r, g, b)
    pdf.set_font('Helvetica', 'B', 15)
    pdf.multi_cell(w, 8, f'{section_num}. {_sanitize(section["title"])}')
    pdf.set_draw_color(r, g, b)
    pdf.set_line_width(0.2)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(3)

    for item in section['items']:
        t = item['type']
        text = _sanitize(item['text'])

        if t == 'text':
            pdf.set_text_color(50, 50, 50)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(w, 5.5, text)
            pdf.ln(1.5)

        elif t == 'subheader':
            pdf.ln(1)
            pdf.set_text_color(r, g, b)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.multi_cell(w, 6, text)
            pdf.set_text_color(50, 50, 50)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(1)

        elif t == 'bullet':
            pdf.set_text_color(50, 50, 50)
            pdf.set_font('Helvetica', '', 10)
            x0 = pdf.get_x()
            pdf.set_x(x0 + 5)
            pdf.set_text_color(r, g, b)
            pdf.cell(5, 5.5, '> ')
            pdf.set_text_color(50, 50, 50)
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(w - 10, 5.5, text)
            pdf.set_x(x0)

        elif t == 'numbered':
            pdf.set_text_color(50, 50, 50)
            pdf.set_font('Helvetica', '', 10)
            x0 = pdf.get_x()
            pdf.set_x(x0 + 5)
            pdf.multi_cell(w - 5, 5.5, text)
            pdf.set_x(x0)

        elif t == 'quote':
            pdf.set_x(25)
            pdf.set_text_color(120, 120, 120)
            pdf.set_font('Helvetica', 'I', 9)
            pdf.multi_cell(w - 10, 5, text)
            pdf.set_x(20)

    pdf.ln(2)


def generate_professional_pdf_bytes(niche):
    raw = _call_gemini(niche['prompt'])
    if not raw:
        raw = f"Content for {niche['title']} is being prepared. Please try again in a moment."

    sections = _parse_sections(raw)
    if not sections:
        sections = [{'title': 'Overview', 'items': [{'type': 'text', 'text': raw[:5000]}]}]

    color_hex = niche.get('color', '#10b981').lstrip('#')
    accent = (int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16))

    pdf = ProfessionalPDF(niche, accent)
    _add_cover(pdf, niche)
    _add_toc(pdf, sections)
    for i, sec in enumerate(sections, 1):
        _add_section(pdf, sec, i)

    buf = BytesIO()
    pdf.output(buf)
    return buf.getvalue()
