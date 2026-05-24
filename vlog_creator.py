import json
import re
from datetime import datetime

import httpx

from config import OLLAMA_URL, OLLAMA_MODEL
from avatar_manager import get_avatar


def _extract_json_braces(text: str) -> str:
    brace_count = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == '{':
            if start == -1:
                start = i
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0 and start != -1:
                return text[start:i+1]
    return text


def _parse_llm_json(text: str) -> dict:
    text = _extract_json_braces(text)
    text = text.replace("\\'", "'")
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*\]', ']', text)
    for _ in range(3):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        import ast
        try:
            return ast.literal_eval(text)
        except Exception:
            pass
        backslash_pos = text.find("\\")
        if backslash_pos >= 0:
            next_char = text[backslash_pos+1] if backslash_pos+1 < len(text) else ""
            text = text[:backslash_pos] + next_char + text[backslash_pos+2:]
        else:
            break
    raise ValueError(f"Could not parse JSON from LLM response")


VLOG_SYSTEM_PROMPT = """You are a YouTube/TikTok vlog script writer. Create a short, engaging vlog script 
promoting a course. The vlog should have a charismatic host (the avatar) teaching or teasing the content.

Return ONLY valid JSON:
{
  "title": "Click-worthy vlog title",
  "hook": "First 5 seconds hook to grab attention",
  "script": [
    {"time": "0:00", "text": "script line", "visual": "what avatar does/shows"},
    {"time": "0:15", "text": "script line", "visual": "visual description"},
    {"time": "0:30", "text": "script line", "visual": "visual description"}
  ],
  "cta": "Call to action at the end",
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "duration_seconds": 60,
  "mood": "energetic|educational|inspirational"
}

Keep the vlog 30-90 seconds. Make it persuasive."""


async def generate_vlog(course: dict) -> dict:
    prompt = (
        f"Create a vlog script promoting this course:\n"
        f"Title: {course['title']}\n"
        f"Topic: {course['topic']}\n"
        f"Price: ${course['price']}\n"
        f"Modules: {[m['title'] for m in course['modules']]}\n"
        f"Key takeaways: {course.get('key_takeaways', [])}"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": VLOG_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.8, "num_predict": 2048}
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        resp.raise_for_status()
        content = resp.json()["message"]["content"].strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0].strip()

    vlog = _parse_llm_json(content)
    vlog["course_title"] = course["title"]
    vlog["generated_at"] = datetime.now().isoformat()

    avatar = get_avatar()
    vlog["avatar"] = avatar.get("name", "AI Teacher")
    vlog["avatar_style"] = avatar.get("style", "professional")

    return vlog


def render_vlog_html(vlog: dict) -> str:
    avatar_name = vlog.get("avatar", "AI Teacher")
    avatar_style = vlog.get("avatar_style", "")

    lines_html = ""
    for line in vlog.get("script", []):
        lines_html += f"""
        <div style="display: flex; gap: 12px; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #6b7280; font-family: monospace; min-width: 40px;">{line.get('time', '0:00')}</span>
            <div>
                <div style="color: #e5e7eb;">{line.get('text', '')}</div>
                <div style="color: #6b7280; font-size: 12px; margin-top: 2px;">🎬 {line.get('visual', '')}</div>
            </div>
        </div>"""

    html = f"""<div class="vlog-card" style="
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-radius: 16px;
    padding: 24px;
    color: white;
    font-family: system-ui, sans-serif;
    max-width: 640px;
    margin: 20px auto;
    border: 1px solid rgba(255,255,255,0.1);
">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
        <div style="
            width: 48px; height: 48px;
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        ">🎙️</div>
        <div>
            <div style="font-weight: 600;">{vlog.get('title', '')}</div>
            <div style="color: #94a3b8; font-size: 13px;">
                🧑‍🏫 {avatar_name} · {vlog.get('duration_seconds', 60)}s · {vlog.get('mood', 'educational')}
            </div>
        </div>
    </div>

    <div style="
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
        border-left: 3px solid #f59e0b;
    ">
        <div style="color: #f59e0b; font-size: 12px; font-weight: bold; text-transform: uppercase;">Hook</div>
        <div style="color: #e5e7eb; margin-top: 4px;">{vlog.get('hook', '')}</div>
    </div>

    {lines_html}

    <div style="
        margin-top: 16px;
        padding: 12px;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(34, 197, 94, 0.2);
    ">
        <div style="color: #22c55e; font-size: 12px; font-weight: bold;">🎯 CTA</div>
        <div style="color: #e5e7eb; margin-top: 2px;">{vlog.get('cta', '')}</div>
    </div>

    <div style="margin-top: 12px; display: flex; gap: 6px; flex-wrap: wrap;">
        {''.join(f'<span style="background: rgba(99,102,241,0.2); color: #818cf8; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{tag}</span>' for tag in vlog.get('hashtags', []))}
    </div>
</div>"""
    return html
