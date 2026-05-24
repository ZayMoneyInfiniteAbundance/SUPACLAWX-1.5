import json
import random
import re
from datetime import datetime
from typing import Optional

import httpx

from config import OLLAMA_URL, OLLAMA_MODEL, COURSE_TOPICS


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
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    try:
        import ast
        return ast.literal_eval(text)
    except Exception:
        pass
    raise ValueError(f"Could not parse JSON from LLM response")


SYSTEM_PROMPT = """You are a course creation expert. Generate a complete mini-course on the given topic.
The course should be practical, actionable, and focused on making money online.

Return ONLY valid JSON with this structure:
{
  "title": "Course title",
  "subtitle": "Short subtitle",
  "topic": "main topic",
  "difficulty": "beginner|intermediate|advanced",
  "price": 9.99,
  "intro_video_script": "60-second hook script that sells the course",
  "modules": [
    {
      "title": "Module title",
      "lessons": [
        {
          "title": "Lesson title",
          "content": "Lesson content with actionable steps",
          "duration_minutes": 5
        }
      ]
    }
  ],
  "key_takeaways": ["takeaway1", "takeaway2", "takeaway3"],
  "target_audience": "who this is for"
}

Generate 2-3 modules with 2-3 lessons each. Keep content concise but valuable."""


async def generate_course(topic: Optional[str] = None) -> dict:
    if topic is None:
        topic = random.choice(COURSE_TOPICS)

    prompt = f"Create a mini-course about: {topic}"

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.8, "num_predict": 4096}
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        resp.raise_for_status()
        content = resp.json()["message"]["content"].strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0].strip()

    course = _parse_llm_json(content)
    course["topic"] = topic
    course["generated_at"] = datetime.now().isoformat()
    return course


def generate_teaser_html(course: dict) -> str:
    from config import TEASER_BLUR_RADIUS, FREE_LESSONS_COUNT, COURSE_PRICE
    first_module = course["modules"][0]
    first_lesson = first_module["lessons"][0]
    price = course.get("price", COURSE_PRICE)

    html = f"""<div class="course-teaser" style="
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border-radius: 16px;
    padding: 32px;
    color: white;
    font-family: system-ui, sans-serif;
    max-width: 720px;
    margin: 20px auto;
">
    <div style="text-align: center; margin-bottom: 24px;">
        <span style="
            background: #f59e0b;
            color: black;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        ">FREE PREVIEW</span>
    </div>

    <h2 style="font-size: 24px; margin-bottom: 4px;">{course['title']}</h2>
    <p style="color: #a5b4fc; margin-bottom: 20px;">{course.get('subtitle', '')}</p>

    <div style="
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.15);
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="
                width: 40px; height: 40px;
                background: #22c55e;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            ">▶</div>
            <div>
                <div style="font-weight: 600;">{first_lesson['title']}</div>
                <div style="color: #94a3b8; font-size: 14px;">Free · {first_lesson.get('duration_minutes', 5)} min</div>
            </div>
        </div>
    </div>

    <div style="
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 16px;
        filter: blur({TEASER_BLUR_RADIUS if not FREE_LESSONS_COUNT > 1 else 0}px);
        user-select: none;
        pointer-events: none;
    ">
        <div style="display: flex; align-items: center; gap: 12px; opacity: 0.4;">
            <div style="
                width: 40px; height: 40px;
                background: #6b7280;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            ">🔒</div>
            <div>
                <div style="font-weight: 600;">Full Course ({len(course['modules'])} modules)</div>
                <div style="color: #94a3b8; font-size: 14px;">Unlock for ${price:.2f}</div>
            </div>
        </div>
    </div>

    <div style="margin-top: 20px; text-align: center;">
        <div style="
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: black;
            padding: 12px 32px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 16px;
            display: inline-block;
            cursor: pointer;
        ">🔓 Unlock Full Course — ${price:.2f}</div>
        <p style="color: #94a3b8; font-size: 13px; margin-top: 8px;">
            {course.get('key_takeaways', [''])[0] if course.get('key_takeaways') else ''}
        </p>
    </div>
</div>"""
    return html
