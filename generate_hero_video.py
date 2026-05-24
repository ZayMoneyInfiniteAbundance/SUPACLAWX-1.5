#!/usr/bin/env python3
import json, os, sys, time, requests
from pathlib import Path

API_KEY = "5965113ea28265fd619e8596b80329f1e7d72e0a203da8d323531243ffa96a78"
BASE_URL = "https://api.muapi.ai/api/v1"
OUTPUT_DIR = Path(__file__).parent / "output" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMG_MODEL = "gpt-image-2-text-to-image"
VID_MODEL = "seedance-pro-i2v-fast"
W = 78

def poll_result(rid, mw=300):
    url = f"{BASE_URL}/predictions/{rid}/result"
    h = {"x-api-key": API_KEY}; s = time.time()
    while time.time() - s < mw:
        r = requests.get(url, headers=h, timeout=30)
        if r.status_code == 200:
            d = r.json()
            if d.get("status") == "completed": return d
            if d.get("status") == "failed": return None
        time.sleep(3)
    return None

def gen_img(nid, pr, asp="16:9"):
    url = f"{BASE_URL}/{IMG_MODEL}"
    h = {"Content-Type":"application/json","x-api-key":API_KEY}
    p = {"prompt":pr,"aspect_ratio":asp,"num_images":1}
    print(f"  [{nid}] gpt-image-2..."); sys.stdout.flush()
    r = requests.post(url, json=p, headers=h, timeout=60)
    if r.status_code != 200: print(f"  ERR {r.status_code}: {r.text[:200]}"); return None
    rid = r.json().get("request_id")
    if not rid: return None
    print(f"  Request: {rid}"); sys.stdout.flush()
    res = poll_result(rid)
    if not res: return None
    url = (res.get("outputs") or [None])[0]
    if not url: return None
    ir = requests.get(url, timeout=60)
    if ir.status_code != 200: return None
    ct = ir.headers.get("Content-Type","")
    ext = "png"
    if "jpeg" in ct or "jpg" in ct: ext = "jpg"
    elif "webp" in ct: ext = "webp"
    fp = OUTPUT_DIR / f"{nid}.{ext}"
    fp.write_bytes(ir.content)
    print(f"  Saved: {fp.name} ({len(ir.content)}b)")
    return str(fp), url

def gen_vid(nid, img_url, pr):
    url = f"{BASE_URL}/{VID_MODEL}"
    h = {"Content-Type":"application/json","x-api-key":API_KEY}
    p = {"image_url":img_url,"prompt":pr,"aspect_ratio":"16:9"}
    print(f"  [{nid}] Seedance I2V..."); sys.stdout.flush()
    r = requests.post(url, json=p, headers=h, timeout=60)
    if r.status_code != 200: print(f"  ERR {r.status_code}: {r.text[:200]}"); return None
    rid = r.json().get("request_id")
    if not rid: return None
    print(f"  Request: {rid}"); sys.stdout.flush()
    res = poll_result(rid, mw=300)
    if not res: return None
    url = (res.get("outputs") or [None])[0]
    if not url: return None
    vr = requests.get(url, timeout=120)
    if vr.status_code != 200: return None
    ct = vr.headers.get("Content-Type","")
    ext = "mp4"
    if "webm" in ct: ext = "webm"
    fn = "hero.mp4" if nid == "hero" else f"{nid}.mp4"
    fp = OUTPUT_DIR / fn
    fp.write_bytes(vr.content)
    print(f"  Video: {fp.name} ({len(vr.content)}b)")
    return str(fp)

def main():
    print(f"{'='*W}\n  MuAPI Hero + Asset Videos\n{'='*W}")
    cost = 0.0
    # Hero
    cost += 0.09; hr = gen_img("hero",
        "Epic cinematic wide shot of a futuristic operational intelligence network. "
        "A massive holographic globe of luminous teal data streams in a dark command center. "
        "Floating holographic interfaces displaying AI workflows, automation pipelines, analytics. "
        "Glowing network nodes connected by threads of light across a vast dark space. "
        "Dark navy and teal color palette with warm amber accents. "
        "Volumetric light beams, god rays cutting through haze. "
        "Photorealistic, ultra-detailed, cinematic color grading, anamorphic lens. "
        "No text, no watermarks. 16:9.", "16:9")
    if hr: cost += 0.06; gen_vid("hero", hr[1],
        "Slow cinematic camera orbit around the central holographic globe. "
        "Data streams pulse and flow gently through the network. "
        "Subtle particle movement, glowing nodes flicker. "
        "Smooth elegant premium motion. Loopable. No text.")
    time.sleep(2)
    # 3 Assets
    assets = [
        ("ai-side-hustles",
         "Cinematic shot of a futuristic digital product factory. "
         "Automated AI pipelines as streams of luminous teal data flowing through transparent tubes "
         "into finished digital products floating in a dark workshop. "
         "Holographic dashboards showing revenue streams. "
         "Warm amber and teal accent lighting. Photorealistic, ultra-detailed. 3:2.",
         "Gentle slow motion. Data streams flow through tubes. "
         "Digital products float and rotate slowly. "
         "Subtle particles. Smooth cinematic motion. Loopable."),
        ("crypto-defi",
         "Epic cinematic visualization of a decentralized finance network. "
         "Glowing blockchain nodes connected by streams of teal and purple light "
         "forming a massive geometric structure floating in dark space. "
         "Smart contract code cascading like digital waterfalls. "
         "Holographic charts in background. Photorealistic, ultra-detailed. 3:2.",
         "Slow camera drift through the geometric blockchain structure. "
         "Light streams pulse along connection lines. "
         "Code cascades gently. Subtle particle glow. Loopable."),
        ("health-biohacking",
         "Cinematic shot of a futuristic bio-optimization lab. "
         "A translucent human form filled with flowing golden and teal energy pathways "
         "representing neural optimization. Dark lab with holographic vitals. "
         "Cyan and amber lighting. Photorealistic, volumetric fog. 3:2.",
         "Gentle pulsing energy flows through the translucent form. "
         "Holographic vitals float and rotate. "
         "Subtle light particles drift upward. Smooth premium motion. Loopable."),
    ]
    for aid, ip, vp in assets:
        cost += 0.09; r = gen_img(aid, ip, "16:9")
        if r: cost += 0.06; gen_vid(aid, r[1], vp)
        time.sleep(2)
    print(f"\n{'='*W}\n  DONE. Total: ${cost:.2f}\n{'='*W}")

if __name__ == "__main__":
    main()
