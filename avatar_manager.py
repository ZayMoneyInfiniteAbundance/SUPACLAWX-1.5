import asyncio
import json
import os
import time
from pathlib import Path
from typing import Optional
from rich.console import Console

from muapi_client import MuAPIClient
from config import AVATARS_DIR, DEFAULT_AVATAR

_console = Console()


AVATAR_DB = AVATARS_DIR / "avatars.json"


def _load_avatars() -> list:
    if AVATAR_DB.exists():
        with open(AVATAR_DB) as f:
            return json.load(f)
    return []


def _save_avatars(avatars: list):
    AVATARS_DIR.mkdir(parents=True, exist_ok=True)
    with open(AVATAR_DB, "w") as f:
        json.dump(avatars, f, indent=2)


def get_avatar() -> dict:
    avatars = _load_avatars()
    if avatars:
        return avatars[0]
    return {
        "id": "default",
        "name": DEFAULT_AVATAR,
        "style": "professional",
        "status": "local_only"
    }


def register_avatar(avatar_data: dict):
    avatars = _load_avatars()
    avatars.insert(0, avatar_data)
    _save_avatars(avatars)


async def _poll_output(client: MuAPIClient, request_id: str, timeout: int = 90) -> Optional[str]:
    start = time.time()
    while time.time() - start < timeout:
        await asyncio.sleep(3)
        try:
            result = await client.poll_result(request_id)
            if result.get("status") == "completed":
                outputs = result.get("outputs") or []
                return outputs[0] if outputs else None
            if result.get("status") in ("failed", "error"):
                return None
        except Exception:
            continue
    return None


async def generate_thumbnail(prompt: str, timeout: int = 90) -> Optional[str]:
    client = MuAPIClient()
    result = await client.generate_image(prompt, resolution="1K", quality="medium")
    request_id = result.get("request_id")
    if not request_id:
        return None
    return await _poll_output(client, request_id, timeout=timeout)


async def generate_voiceover(text: str, voice_id: str = "male-optimistic-upbeat",
                              webhook_url: str = "") -> str:
    client = MuAPIClient()
    result = await client.generate_speech(prompt=text, voice_id=voice_id,
                                          webhook_url=webhook_url)
    return result.get("request_id", "")


async def generate_course_assets(course: dict) -> dict:
    client = MuAPIClient()
    title = course["title"]
    topic = course.get("topic", "")

    assets = {
        "thumbnail_url": None,
        "avatar_image_url": None,
        "video_url": None,
    }

    thumbnail = await client.generate_image(
        f"Professional course thumbnail for {title}, {topic}, "
        "blue and gold gradient, modern 3D design, text overlay area, "
        "16:9, photorealistic, high quality",
        resolution="1K", quality="medium"
    )
    tid = thumbnail.get("request_id")
    if tid:
        assets["thumbnail_url"] = await _poll_output(client, tid, timeout=90)

    avatar_img = await client.generate_image(
        f"Professional teacher portrait, {topic} expert, "
        "wearing business suit, confident smile, classroom background, "
        "photorealistic, professional lighting",
        resolution="1K", quality="medium"
    )
    aid = avatar_img.get("request_id")
    if aid:
        assets["avatar_image_url"] = await _poll_output(client, aid)

    _console.print("  Generating intro video (Seedance Pro)...")
    video_resp = await client._post("/api/v1/seedance-pro-t2v", {
        "prompt": f"Cinematic course intro: {title} — {topic}. "
                  "Professional ecommerce visualization with floating 3D product icons, "
                  "glowing blue and gold particle network, smooth orbiting camera motion, "
                  "warm cinematic lighting, premium brand feel, 1080p, 10 seconds, text space at bottom."
    })
    vid = video_resp.get("request_id")
    if vid:
        _console.print("  Polling video result (up to 5 min)...")
        assets["video_url"] = await _poll_output(client, vid, timeout=300)
        if assets["video_url"]:
            _console.print(f"  Video generated: {assets['video_url'][:60]}...")
            # Download locally for persistence
            import httpx
            try:
                r = httpx.get(assets["video_url"], timeout=120)
                video_path = Path("/Users/dvnmarketingstudios/nemoclaw-creator/output/assets/intro.mp4")
                video_path.parent.mkdir(parents=True, exist_ok=True)
                video_path.write_bytes(r.content)
                _console.print(f"  Saved locally: {video_path}")
            except Exception as e:
                _console.print(f"  Local save skipped: {e}")
    else:
        _console.print("  Video generation failed")

    return assets


async def check_muapi_status() -> dict:
    client = MuAPIClient()
    try:
        await client.health_check()
        models = await client.list_models()
        avatars = _load_avatars()
        return {
            "connected": True,
            "avatar_count": len(avatars),
            "models_available": len(models),
        }
    except Exception as e:
        return {
            "connected": False,
            "avatar_count": 0,
            "error": str(e),
        }
