import json
from datetime import datetime

from config import TEASERS_DIR, FREE_LESSONS_COUNT, TEASER_BLUR_RADIUS, COURSES_DIR
from storage import save_teaser


def generate_teaser(course: dict) -> dict:
    first_module = course["modules"][0]
    free_lessons = first_module["lessons"][:FREE_LESSONS_COUNT]
    locked_count = sum(len(m["lessons"]) for m in course["modules"]) - len(free_lessons)

    teaser = {
        "title": course["title"],
        "subtitle": course.get("subtitle", ""),
        "price": course["price"],
        "free_lessons": [
            {"title": l["title"], "content": l["content"][:200] + "..."}
            for l in free_lessons
        ],
        "locked_lessons_count": locked_count,
        "total_modules": len(course["modules"]),
        "total_lessons": locked_count + len(free_lessons),
        "blur_radius": TEASER_BLUR_RADIUS,
        "call_to_action": f"Unlock full course for ${course['price']:.2f}",
        "generated_at": datetime.now().isoformat(),
    }

    save_teaser(course.get("id", "unknown"), teaser)
    return teaser


def render_teaser_html(teaser: dict) -> str:
    free_items = "".join(
        f"""<div style="
            background: rgba(34,197,94,0.1);
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-left: 3px solid #22c55e;
        ">
            <div style="font-weight: 500; font-size: 14px;">▶ {l['title']}</div>
            <div style="color: #94a3b8; font-size: 12px; margin-top: 4px;">{l['content'][:100]}...</div>
        </div>"""
        for l in teaser.get("free_lessons", [])
    )

    locked_html = f"""<div style="
        background: rgba(107,114,128,0.1);
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        filter: blur({teaser.get('blur_radius', 15)}px);
        user-select: none;
        pointer-events: none;
        margin-top: 12px;
    ">
        <div style="font-size: 24px; margin-bottom: 8px;">🔒</div>
        <div style="color: #6b7280;">+{teaser.get('locked_lessons_count', 0)} more lessons locked</div>
    </div>"""

    html = f"""<div class="course-teaser" style="
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-radius: 16px;
    padding: 24px;
    color: white;
    font-family: system-ui, sans-serif;
    max-width: 640px;
    margin: 20px auto;
    border: 1px solid rgba(255,255,255,0.1);
">
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: black;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">🎁 FREE PREVIEW</span>
    </div>

    <h2 style="font-size: 22px; margin-bottom: 4px;">{teaser['title']}</h2>
    <p style="color: #94a3b8; font-size: 14px; margin-bottom: 20px;">{teaser.get('subtitle', '')}</p>

    <div style="font-size: 13px; color: #6b7280; margin-bottom: 12px;">
        📚 {teaser['total_modules']} modules · {teaser['total_lessons']} lessons
    </div>

    {free_items}
    {locked_html}

    <div style="
        margin-top: 20px;
        background: rgba(245,158,11,0.1);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid rgba(245,158,11,0.2);
    ">
        <div style="font-size: 20px; font-weight: bold; color: #f59e0b;">
            ${teaser['price']:.2f}
        </div>
        <div style="
            margin-top: 10px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: black;
            padding: 10px 24px;
            border-radius: 24px;
            font-weight: bold;
            display: inline-block;
            cursor: pointer;
        ">🔓 Unlock Full Access</div>
    </div>
</div>"""
    return html
