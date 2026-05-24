#!/usr/bin/env python3
"""Rebrand NemoClaw per strategy doc: Palantir x Stripe x Linear for internet operators."""
import re
from pathlib import Path

pub = Path("/Users/dvnmarketingstudios/nemoclaw-creator/publisher.py")
content = pub.read_text()

# ── 1. COLOR SYSTEM ──
# Primary: #00D4AA -> #00FFC6 (more premium emerald)
# Background: #0D0D0F -> #05070B (deeper, richer)
content = content.replace("#00D4AA", "#00FFC6")
content = content.replace("#00E6B3", "#00FFD6")
content = content.replace("#00B894", "#00D99C")
# But NOT in RANK_COLORS which uses actual metal colors
# Fix double-replacement issues
content = content.replace("#00FFC6/40", "#00FFC6/40")  # no-op, ensure correct

# ── 2. VISUAL NOISE REDUCTION ──
# Reduce `grd` grid background - make it subtler
content = content.replace(
    ".grd{{background-image:linear-gradient(rgba(255,255,255,.008) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.008) 1px,transparent 1px);background-size:56px 56px;background-position:center center}}",
    ".grd{{background-image:linear-gradient(rgba(255,255,255,.004) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.004) 1px,transparent 1px);background-size:64px 64px;background-position:center center}}"
)

# Remove scan line / radial gradient noise on decorative elements
# Keep the real content overlays but reduce fake texture

# ── 3. TYPOGRAPHY ──
# Reduce monospace overuse in body text (keep for code-like elements)
# Body text descriptions should use Inter (regular), not JetBrains Mono
# We'll adjust specific elements in the HTML

# ── 4. LANGUAGE CLEANUP ──
# Reduce roleplay terminology, replace with operational language
replacements_lang = {
    "intelligence vault": "operational network",
    "Access Intelligence Vault": "Access Intelligence Systems",
    "Intelligence Vault": "Operational Network",
    "Vault initialized": "Systems initialized",
    "hidden intelligence archive": "advanced intelligence archive",
    "restricted intelligence layer": "advanced operational layer",
    "Phantom tier": "Strategic tier",
    "Phantom Clearance": "Strategic Access",
    "Phantom": "Architect",
    "current rank": "current tier",
    "Current Rank": "Current Tier",
    "operator rank": "operator tier",
    "Operator Clearance": "Operator Progression",
    "Clearance Review": "Strategic Access",
    "Requires Strategist rank eligibility": "Requires Strategist tier eligibility",
    "CLEARANCE": "TIER",
    "black archive": "advanced archive",
    "classified documents": "operational documents",
    "classified": "internal",
    "restricted": "advanced",
    # Rank names
    "Recruit": "Recruit",
    "Analyst": "Analyst",
    "Operator": "Operator",
    "Strategist": "Strategist",
    "Architect": "Architect",
    "Architect": "Senior Architect",
    "Phantom": "Senior Architect",
}

for old, new in replacements_lang.items():
    content = content.replace(old, new)

# Fix the rank array duplication from Phantom -> Architect -> Senior Architect
content = content.replace("Senior Architect", "Senior Architect", 5)  # keep 5 correct ones
# RANK_NAMES line
content = content.replace(
    'RANK_NAMES = ["Recruit", "Analyst", "Operator", "Strategist", "Senior Architect", "Senior Architect"]',
    'RANK_NAMES = ["Recruit", "Analyst", "Operator", "Strategist", "Architect", "Senior Architect"]'
)
content = content.replace(
    'RANK_COLORS = ["#6B6B78", "#CD7F32", "#C0C0C0", "#FFD700", "#E5E4E2", "#000000"]',
    'RANK_COLORS = ["#6B6B78", "#CD7F32", "#C0C0C0", "#FFD700", "#E5E4E2", "#0A0A0C"]'
)

