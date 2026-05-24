#!/usr/bin/env python3
import json, os, sys, time, requests
from pathlib import Path

API_KEY = "5965113ea28265fd619e8596b80329f1e7d72e0a203da8d323531243ffa96a78"
MODEL = "gpt4o-text-to-image"
BASE_URL = "https://api.muapi.ai/api/v1"
OUTPUT_DIR = Path(__file__).parent / "output" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = {
    "ai-ecommerce": """Cinematic wide shot of a futuristic e-commerce command center. A massive holographic display shows real-time sales data, AI product analytics, and a glowing 3D globe with order routes pulsing across continents. Dark blue and teal color scheme. Operators at sleek curved desks managing automated systems. Reflections on polished black floor. Photorealistic, ultra-detailed, 8K quality, dramatic lighting, volumetric light beams through window blinds. Epic scale, high-end technology aesthetic.""",

    "viral-content": """Cinematic shot of a hyper-modern content operations room. Multiple holographic screens display trending graphs, viral metrics, and automated content pipelines processing in real-time. Amber and electric blue neon lighting. A central AI core pulses with data streams. Dark atmospheric environment with dramatic rim lighting on the equipment. Photorealistic, ultra-detailed, cinematic color grading, anamorphic lens effect.""",

    "crypto-defi": """Epic cinematic visualization of a decentralized finance network. Glowing blockchain nodes connected by streams of light forming a massive geometric structure floating in dark space. Smart contract code cascading like digital waterfalls. Deep purple and cyan neon lighting. Holographic candlestick charts and yield curves in the background. Photorealistic, ultra-detailed, grand scale, sci-fi aesthetic, cinematic lighting with god rays.""",

    "productivity-hacks": """Cinematic top-down shot of a minimalist executive command center. A sleek glass desk with a transparent holographic interface displaying workflow automation, task pipelines, and productivity metrics. Soft warm accent lighting on matte black surfaces. Calm professional atmosphere with subtle teal glow. Photorealistic, ultra-detailed, editorial photography style, dramatic shadows.""",

    "health-biohacking": """Cinematic shot of a futuristic bio-optimization lab. A translucent human form outline filled with flowing golden energy pathways representing neural and hormonal optimization. Dark lab environment with holographic vitals and biometric data floating around. Cyan and amber scientific instrument lighting. Photorealistic, ultra-detailed, medical drama meets sci-fi aesthetic, volumetric fog.""",

    "dating-optimization": """Cinematic shot of a sophisticated social network visualization. Luminescent connection lines between glowing avatar nodes forming a complex relationship map in 3D space. Rose gold and teal color palette. Floating profile cards with compatibility scores. Dark moody background with bokeh lights. Photorealistic, ultra-detailed, modern elegant aesthetic, dramatic rim lighting.""",

    "digital-real-estate": """Epic cinematic visualization of a digital asset empire. Websites and online properties rendered as towering futuristic skyscrapers made of light and data. A massive valuation graph rising through the center. Drone-like aerial perspective looking up at the glowing buildings. Gold and electric blue lighting. Photorealistic, ultra-detailed, grand architectural scale, cinematic clouds.""",

    "remote-freedom": """Cinematic wide shot of a location-independent command hub. A sleek laptop open on a minimal desk with a holographic globe projecting above it showing connection routes spanning the world. Floor-to-ceiling windows overlooking a sunset city skyline. Warm golden hour light mixing with cool blue screen glow. Photorealistic, ultra-detailed, luxury travel aesthetic, editorial quality.""",

    "ai-side-hustles": """Cinematic shot of a futuristic digital product factory. Automated AI pipelines visualized as streams of luminous data flowing through transparent tubes into finished digital products that float in the air. Dark workshop environment with warm amber and teal accent lighting. Holographic dashboards showing revenue streams. Photorealistic, ultra-detailed, industrial meets digital age aesthetic.""",

    "home-fitness": """Cinematic shot of a futuristic home gym with AI integration. A muscular silhouette backlit by a large holographic display showing real-time biometrics, form correction overlays, and performance analytics. Dark environment with dramatic cyan lighting from below. Sweat droplets catching light. Photorealistic, ultra-detailed, high-end fitness commercial aesthetic, dramatic contrast.""",
}


def poll_result(request_id, max_wait=120):
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
        # Still processing, wait and retry
        time.sleep(3)
    print(f"  TIMEOUT after {max_wait}s")
    return None


def generate_image(niche_id, prompt):
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
    print(f"  Generating {niche_id}...")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"  ERROR: {resp.status_code} {resp.text[:300]}")
        return None
    data = resp.json()
    request_id = data.get("request_id")
    if not request_id:
        print(f"  WARNING: No request_id in response: {json.dumps(data)[:200]}")
        return None
    print(f"  Request ID: {request_id}, polling...")

    result = poll_result(request_id)
    if not result:
        return None

    # Extract image URL from result
    outputs = result.get("outputs", [])
    image_url = None
    if outputs:
        image_url = outputs[0]
    if not image_url:
        print(f"  WARNING: No outputs in result: {json.dumps(result)[:300]}")
        return None

    # Download the image
    img_resp = requests.get(image_url, timeout=60)
    if img_resp.status_code != 200:
        print(f"  ERROR downloading image: {img_resp.status_code}")
        return None
    ext = "jpg"
    ct = img_resp.headers.get("Content-Type", "")
    if "png" in ct:
        ext = "png"
    elif "webp" in ct:
        ext = "webp"
    elif "jpeg" in ct or "jpg" in ct:
        ext = "jpg"
    filepath = OUTPUT_DIR / f"{niche_id}.{ext}"
    filepath.write_bytes(img_resp.content)
    print(f"  Saved {filepath} ({len(img_resp.content)} bytes)")
    return filepath


def main():
    print(f"Generating images using {MODEL} on MuAPI...")
    print(f"Total: {len(PROMPTS)} images at $0.04 each = ${len(PROMPTS) * 0.04:.2f}")
    print()
    results = {}
    for niche_id, prompt in PROMPTS.items():
        filepath = generate_image(niche_id, prompt)
        results[niche_id] = filepath
        if filepath:
            print(f"  OK - {niche_id}: {filepath.name}")
        else:
            print(f"  FAILED - {niche_id}")
        print()
        time.sleep(1)
    print("=== Summary ===")
    success = [k for k, v in results.items() if v]
    failed = [k for k, v in results.items() if not v]
    print(f"Success: {len(success)}/{len(PROMPTS)}")
    if failed:
        print(f"Failed: {failed}")
        for f in failed:
            print(f"  - {f}")
    print("\nImages ready for use in store page.")


if __name__ == "__main__":
    main()
