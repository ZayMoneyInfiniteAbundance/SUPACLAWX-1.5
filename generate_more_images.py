#!/usr/bin/env python3
import json, os, sys, time, requests
from pathlib import Path

API_KEY = "5965113ea28265fd619e8596b80329f1e7d72e0a203da8d323531243ffa96a78"
MODEL = "gpt4o-text-to-image"
BASE_URL = "https://api.muapi.ai/api/v1"
OUTPUT_DIR = Path(__file__).parent / "output" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = {
    # ── HERO ──
    "hero": """Epic cinematic wide shot of a futuristic intelligence command center. A massive circular holographic globe dominates the center with glowing data streams, neural network connections, and real-time analytics pulsing across its surface. Teal and electric blue neon lighting cutting through dark atmospheric fog. Multiple layered holographic displays float in the air showing system status, deployment metrics, and global activity. Sleek dark architecture with reflective surfaces. Silhouetted operators at workstations in the foreground. Dramatic god rays from above. Volumetric lighting, ultra-detailed, 8K quality, Blade Runner meets Mission Control aesthetic, anamorphic lens flare, deep shadows, cinematic color grading.""",

    # ── PHANTOM TIER ──
    "phantom": """Cinematic shot of a hidden underground intelligence vault. A massive black monolith with glowing teal circuitry patterns stands in the center of a dark chamber. Holographic lock symbols and encrypted data streams float around it. Red and teal warning lights casting dramatic shadows. Restricted access signage glowing faintly. Steampunk meets cyberpunk aesthetic, ultra-detailed, heavy atmosphere, volumetric fog, dramatic rim lighting from below, elite secret facility vibes, 8K quality.""",

    # ── VERIFIED DEPLOYMENT CASE IMAGES ──
    "case-ecom": """Cinematic close-up shot of a sleek e-commerce dashboard glowing with real-time sales metrics. Gold and green upward trending graphs reflecting on a polished glass surface. Background blur of automated warehouse robots. Photorealistic, ultra-detailed, editorial photography, dramatic lighting, success visualization, rich colors.""",

    "case-content": """Cinematic shot of a content creator's command center. Multiple floating screens showing viral video analytics, engagement graphs spiking upward, and content calendar. Warm amber and teal lighting. Neon glow reflecting off a dark desk. Photorealistic, ultra-detailed, modern creator aesthetic, dramatic shadows, cinematic color grading.""",

    "case-crypto": """Cinematic shot of a cryptocurrency trading dashboard with massive green candles and profit metrics. Glowing blockchain visualization in the background. Gold and emerald green lighting. Dark sophisticated environment. Reflection on polished surfaces. Photorealistic, ultra-detailed, wealth and success aesthetic, dramatic rim lighting.""",

    "case-leads": """Cinematic shot of an automated lead generation pipeline visualization. Glowing funnel with golden data particles flowing through each stage. Conversion metrics and contact cards floating holographically. Deep blue and amber lighting. Photorealistic, ultra-detailed, sales technology aesthetic, dramatic contrast.""",

    "case-ads": """Cinematic shot of an advertising performance command center. Multiple screens showing ad creatives, ROAS metrics, and conversion funnels with explosive growth charts. Purple and electric blue neon aesthetic. Dark atmospheric room with data reflecting off surfaces. Photorealistic, ultra-detailed, high-stakes trading floor energy.""",

    "case-saas": """Cinematic shot of a SaaS analytics platform with hockey-stick growth graphs. User acquisition metrics glowing in gold and teal. Server rack lights blinking in the background. Modern sleek dashboard with real-time data. Photorealistic, ultra-detailed, silicon valley startup aesthetic, dramatic lighting.""",

    # ── SECTION DECORATIVE IMAGES ──
    "network-bg": """Cinematic abstract visualization of a global intelligence network. Thousands of glowing connection points forming a neural mesh across a dark space. Pulsing data packets traveling along fiber optic-like paths. Deep teal and indigo color palette. Ultra-detailed, fractal-like patterns, tech aesthetic, atmospheric, wallpaper quality.""",

    "clearance-bg": """Cinematic close-up of a glowing security clearance identification system. Holographic rank insignia floating above a dark terminal. Biometric scan lines and identity verification data streams. Deep blue and teal scientific lighting. Photorealistic, ultra-detailed, spy thriller aesthetic, dramatic macro shot.""",

    "deployment-bg": """Cinematic shot of a massive data center deployment visualization. Rack after rack of servers with blinking activity lights arranged in a circular pattern. Holographic deployment progress bars floating in the air above. Blue and cyan lighting. Photorealistic, ultra-detailed, grand scale, operations center aesthetic.""",

    "footer-bg": """Cinematic abstract of digital binary code and circuit patterns fading into darkness. Minimalist tech aesthetic with subtle teal glow. Deep black background with fine illuminated lines creating geometric patterns. Ultra-detailed, wallpaper quality, atmospheric, sophisticated.""",

    # ── RANK BADGE IMAGES ──
    "rank-recruit": """Close-up cinematic shot of a sleek metallic badge with the word RECRUIT etched in minimalist font. Dark titanium finish with subtle teal edge lighting. Clean professional macro photography, shallow depth of field, dramatic lighting, premium material aesthetic.""",

    "rank-analyst": """Close-up cinematic shot of a bronze metallic badge with the word ANALYST engraved. Warm metallic reflections on dark background. Premium macro photography, dramatic rim lighting, ultra-detailed metal texture, sophisticated.""",

    "rank-operator": """Close-up cinematic shot of a silver metallic badge with the word OPERATOR embossed. Brushed steel finish with cool blue reflections. Macro photography, ultra-detailed metal grain, dramatic lighting, premium quality.""",

    "rank-strategist": """Close-up cinematic shot of a gold metallic badge with the word STRATEGIST engraved in elegant font. Warm golden reflections and subtle sparkle. Ultra-detailed macro photography, luxury aesthetic, dramatic lighting, prestigious.""",

    "rank-architect": """Close-up cinematic shot of a platinum metallic badge with the word ARCHITECT etched in modern font. White precious metal finish with subtle prismatic reflections. Ultra-detailed macro photography, premium luxury aesthetic, dramatic rim lighting.""",

    "rank-phantom": """Close-up cinematic shot of a matte black badge with the word PHANTOM in ghostly faded text. Almost invisible until caught in dramatic side lighting. Dark and mysterious, stealth aesthetic, ultra-detailed macro photography, elite covert quality.""",
}