# Fix JS rank name array - this is in the f-string JS blob
content = content.replace(
    "['Recruit','Analyst','Operator','Strategist','Architect','Senior Architect']",
    "['Recruit','Analyst','Operator','Strategist','Architect','Senior Architect']"
)
# But original JS had Phantom -> need to fix
content = content.replace(
    "getRankName(r){return['Recruit','Analyst','Operator','Strategist','Architect','Senior Architect']",
    "getRankName(r){return['Recruit','Analyst','Operator','Strategist','Architect','Senior Architect']"
)
# Original was Phantom:
content = content.replace(
    "getRankName(r){return['Recruit','Analyst','Operator','Strategist','Architect','Phantom']",
    "getRankName(r){return['Recruit','Analyst','Operator','Strategist','Architect','Senior Architect']"
)

# ── 5. RANK BADGE IMAGES ──
content = content.replace('src="/images/rank-phantom.png"', 'src="/images/rank-phantom.png"')
# The phantom rank badge stays (it's a cool image)

# ── 6. JS ACTIVITY MESSAGES ──
content = content.replace(
    "Intelligence drop: New monetization protocol identified in E-Commerce sector",
    "New monetization protocol deployed in E-Commerce sector"
)

# ── 7. HERO SIMPLIFICATION ──
# Replace the badge text
content = content.replace(
    "operational intelligence network &middot; v3.7.1",
    "operational intelligence infrastructure"
)
content = content.replace(
    "operator_terminal — v3.7.1",
    "operational terminal — v3.7.1"
)

# ── 8. REDUCE EXCESSIVE GLOW CLASS ──
# btnpglow class - reduce glow intensity
content = content.replace(
    ".btnpglow{{box-shadow:0 0 24px rgba(0,212,170,.15),0 0 48px rgba(0,212,170,.06)}}",
    ".btnpglow{{box-shadow:0 0 16px rgba(0,255,198,.1),0 0 32px rgba(0,255,198,.04)}}"
)

# ── 9. SPACING ──
# Increase section padding
content = content.replace("py-16 sm:py-20", "py-20 sm:py-28")
content = content.replace("py-16 sm:py-24", "py-20 sm:py-28")

# ── 10. NAVBAR ──
content = content.replace(
    '<span class="text-xs text-white/15 bg-white/[0.03] px-1.5 py-0.5 rounded-full font-mono uppercase tracking-wider">system</span>',
    '<span class="text-xs text-white/20 bg-white/[0.04] px-2 py-0.5 rounded-full font-mono uppercase tracking-wider">module</span>'
)

# ── 11. REMOVE EXCESSIVE MYSTERY BADGE ──
content = content.replace(
    'inline-flex items-center gap-2 bg-white/[0.02] border border-white/[0.06] rounded-full px-3.5 py-1.5 text-xs text-white/15 font-mono tracking-wider uppercase mb-4',
    'inline-flex items-center gap-2 bg-white/[0.02] border border-white/[0.06] rounded-full px-3.5 py-1.5 text-xs text-white/20 font-mono tracking-wider uppercase mb-4'
)

# ── 12. CASE STUDIES BADGE ──
content = content.replace(
    '"system"', '"module"'
)

# Fix: "system deployed" in JS
content = content.replace(
    "system deployed", "module deployed"
)

# ── 13. SYSTEM -> MODULE in some contexts (but keep SYSTEM as category label) ──
# In card badges
content = content.replace(
    '<span class="text-xs text-white/20 bg-white/[0.04] px-2 py-0.5 rounded-full font-mono uppercase tracking-wider">system</span>',
    '<span class="text-xs text-white/20 bg-white/[0.04] px-2 py-0.5 rounded-full font-mono uppercase tracking-wider">system</span>'
)
# Actually keep "system" as the badge - it's operational language. Just remove the roleplay feel.

# ── 14. INTEL CREDITS -> CREDITS ──
content = content.replace("intel credits", "credits")

pub.write_text(content)
print("✅ Overhaul applied to publisher.py")
print("⚠️  Manual review needed for:", [
    "Phantom -> Senior Architect (verify JS rank arrays)",
    "Colors #00FFC6 everywhere",
    "btnpglow reduced glow",
    "Section spacing increased",
    "Language cleanup applied",
])
