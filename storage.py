import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import COURSES_DIR, VLOGS_DIR, TEASERS_DIR, AVATARS_DIR


def save_course(course: dict) -> str:
    COURSES_DIR.mkdir(parents=True, exist_ok=True)
    slug = course["title"].lower().replace(" ", "_")[:40]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{slug}.json"
    path = COURSES_DIR / filename
    course["id"] = filename.replace(".json", "")
    course["created_at"] = datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(course, f, indent=2)
    return str(path)


def save_vlog(vlog: dict) -> str:
    VLOGS_DIR.mkdir(parents=True, exist_ok=True)
    slug = vlog["title"].lower().replace(" ", "_")[:40]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{slug}.json"
    path = VLOGS_DIR / filename
    vlog["id"] = filename.replace(".json", "")
    vlog["created_at"] = datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(vlog, f, indent=2)
    return str(path)


def save_teaser(course_id: str, teaser: dict) -> str:
    TEASERS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"teaser_{course_id}.json"
    path = TEASERS_DIR / filename
    teaser["course_id"] = course_id
    teaser["created_at"] = datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(teaser, f, indent=2)
    return str(path)


def get_recent_courses(limit: int = 10) -> list:
    if not COURSES_DIR.exists():
        return []
    files = sorted(COURSES_DIR.glob("*.json"), reverse=True)[:limit]
    courses = []
    for f in files:
        with open(f) as fh:
            courses.append(json.load(fh))
    return courses


def get_course_count() -> int:
    if not COURSES_DIR.exists():
        return 0
    return len(list(COURSES_DIR.glob("*.json")))


def get_total_earnings() -> float:
    courses = get_recent_courses(1000)
    return sum(c.get("price", 0) for c in courses if c.get("sold"))