results_log = []

def poll_result(request_id, max_wait=180):
    url = f"{BASE_URL}/predictions/{request_id}/result"
    headers = {"x-api-key": API_KEY}
    start = time.time()
    while time.time() - start < max_wait:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "completed":
                return data
            elif data.get("status") == "failed":
                print(f"  FAILED: {data.get('error', 'unknown error')}")
                return None
        time.sleep(4)
    print(f"  TIMEOUT after {max_wait}s")
    return None

def generate_image(key, prompt):
    url = f"{BASE_URL}/{MODEL}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    payload = {
        "prompt": prompt,
        "aspect_ratio": "3:2",
        "num_images": 1,
    }
    print(f"[{key}] Generating...")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"  ERROR: {resp.status_code} {resp.text[:200]}")
        results_log.append((key, "FAILED", resp.text[:200]))
        return
    data = resp.json()
    request_id = data.get("request_id")
    if not request_id:
        print(f"  WARNING: No request_id")
        results_log.append((key, "FAILED", "no request_id"))
        return
    print(f"  Request: {request_id[:8]}... polling")
    result = poll_result(request_id)
    if not result:
        results_log.append((key, "FAILED", "no result"))
        return
    outputs = result.get("outputs", [])
    image_url = outputs[0] if outputs else None
    if not image_url:
        print(f"  WARNING: No outputs")
        results_log.append((key, "FAILED", "no outputs"))
        return
    img_resp = requests.get(image_url, timeout=60)
    if img_resp.status_code != 200:
        print(f"  ERROR downloading: {img_resp.status_code}")
        results_log.append((key, "FAILED", f"download {img_resp.status_code}"))
        return
    ext = "png"
    ct = img_resp.headers.get("Content-Type", "")
    if "jpeg" in ct or "jpg" in ct: ext = "jpg"
    elif "webp" in ct: ext = "webp"
    filepath = OUTPUT_DIR / f"{key}.{ext}"
    filepath.write_bytes(img_resp.content)
    size_kb = len(img_resp.content) // 1024
    print(f"  OK → {filepath.name} ({size_kb}KB)")
    results_log.append((key, "OK", f"{filepath.name} ({size_kb}KB)"))

def main():
    total_cost = len(PROMPTS) * 0.04
    print(f"Generating {len(PROMPTS)} images via {MODEL} ($0.04 each = ${total_cost:.2f} total)")
    print("═" * 50)
    for i, (key, prompt) in enumerate(PROMPTS.items(), 1):
        print(f"\n[{i}/{len(PROMPTS)}] ", end="")
        generate_image(key, prompt)
        time.sleep(0.5)
    print("\n" + "═" * 50)
    print("SUMMARY:")
    ok = [r for r in results_log if r[1] == "OK"]
    fail = [r for r in results_log if r[1] != "OK"]
    print(f"  Success: {len(ok)}/{len(PROMPTS)}")
    for k, s, d in ok:
        print(f"    ✓ {k} → {d}")
    if fail:
        print(f"  Failed: {len(fail)}")
        for k, s, d in fail:
            print(f"    ✗ {k}: {d}")
    print(f"\nTotal cost: ${len(ok) * 0.04:.2f} (${total_cost:.2f} max)")
    print("Ready to go wild 🚀")

if __name__ == "__main__":
    main()
