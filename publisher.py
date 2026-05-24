import json
from datetime import datetime
from pathlib import Path
from config import NICHES, COIN_PACKS, BADGES, STREAK_BONUS, WHATSAPP_NUMBER, OUTPUT_DIR


def _svg(path_d, cls="w-5 h-5"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="{path_d}"/></svg>'


OUTCOMES = {
    "ai-side-hustles": "Automated digital product systems: fulfillment, GPT workflows, monetization funnels, pricing optimization",
    "crypto-defi": "Automated yield architecture: smart contract interactions, liquidity deployment, risk-managed staking protocols",
    "health-biohacking": "Systematic optimization protocols: sleep architecture, cognitive enhancement, longevity automation",
    "ai-ecommerce": "Full-stack e-commerce automation: AI product research, chatbot service, listing optimization, predictive inventory",
    "viral-content": "Content-to-revenue pipeline: trend detection, automated production, audience segmentation, monetization",
    "digital-real-estate": "Digital asset acquisition pipeline: valuation algorithms, SEO automation, flip optimization, exit timing",
    "dating-optimization": "Relationship acquisition system: profile optimization AI, message sequencing, selection algorithms",
    "productivity-hacks": "Executive function automation: deep work protocols, AI task management, environment design",
    "home-fitness": "Physical transformation system: program generation, progress tracking, recovery optimization",
    "remote-freedom": "Location independence infrastructure: income routing, jurisdiction stacking, operational mobility",
}

ICONS = {
    "ai-side-hustles": "M9 3v2M15 3v2M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zM3 10h18M3 14h18M3 18h18",
    "crypto-defi": "M12 2l8 5v10l-8 5-8-5V7l8-5zM12 2v20M4 7l8 5 8-5M4 17l8 5 8-5",
    "health-biohacking": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12h6M12 9v6",
    "ai-ecommerce": "M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4zM3 6h18M16 10a4 4 0 0 1-8 0M12 10v8",
    "viral-content": "M5 3l14 9-14 9V3z",
    "digital-real-estate": "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM9 22V12h6v10",
    "dating-optimization": "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.8z",
    "productivity-hacks": "M13 2L4 14h7l-2 8 9-12h-7z",
    "home-fitness": "M6.5 6.5l11 11M6.5 17.5l11-11M12 5v14M5 12h14",
    "remote-freedom": "M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zM2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z",
}

RISK = {"ai-side-hustles":"Low","crypto-defi":"Medium","health-biohacking":"Low","ai-ecommerce":"Medium","viral-content":"Low","digital-real-estate":"Medium","dating-optimization":"Low","productivity-hacks":"Low","home-fitness":"Low","remote-freedom":"Low"}
TTR = {"ai-side-hustles":"4-6h","crypto-defi":"2-3h","health-biohacking":"1-2h","ai-ecommerce":"6-8h","viral-content":"3-5h","digital-real-estate":"4-6h","dating-optimization":"1h","productivity-hacks":"30m","home-fitness":"1h","remote-freedom":"3-4h"}
DIFF = {"ai-side-hustles":6,"crypto-defi":8,"health-biohacking":4,"ai-ecommerce":7,"viral-content":5,"digital-real-estate":8,"dating-optimization":3,"productivity-hacks":2,"home-fitness":3,"remote-freedom":6}
OP_COUNT = {"ai-side-hustles":187,"crypto-defi":142,"health-biohacking":203,"ai-ecommerce":312,"viral-content":428,"digital-real-estate":94,"dating-optimization":156,"productivity-hacks":389,"home-fitness":267,"remote-freedom":106}

DELIVERABLES = {
    "ai-side-hustles": "8 workflows, prompt library, setup guide, templates",
    "crypto-defi": "6 automation scripts, risk framework, wallet setup guide",
    "health-biohacking": "5 protocols, tracking templates, supplement guide",
    "ai-ecommerce": "12 workflows, product research AI, chatbot templates",
    "viral-content": "10 content templates, scheduling automation, analytics dashboard",
    "digital-real-estate": "7 acquisition frameworks, SEO templates, valuation tools",
    "dating-optimization": "4 optimization scripts, message templates, profile guide",
    "productivity-hacks": "6 automation workflows, task templates, focus protocols",
    "home-fitness": "5 program templates, tracking system, recovery protocols",
    "remote-freedom": "8 business frameworks, income routing guide, legal templates",
}

BEST_FOR = {
    "ai-side-hustles": "Creators & Solopreneurs",
    "crypto-defi": "Crypto Investors",
    "health-biohacking": "Health Optimizers",
    "ai-ecommerce": "E-Commerce Operators",
    "viral-content": "Content Creators",
    "digital-real-estate": "Digital Investors",
    "dating-optimization": "Singles & Coaches",
    "productivity-hacks": "Professionals & Founders",
    "home-fitness": "Fitness Enthusiasts",
    "remote-freedom": "Digital Nomads",
}

CATEGORIES = {
    "ai-side-hustles": "automation",
    "crypto-defi": "growth",
    "health-biohacking": "lifestyle",
    "ai-ecommerce": "automation",
    "viral-content": "monetization",
    "digital-real-estate": "growth",
    "dating-optimization": "lifestyle",
    "productivity-hacks": "automation",
    "home-fitness": "lifestyle",
    "remote-freedom": "automation",
}

RELATED = {
    "ai-side-hustles": ["viral-content", "ai-ecommerce"],
    "crypto-defi": ["digital-real-estate", "remote-freedom"],
    "health-biohacking": ["home-fitness", "productivity-hacks"],
    "ai-ecommerce": ["ai-side-hustles", "viral-content"],
    "viral-content": ["ai-ecommerce", "ai-side-hustles"],
    "digital-real-estate": ["crypto-defi", "remote-freedom"],
    "dating-optimization": ["productivity-hacks", "health-biohacking"],
    "productivity-hacks": ["remote-freedom", "ai-side-hustles"],
    "home-fitness": ["health-biohacking", "productivity-hacks"],
    "remote-freedom": ["productivity-hacks", "crypto-defi"],
}

RANK_NAMES = ["Recruit", "Analyst", "Operator", "Strategist", "Architect", "Senior Architect"]
RANK_COLORS = ["#6B6B78", "#CD7F32", "#C0C0C0", "#FFD700", "#E5E4E2", "#0A0A0C"]
RANK_REQS = [0, 1, 3, 5, 10, 999]

SYSTEM_NAMES = {
    "ai-side-hustles": "AI Commerce Automation Stack",
"crypto-defi": "Automated Capital Allocation System",
    "health-biohacking": "AI Health Optimization Protocol",
    "ai-ecommerce": "AI E-Commerce Automation Suite",
    "viral-content": "AI Content Monetization Engine",
    "digital-real-estate": "Digital Asset Growth Engine",
    "dating-optimization": "AI Social Optimization Framework",
    "productivity-hacks": "AI Productivity Automation",
    "home-fitness": "AI Fitness & Recovery System",
    "remote-freedom": "Remote Business Automation",
}

CASE_STUDIES = [
    {"name": "tactical_mike", "role": "Operator", "system": "AI Commerce Automation Stack", "result": "$2,847 first 30 days", "quote": "Deployed the full pipeline in 6 hours. First automated sale at day 11. The fulfillment workflow alone saved 20h/week."},
    {"name": "system_sarah", "role": "Strategist", "system": "AI Content Monetization Engine", "result": "340% ROAS", "quote": "Took 3 days to configure all 8 modules. Content production went from 3h per post to 11 minutes. Revenue tripled in week 2."},
    {"name": "yield_jackson", "role": "Operator", "system": "Automated Capital Allocation System", "result": "12.4% APY on $3,400", "quote": "Smart contract interactions are fully automated. I checked once after setup and it was already generating yield. 45 min total."},
    {"name": "growth_anika", "role": "Strategist", "system": "AI E-Commerce Automation Suite", "result": "210% conversion lift", "quote": "Product research AI found 3 winning items in the first scan. Chatbot handled 847 customer queries day one. Zero manual work."},
    {"name": "focus_james", "role": "Analyst", "system": "AI Productivity Automation", "result": "Reclaimed 28h/week", "quote": "The deep work protocol alone doubled my output. AI task management eliminated all decision fatigue. First week was transformative."},
]


def _build_js():
    return """(function() {
var SK='nemoclaw_state';var s=load();
var niches=[{"id": "ai-side-hustles", "title": "AI Side Hustles", "subtitle": "ChatGPT Money Blueprint", "description": "Make money with AI tools — no experience needed.", "emoji": "🤖", "pdf_cost": 10, "filename": "chatgpt_money_blueprint.pdf", "color": "#10b981"}, {"id": "crypto-defi", "title": "Crypto & DeFi", "subtitle": "Passive Income Guide", "description": "Crypto passive income strategies for 2026.", "emoji": "₿", "pdf_cost": 20, "filename": "crypto_passive_income.pdf", "color": "#f59e0b"}, {"id": "health-biohacking", "title": "Health & Biohacking", "subtitle": "Longevity Protocol", "description": "Science-backed longevity and optimization.", "emoji": "🧬", "pdf_cost": 15, "filename": "longevity_protocol.pdf", "color": "#8b5cf6"}, {"id": "ai-ecommerce", "title": "AI E-Commerce", "subtitle": "Automated Store System", "description": "AI-powered dropshipping and store automation.", "emoji": "🛒", "pdf_cost": 20, "filename": "ai_ecommerce_system.pdf", "color": "#ef4444"}, {"id": "viral-content", "title": "Viral Content Machine", "subtitle": "Social Media Growth 2026", "description": "Grow on TikTok, IG, and YouTube with AI.", "emoji": "📱", "pdf_cost": 30, "filename": "viral_content_machine.pdf", "color": "#3b82f6"}, {"id": "digital-real-estate", "title": "Digital Real Estate", "subtitle": "Website Flipping Playbook", "description": "Buy, build, and flip websites for profit.", "emoji": "🌐", "pdf_cost": 25, "filename": "website_flipping_playbook.pdf", "color": "#14b8a6"}, {"id": "dating-optimization", "title": "Online Dating", "subtitle": "Dating App Optimization", "description": "AI-optimized profiles and messaging.", "emoji": "💘", "pdf_cost": 8, "filename": "dating_app_optimization.pdf", "color": "#ec4899"}, {"id": "productivity-hacks", "title": "Productivity Hacks", "subtitle": "ADHD Hacker System", "description": "Hyperfocus and workflow optimization.", "emoji": "⚡", "pdf_cost": 0, "filename": "adhd_hacker_system.pdf", "color": "#f97316"}, {"id": "home-fitness", "title": "Home Fitness", "subtitle": "No-Gym Workout Bible", "description": "Build muscle at home with zero equipment.", "emoji": "💪", "pdf_cost": 0, "filename": "home_workout_bible.pdf", "color": "#22c55e"}, {"id": "remote-freedom", "title": "Remote Work Freedom", "subtitle": "Digital Nomad Starter Kit", "description": "Escape the 9-5 and work from anywhere.", "emoji": "🏝️", "pdf_cost": 35, "filename": "digital_nomad_starter.pdf", "color": "#06b6d4"}];

var packs=[{"id": "starter", "coins": 10, "price": 9.0, "bonus": 0}, {"id": "popular", "coins": 25, "price": 19.0, "bonus": 3}, {"id": "advanced", "coins": 75, "price": 49.0, "bonus": 10}, {"id": "elite", "coins": 200, "price": 99.0, "bonus": 40}];

var sysNames={"ai-side-hustles": "AI Commerce Automation Stack", "crypto-defi": "Automated Capital Allocation System", "health-biohacking": "AI Health Optimization Protocol", "ai-ecommerce": "AI E-Commerce Automation Suite", "viral-content": "AI Content Monetization Engine", "digital-real-estate": "Digital Asset Growth Engine", "dating-optimization": "AI Social Optimization Framework", "productivity-hacks": "AI Productivity Automation", "home-fitness": "AI Fitness & Recovery System", "remote-freedom": "Remote Business Automation"};
var opCounts={"ai-side-hustles": 187, "crypto-defi": 142, "health-biohacking": 203, "ai-ecommerce": 312, "viral-content": 428, "digital-real-estate": 94, "dating-optimization": 156, "productivity-hacks": 389, "home-fitness": 267, "remote-freedom": 106};
var outcomes={"ai-side-hustles": "Automated digital product systems: fulfillment, GPT workflows, monetization funnels, pricing optimization", "crypto-defi": "Automated yield architecture: smart contract interactions, liquidity deployment, risk-managed staking protocols", "health-biohacking": "Systematic optimization protocols: sleep architecture, cognitive enhancement, longevity automation", "ai-ecommerce": "Full-stack e-commerce automation: AI product research, chatbot service, listing optimization, predictive inventory", "viral-content": "Content-to-revenue pipeline: trend detection, automated production, audience segmentation, monetization", "digital-real-estate": "Digital asset acquisition pipeline: valuation algorithms, SEO automation, flip optimization, exit timing", "dating-optimization": "Relationship acquisition system: profile optimization AI, message sequencing, selection algorithms", "productivity-hacks": "Executive function automation: deep work protocols, AI task management, environment design", "home-fitness": "Physical transformation system: program generation, progress tracking, recovery optimization", "remote-freedom": "Location independence infrastructure: income routing, jurisdiction stacking, operational mobility"};
var RANK_REQS=[0, 1, 3, 5, 10, 999];
var ICONS={"ai-side-hustles": "M9 3v2M15 3v2M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zM3 10h18M3 14h18M3 18h18", "crypto-defi": "M12 2l8 5v10l-8 5-8-5V7l8-5zM12 2v20M4 7l8 5 8-5M4 17l8 5 8-5", "health-biohacking": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12h6M12 9v6", "ai-ecommerce": "M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4zM3 6h18M16 10a4 4 0 0 1-8 0M12 10v8", "viral-content": "M5 3l14 9-14 9V3z", "digital-real-estate": "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM9 22V12h6v10", "dating-optimization": "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.8z", "productivity-hacks": "M13 2L4 14h7l-2 8 9-12h-7z", "home-fitness": "M6.5 6.5l11 11M6.5 17.5l11-11M12 5v14M5 12h14", "remote-freedom": "M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zM2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"};
var DIFF={"ai-side-hustles": 6, "crypto-defi": 8, "health-biohacking": 4, "ai-ecommerce": 7, "viral-content": 5, "digital-real-estate": 8, "dating-optimization": 3, "productivity-hacks": 2, "home-fitness": 3, "remote-freedom": 6};
var RELATED={"ai-side-hustles":["viral-content","ai-ecommerce"],"crypto-defi":["digital-real-estate","remote-freedom"],"health-biohacking":["home-fitness","productivity-hacks"],"ai-ecommerce":["ai-side-hustles","viral-content"],"viral-content":["ai-ecommerce","ai-side-hustles"],"digital-real-estate":["crypto-defi","remote-freedom"],"dating-optimization":["productivity-hacks","health-biohacking"],"productivity-hacks":["remote-freedom","ai-side-hustles"],"home-fitness":["health-biohacking","productivity-hacks"],"remote-freedom":["productivity-hacks","crypto-defi"]};
var selected=null,selectedPack=null,downloading=false,drawer=false,exitShown=false,actInterval=null;

function load(){try{var r=localStorage.getItem(SK);if(r)return JSON.parse(r)}catch(e){}return{coins:5,downloads:[],streak:0,lastLogin:null,xp:0}}
function save(){try{localStorage.setItem(SK,JSON.stringify(s))}catch(e){}}
function getRank(){var c=s.downloads.length;if(c>=10)return 5;if(c>=5)return 4;if(c>=3)return 3;if(c>=1)return 2;return 1}
function getRankName(r){return['Recruit','Analyst','Operator','Strategist','Architect','Senior Architect'][Math.min(r,5)]}
function getRankColor(r){return['#6B6B78','#CD7F32','#C0C0C0','#FFD700','#E5E4E2','#000000'][Math.min(r,5)]}
function updateUX(){var bal=document.getElementById('bal');if(bal)bal.textContent=s.coins;var dl=document.getElementById('dl');if(dl)dl.textContent=s.downloads.length;var xp=document.getElementById('xp');if(xp)xp.textContent=(s.xp||0)+' XP';var rk=document.getElementById('rank');if(rk){var r=getRank();rk.textContent=getRankName(r);rk.style.color=getRankColor(r)}var rk2=document.getElementById('rank2');if(rk2){var r=getRank();rk2.textContent=getRankName(r)}var bar=document.getElementById('rankBar');if(bar){var c=s.downloads.length;var nxt=RANK_REQS.find(function(x){return x>c})||RANK_REQS[RANK_REQS.length-1];var prev=RANK_REQS.filter(function(x){return x<=c});var p=prev[prev.length-1]||0;var pct=nxt===p?100:Math.round((c-p)/(nxt-p)*100);bar.style.width=Math.min(pct,100)+'%'}var act=document.getElementById('actCount');if(act)act.textContent=(140+Math.floor(Math.random()*20)).toLocaleString();var sys=document.getElementById('sysCount');if(sys)sys.textContent=(2184+s.downloads.length).toLocaleString()}
function fly(n){for(var i=0;i<Math.min(n,8);i++)(function(){var e=document.createElement('div');e.className='fly';e.innerHTML='<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="#00FFC6" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';e.style.left=(window.innerWidth*0.2+Math.random()*window.innerWidth*0.6)+'px';e.style.bottom='100px';e.style.animationDelay=(i*60)+'ms';document.body.appendChild(e);setTimeout(function(){e.remove()},1000)})()}
function openDr(){drawer=true;var d=document.getElementById('dr');d.classList.remove('hidden');requestAnimationFrame(function(){document.getElementById('drb').classList.remove('op0','pev');document.getElementById('drp').classList.remove('txf')});document.body.style.overflow='hidden'}
window.closeDr=function(){drawer=false;document.getElementById('drb').classList.add('op0','pev');document.getElementById('drp').classList.add('txf');document.body.style.overflow='';setTimeout(function(){document.getElementById('dr').classList.add('hidden');document.getElementById('dmBg').src=''},400)}
function showDr(id){document.querySelectorAll('.drc').forEach(function(e){e.classList.add('hidden')});document.getElementById(id).classList.remove('hidden')}
window.openMod=function(id){var n=niches.find(function(x){return x.id===id});if(!n)return;selected=n;var sn=sysNames[n.id]||n.title;document.getElementById('dmTitle').textContent=sn;document.getElementById('dmSys').textContent='SYSTEM: '+sn;document.getElementById('dmOut').textContent=outcomes[n.id]||'';document.getElementById('dmDesc').textContent=n.description;document.getElementById('dmOps').textContent=(opCounts[n.id]||0).toLocaleString()+' deployments';document.getElementById('dmIcon').innerHTML='<svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="'+(ICONS[n.id]||'')+'"/></svg>';document.getElementById('dmBg').src='/images/'+n.id+'.png';var diff=DIFF[n.id]||5;document.getElementById('dmDiff').innerHTML='<div class="flex gap-1">'+Array(10).fill(0).map(function(_,i){return '<div class="w-2 h-2 rounded-full '+(i<diff?'bg-[#00FFC6]/60':'bg-white/[0.06]')+'"></div>'}).join('')+'</div>';var cost=document.getElementById('dmCost');cost.innerHTML=n.pdf_cost===0?'<span class="text-emerald-400 font-semibold">Free</span>':'<span class="text-white/50 text-[12px] font-mono">'+n.pdf_cost+' credits</span>';var btn=document.getElementById('dmBtn');if(n.pdf_cost===0||s.coins>=n.pdf_cost){btn.disabled=false;btn.classList.remove('opacity-50','cursor-not-allowed');btn.setAttribute('onclick','showQuestions()');btn.innerHTML='Calibrate &amp; Deploy'}else{var need=n.pdf_cost-s.coins;btn.disabled=false;btn.classList.remove('opacity-50','cursor-not-allowed');btn.onclick=openShopFromMod;btn.innerHTML='Get '+need+' Credits to Deploy'};document.getElementById('dmPrice').innerHTML=n.pdf_cost===0?'Free':'<span class="text-white/30 line-through text-xs font-mono">$'+Math.round(n.pdf_cost*2.8+7)+'</span> <span class="text-white font-semibold">'+n.pdf_cost+' credits</span>';showRelated(n.id);showDr('drMod');openDr()}
window.preview=function(id){var n=niches.find(function(x){return x.id===id});if(!n)return;selected=n;var sn=sysNames[n.id]||n.title;document.getElementById('dpTitle').textContent=sn;document.getElementById('dpSub').textContent='SYSTEM: '+sn;document.getElementById('dpOut').textContent=outcomes[n.id]||'';document.getElementById('dpIcon').innerHTML='<svg class="w-12 h-12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="'+(ICONS[n.id]||'')+'"/></svg>';var img=document.getElementById('dpImg');if(img){img.classList.add('op0');img.src='/preview-pdf/'+n.id};showDr('drPrev');openDr()}
window.dl=function(){var n=selected;if(!n||s.coins<n.pdf_cost||downloading)return;var nn=selected;if(!nn||s.coins<nn.pdf_cost||downloading)return;downloading=true;var btn=document.getElementById('dmBtn');btn.disabled=true;btn.innerHTML='Deploying';var sgs=['initializing','configuring','deploying','verifying'];var si=0;var tmr=setInterval(function(){si++;if(si<sgs.length)btn.innerHTML=sgs[si]},1200);var ctrl=new AbortController();var to=setTimeout(function(){ctrl.abort()},60000);fetch('/generate-pdf',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({niche_id:nn.id}),signal:ctrl.signal}).then(function(r){clearInterval(tmr);clearTimeout(to);if(!r.ok)throw new Error('Deployment failed');return r.blob()}).then(function(blob){s.coins-=nn.pdf_cost;s.xp=(s.xp||0)+25;if(!s.downloads.includes(nn.id))s.downloads.push(nn.id);save();updateUX();var url=URL.createObjectURL(blob);var a=document.createElement('a');a.href=url;a.download=nn.filename;document.body.appendChild(a);a.click();setTimeout(function(){document.body.removeChild(a);URL.revokeObjectURL(url)},300);fly(3);closeDr();toast('System Deployed',sysNames[nn.id]||nn.title+' - operational');addActivity(s.downloads.length+' systems deployed','deployment completed');var rel=RELATED[nn.id];if(rel&&rel.length){var rn=niches.find(function(x){return x.id===rel[0]});if(rn&&rn.pdf_cost>0){setTimeout(function(){toast('Complete Your Stack','Operators who deployed '+sysNames[nn.id]+' also deployed '+sysNames[rn.id]+'. '+rn.pdf_cost+' credits.')},4000)}};downloading=false}).catch(function(err){clearInterval(tmr);clearTimeout(to);btn.disabled=false;btn.innerHTML='Deploy System';toast('Error',err.name==='AbortError'?'Timed out. Retry.':(err.message||'Failed.'));downloading=false})}
window.showBundle=function(){toast('Growth Bundle','3 systems for 45 credits (save 15). Purchase credits to unlock.');setTimeout(showShop,1200)}
window.showShop=function(){showDr('drShop');openDr()}
window.buy=function(id){var p=packs.find(function(x){return x.id===id});if(!p)return;selectedPack=p;document.getElementById('bpName').textContent=p.coins+' credits'+(p.bonus?' (+'+p.bonus+' free)':'');document.getElementById('bpPrice').textContent='$'+p.price.toFixed(2);document.getElementById('bpCoins').textContent=p.coins+(p.bonus?' + '+p.bonus+' free':'');showDr('drBuy');openDr()}
window.confirmBuy=function(){var p=selectedPack;if(!p)return;var pp=selectedPack;if(!pp)return;closeDr();toast('Processing','Connecting to payment gateway...');fetch('/create-checkout-session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pack_id:pp.id})}).then(function(r){return r.json()}).then(function(data){if(data.simulated){setTimeout(function(){s.coins+=data.credits||10;s.xp=(s.xp||0)+15;save();updateUX();fly(5);toast('Credits Deposited',(data.credits||10)+' credits added (simulated)')},600)}else if(data.url){window.location.href=data.url}else{toast('Error','Payment gateway unavailable.')}}).catch(function(err){toast('Error',err.message||'Connection failed')})}
window.showSub=function(){showDr('drSub');openDr()}
window.subPro=function(){closeDr();setTimeout(function(){toast('Application Received','Your request is under review. We will respond within 24 hours.')},600)}
window.wa=function(){window.open('https://wa.me/14073015305','_blank')}
window.closeToast=function(){document.getElementById('toast').classList.add('hidden');var p=document.getElementById('tpb');if(p){p.style.transition='none';p.style.width='0%'}}
function toast(title,msg){document.getElementById('toT').textContent=title;document.getElementById('toM').textContent=msg;var el=document.getElementById('toast');el.classList.remove('hidden');var pb=document.getElementById('tpb');if(pb){pb.style.transition='none';pb.style.width='0%';requestAnimationFrame(function(){pb.style.transition='width 4s linear';pb.style.width='100%'})};if(window._totmr)clearTimeout(window._totmr);window._totmr=setTimeout(function(){el.classList.add('hidden');if(pb){pb.style.transition='none';pb.style.width='0%'}},5000)}

var acts=['@tactical_mike deployed AI Commerce Stack — $2,847 first 30 days','@system_sarah activated Content Monetization Engine — 340% ROAS','3 new members joined Analyst tier','System update: Module 7 v2.1 deployed to all tiers','@yield_jackson verified 12.4% APY on Capital Allocation System','@growth_anika reported 210% conversion lift on e-commerce deployment','@focus_james completed Productivity Automation — reclaimed 28h/week','5 members upgraded to Operator tier this hour','New automation workflow deployed in E-Commerce sector']
function addActivity(msg,detail){var el=document.getElementById('feed');if(!el)return;var d=new Date();var ts=d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0');var div=document.createElement('div');div.className='text-xs text-white/20 font-mono flex items-center gap-2';div.innerHTML='<span class="text-white/10">['+ts+']</span> <span class="text-[#00FFC6]/40">member</span> '+msg;el.insertBefore(div,el.firstChild);if(el.children.length>8)el.removeChild(el.lastChild)}
function showActivity(){var msg=acts[Math.floor(Math.random()*acts.length)];addActivity(msg);var el=document.createElement('div');el.className='fixed bottom-24 left-4 z-[90] max-w-xs bg-[#05070B]/90 border border-white/[0.06] rounded-xl p-3 shadow-2xl op0 transition-all duration-500';el.innerHTML='<div class="flex items-start gap-2"><div class="w-1.5 h-1.5 rounded-full bg-[#00FFC6] mt-0.5 pd"></div><div><div class="text-xs text-white/30 font-mono leading-relaxed">'+msg+'</div></div></div>';document.body.appendChild(el);setTimeout(function(){el.classList.add('op100')},50);setTimeout(function(){el.classList.remove('op100');setTimeout(function(){el.remove()},500)},5000)}
function connectSSE(){if(!window.EventSource)return false;var sse=new EventSource('/events');sse.addEventListener('init',function(e){try{var events=JSON.parse(e.data);events.forEach(function(ev){addActivity(ev.msg||'')})}catch(ex){}});sse.addEventListener('activity',function(e){try{var ev=JSON.parse(e.data);addActivity(ev.msg||'');var el=document.createElement('div');el.className='fixed bottom-24 left-4 z-[90] max-w-xs bg-[#05070B]/90 border border-white/[0.06] rounded-xl p-3 shadow-2xl op0 transition-all duration-500';el.innerHTML='<div class="flex items-start gap-2"><div class="w-1.5 h-1.5 rounded-full bg-[#00FFC6] mt-0.5 pd"></div><div><div class="text-xs text-white/30 font-mono leading-relaxed">'+(ev.msg||'')+'</div></div></div>';document.body.appendChild(el);setTimeout(function(){el.classList.add('op100')},50);setTimeout(function(){el.classList.remove('op100');setTimeout(function(){el.remove()},500)},5000)}catch(ex){}});sse.onerror=function(){sse.close();if(!actInterval)actInterval=setInterval(showActivity,22000+Math.random()*18000)};return true}
var params=new URLSearchParams(window.location.search);if(params.get('checkout')==='success'&&params.get('session_id')){var sid=params.get('session_id');fetch('/verify-session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sid})}).then(function(r){return r.json()}).then(function(data){if(data.verified||data.simulated){s.coins+=data.credits||0;s.xp=(s.xp||0)+15;save();updateUX();fly(8);toast('Payment Confirmed',(data.credits||0)+' credits added to vault')}}).catch(function(){});window.history.replaceState({},document.title,'/')}
document.addEventListener('mouseleave',function(e){if(exitShown||e.clientY>0||drawer)return;exitShown=true;document.getElementById('lcModal').classList.remove('hidden')})
window.closeLC=function(){document.getElementById('lcModal').classList.add('hidden')}
window.capLC=function(){var email=document.getElementById('lcEmail').value;if(!email||!email.includes('@')){document.getElementById('lcErr').textContent='Valid email required.';return}document.getElementById('lcErr').textContent='';document.getElementById('lcEmail').disabled=true;fetch('/capture-email',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email})}).then(function(r){return r.json()}).then(function(data){closeLC();if(data.credits)s.coins+=data.credits;if(data.xp)s.xp=(s.xp||0)+data.xp;save();updateUX();toast('Credits Claimed',data.message||'Check email for your free deployment packet.');localStorage.setItem('nemoclaw_email',email)}).catch(function(){document.getElementById('lcErr').textContent='Server error. Try again.';document.getElementById('lcEmail').disabled=false})}
window.filterCategory=function(cat){document.querySelectorAll('.mod').forEach(function(c){var show=cat==='all'||c.dataset.category===cat;c.style.display=show?'':'none'});document.querySelectorAll('.cf').forEach(function(b){b.classList.remove('bg-[#00FFC6]/15','text-[#00FFC6]','border-[#00FFC6]/25');b.classList.add('bg-white/[0.04]','text-white/40','border-white/[0.06]')});var active=document.querySelector('.cf[data-cat="'+cat+'"]');if(active){active.classList.remove('bg-white/[0.04]','text-white/40','border-white/[0.06]');active.classList.add('bg-[#00FFC6]/15','text-[#00FFC6]','border-[#00FFC6]/25')}}
window.showRelated=function(id){var rel=RELATED[id];if(!rel)return;var c=document.getElementById('dmRelated');c.innerHTML='';rel.forEach(function(rid){var n=niches.find(function(x){return x.id===rid});if(!n)return;var sn=sysNames[n.id]||n.title;var b=document.createElement('button');b.className='w-full text-left bg-white/[0.03] hover:bg-white/[0.05] border border-white/[0.06] hover:border-white/[0.10] rounded-xl p-3 transition-all duration-300 group';b.innerHTML='<div class="flex items-center justify-between"><div class="flex items-center gap-2"><div class="w-6 h-6 rounded-lg flex items-center justify-center" style="background:'+n.color+'18;border:1px solid '+n.color+'25"><svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="'+(ICONS[n.id]||'')+'"/></svg></div><div><div class="text-xs font-semibold text-white/80">'+sn+'</div><div class="text-[10px] text-white/20 font-mono">'+n.pdf_cost+' credits</div></div></div><span class="text-white/20 group-hover:text-[#00FFC6]/60 transition text-xs font-mono">Deploy</span></div></button>';b.onclick=function(e){e.stopPropagation();openMod(rid)};c.appendChild(b)});if(c.children.length===0)c.innerHTML='<div class="text-xs text-white/15 font-mono">No related systems.</div>'}
window.openShopFromMod=function(){closeDr();setTimeout(showShop,300)}
var dqAnswers={};window.selectQ=function(cat,val,btn){dqAnswers[cat]=val;btn.parentNode.querySelectorAll('.qo').forEach(function(b){b.classList.remove('selected')});btn.classList.add('selected');var db=document.getElementById('dqDeploy');if(dqAnswers.exp&&dqAnswers.goal&&dqAnswers.time){db.disabled=false;db.classList.remove('opacity-50','cursor-not-allowed')}else{db.disabled=true;db.classList.add('opacity-50','cursor-not-allowed')}};window.showQuestions=function(){if(!selected)return;var sn=sysNames[selected.id]||selected.title;document.getElementById('dqSysName').textContent='Calibrating: '+sn;dqAnswers={};document.querySelectorAll('.qo').forEach(function(b){b.classList.remove('selected')});var db=document.getElementById('dqDeploy');db.disabled=true;db.classList.add('opacity-50','cursor-not-allowed');showDr('drQuestions');openDr()};window.startTailoredDeploy=function(){if(!selected||!dqAnswers.exp||!dqAnswers.goal||!dqAnswers.time)return;s.deployAnswers=dqAnswers;save();closeDr();setTimeout(dl,200)}
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&drawer)closeDr()})
document.addEventListener('click',function(e){var card=e.target.closest('.mod[data-id]');if(card){var id=card.getAttribute('data-id');if(id)window.openMod(id)}})
var obs=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting)e.target.classList.add('vis')})},{threshold:0.08});document.querySelectorAll('.rv').forEach(function(el){obs.observe(el)})
(function(){var c=document.getElementById('pc');if(!c)return;var ctx=c.getContext('2d');var p=[],w,h;function ri(){w=c.width=c.offsetWidth;h=c.height=c.offsetHeight}ri();window.addEventListener('resize',ri);var n=Math.min(50,Math.floor(w*h/8000));for(var i=0;i<n;i++)p.push({x:Math.random()*w,y:Math.random()*h,vx:(Math.random()-.5)*.3,vy:(Math.random()-.5)*.3,r:Math.random()*1.5+1});(function a(){ctx.clearRect(0,0,w,h);for(var i=0;i<p.length;i++){var o=p[i];o.x+=o.vx;o.y+=o.vy;if(o.x<0||o.x>w)o.vx*=-1;if(o.y<0||o.y>h)o.vy*=-1;ctx.beginPath();ctx.arc(o.x,o.y,o.r,0,Math.PI*2);ctx.fillStyle='rgba(0,255,198,'+(.15+Math.random()*.1)+')';ctx.fill();for(var j=i+1;j<p.length;j++){var t=p[j];var dx=o.x-t.x;var dy=o.y-t.y;var d=dx*dx+dy*dy;if(d<20000){ctx.beginPath();ctx.moveTo(o.x,o.y);ctx.lineTo(t.x,t.y);ctx.strokeStyle='rgba(0,255,198,'+((1-d/20000)*.15)+')';ctx.lineWidth=.5;ctx.stroke()}}}requestAnimationFrame(a)})()})();
(function(){var cards=document.querySelectorAll('.mod');var raf=null;cards.forEach(function(c){c.addEventListener('mousemove',function(e){if(raf)return;raf=requestAnimationFrame(function(){raf=null;var r=c.getBoundingClientRect();var x=(e.clientX-r.left)/r.width-.5;var y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(1000px) rotateY('+(x*3)+'deg) rotateX('+(-y*3)+'deg)'})},{passive:true});c.addEventListener('mouseleave',function(){if(raf){cancelAnimationFrame(raf);raf=null}c.style.transform='perspective(1000px) rotateY(0deg) rotateX(0deg)'})})})();
(function(){var o2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var el=e.target;var v=parseInt(el.getAttribute('data-count'))||0;var c=0;var s=Math.max(1,Math.floor(v/30));var t=setInterval(function(){c+=s;if(c>=v){c=v;clearInterval(t)}el.textContent=c.toLocaleString()},30);o2.unobserve(el)}})});document.querySelectorAll('.cv').forEach(function(el){o2.observe(el)})})();
document.addEventListener('click',function(e){var btn=e.target.closest('.btnp,.btns');if(!btn)return;var r=document.createElement('span');r.className='ripple';var rect=btn.getBoundingClientRect();var s=Math.max(rect.width,rect.height);r.style.width=r.style.height=s+'px';r.style.left=(e.clientX-rect.left-s/2)+'px';r.style.top=(e.clientY-rect.top-s/2)+'px';btn.appendChild(r);setTimeout(function(){r.remove()},600)});
window.closeAv=function(){document.getElementById('avModal').classList.add('hidden');var v=document.getElementById('avVid');if(v)v.pause()};
var _openModOrig=window.openMod;window.openMod=function(id){var n=niches.find(function(x){return x.id===id});if(!n)return;_openModOrig(id)};
setTimeout(function(){try{var m=document.getElementById('avModal');var v=document.getElementById('avVid');if(!m||!v)return;m.classList.remove('hidden');try{v.play().catch(function(){})}catch(e){}document.getElementById('avTitle').textContent='Welcome, Operator';document.getElementById('avDesc').textContent='I have 10 intelligence systems ready for deployment. Browse the collection and deploy what fits your operations.';document.getElementById('avBtn').onclick=function(){closeAv();document.getElementById('modules').scrollIntoView({behavior:'smooth'})}}catch(e){}},5000);
(function(){var vw={};niches.forEach(function(n){vw[n.id]=Math.floor(7+Math.random()*15)});var badges=document.querySelectorAll('.mod[data-id]');badges.forEach(function(b){var id=b.getAttribute('data-id');var ct=vw[id]||3;var el=document.createElement('div');el.className='absolute top-3 right-3 z-10 urg';el.innerHTML='<span class="text-[10px] text-[#00FFC6]/60 bg-black/40 backdrop-blur-sm px-1.5 py-0.5 rounded-full font-mono flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-[#00FFC6] pg"></span>'+ct+' viewing</span>';b.appendChild(el)});setInterval(function(){badges.forEach(function(b){var id=b.getAttribute('data-id');var ct=vw[id]||3;var ch=ct+Math.floor(Math.random()*3)-1;if(ch<2)ch=2;if(ch>20)ch=20;vw[id]=ch;var el=b.querySelector('.urg span');if(el)el.innerHTML='<span class="w-1.5 h-1.5 rounded-full bg-[#00FFC6] pg"></span>'+ch+' viewing'})},8000)})();
var _purchases=['just now','3m ago','7m ago','12m ago','18m ago','24m ago','31m ago','45m ago','1h ago','2h ago'];setInterval(function(){addActivity('Someone deployed a system '+_purchases[Math.floor(Math.random()*_purchases.length)])},15000);
try{var _d=localStorage.getItem('nemoclaw_lastLogin');var _n=new Date().toDateString();if(_d!==_n){localStorage.setItem('nemoclaw_lastLogin',_n);s.coins=(s.coins||0)+5;s.xp=(s.xp||0)+10;s.streak=(s.streak||0)+1;if(s.streak===3){s.coins+=8}if(s.streak===7){s.coins+=25}if(s.streak===14){s.coins+=50}if(s.streak===30){s.coins+=100}save()}}catch(e){}
updateUX();if(!connectSSE()){actInterval=setInterval(showActivity,22000+Math.random()*18000)}setTimeout(function(){addActivity('Platform initialized — 10 systems available')},500);setTimeout(function(){addActivity('2,184 deployments completed across network')},1500)
})();"""


def build_store_page(pdf_files: dict = None) -> str:
    today = datetime.now().strftime("%B %d, %Y")

    mod_html = ""

    for n in NICHES:
        id = n["id"]
        outcome = OUTCOMES[id]
        risk = RISK[id]
        ttr = TTR[id]
        op_count = OP_COUNT[id]
        sys_name = SYSTEM_NAMES[id]
        icon = _svg(ICONS[id], "w-4 h-4")
        deliverables = DELIVERABLES.get(id, "Automation workflows, templates, setup guide")
        category = CATEGORIES.get(id, "general")
        cost_str = "Free" if n["pdf_cost"] == 0 else str(n["pdf_cost"])
        cost_label = "" if n["pdf_cost"] == 0 else "credits"

        mod_html += f"""
<div class="mod group relative bg-[#0F1115] border border-white/[0.06] hover:border-[#00FFC6]/30 rounded-2xl transition-all duration-500 cursor-pointer overflow-hidden h-[260px] sm:h-[240px]" onclick="openMod('{id}')" data-id="{id}" data-category="{category}">
  <img src="/images/{id}.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.50] group-hover:opacity-[0.75] transition-all duration-700 pointer-events-none" loading="lazy">
  {f'<video autoplay muted loop playsinline poster="/images/{id}.png" class="absolute inset-0 w-full h-full object-cover opacity-[0.50] group-hover:opacity-[0.75] transition-all duration-700 pointer-events-none" preload="none"><source src="/images/{id}.mp4" type="video/mp4"></video>' if id in ["ai-side-hustles", "crypto-defi", "health-biohacking", "ai-ecommerce", "viral-content", "digital-real-estate", "dating-optimization", "productivity-hacks", "home-fitness", "remote-freedom"] else ''}
  <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" style="background:linear-gradient(135deg, rgba(0,255,198,0.06) 0%, transparent 60%)"></div>
  <div class="absolute inset-0 pointer-events-none" style="background:linear-gradient(to top, rgba(15,17,21,0.98) 0%, rgba(15,17,21,0.75) 40%, rgba(15,17,21,0.30) 70%, rgba(15,17,21,0.10) 100%)"></div>
  <div class="relative z-10 p-5 flex flex-col h-full justify-end">
    <div class="flex items-center justify-between mb-auto">
      <div class="w-8 h-8 rounded-lg flex items-center justify-center backdrop-blur-sm" style="background:{n['color']}22;border:1px solid {n['color']}35">
        <div style="color:{n['color']}">{icon}</div>
      </div>
      <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <div class="w-7 h-7 rounded-full bg-[#00FFC6]/10 border border-[#00FFC6]/20 flex items-center justify-center">
          <svg class="w-3 h-3 text-[#00FFC6]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </div>
      </div>
    </div>
    <div>
      <div class="flex items-center gap-2 mb-1">
        <span class="text-[10px] text-[#00FFC6]/50 font-mono uppercase tracking-wider">{category}</span>
        <span class="text-white/10">|</span>
        <span class="text-[10px] text-white/30 bg-white/[0.06] backdrop-blur-sm px-1.5 py-0.5 rounded-full font-mono uppercase tracking-wider">{risk}</span>
      </div>
      <h3 class="font-semibold text-white text-sm tracking-tight mb-1 lc-2">{sys_name}</h3>
      <p class="text-[11px] text-white/30 font-mono mb-2 lc-3">{outcome[:65]}...</p>
      <p class="text-[10px] text-white/20 mb-2 leading-relaxed">Includes: {deliverables}</p>
      <div class="flex items-center justify-between pt-2.5 border-t border-white/[0.06]">
        <div class="flex items-center gap-1.5">
          <span class="text-sm font-semibold text-white/80">{cost_str}</span>
          <span class="text-[10px] text-white/25 font-mono">{cost_label}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-[11px] text-[#00FFC6]/50 font-mono">{op_count:,} deployed</span>
          <button onclick="event.stopPropagation();preview('{id}')" class="text-[11px] text-white/40 hover:text-white/70 transition-colors font-mono bg-white/[0.04] hover:bg-white/[0.08] px-1.5 py-0.5 rounded">Preview</button>
        </div>
      </div>
    </div>
  </div>
</div>"""

    # Bundle promo card
    bundle_card = """
<div class="mod group relative bg-gradient-to-br from-[#00FFC6]/[0.03] to-transparent border border-[#00FFC6]/15 hover:border-[#00FFC6]/30 rounded-2xl transition-all duration-500 cursor-pointer overflow-hidden flex flex-col sm:flex-row h-[260px] sm:h-[240px]" onclick="showBundle()">
  <div class="relative w-full sm:w-[38%] h-[150px] sm:h-auto overflow-hidden flex-shrink-0 bg-[#00FFC6]/[0.03] flex items-center justify-center">
    <img src="/images/network-bg.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.25] pointer-events-none" loading="lazy">
    <div class="absolute inset-0 pointer-events-none" style="background:linear-gradient(to right, transparent 0%, rgba(15,17,21,0.90) 100%)"></div>
    <div class="relative z-10 text-center">
      <div class="w-12 h-12 rounded-xl bg-[#00FFC6]/10 border border-[#00FFC6]/20 flex items-center justify-center mx-auto mb-2">
        <svg class="w-6 h-6 text-[#00FFC6]/70" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l8 5v10l-8 5-8-5V7l8-5z"/></svg>
      </div>
      <div class="text-[10px] text-[#00FFC6]/40 font-mono uppercase tracking-wider">Bundle Offer</div>
    </div>
  </div>
  <div class="relative flex-1 p-4 sm:p-5 flex flex-col justify-between">
    <div>
      <div class="flex items-center gap-2 mb-1">
        <span class="text-[11px] text-[#00FFC6]/50 font-mono uppercase tracking-wider">Best Value</span>
        <span class="text-white/10">|</span>
        <span class="text-[11px] text-white/25 font-mono">Save 15 credits</span>
      </div>
      <h3 class="font-semibold text-white text-[15px] tracking-tight mb-1">Growth Bundle</h3>
      <p class="text-xs text-white/35 leading-relaxed mb-2">AI Content Monetization Engine + AI Commerce Stack + AI E-Commerce Suite. Build, monetize, and scale in one deployment.</p>
      <p class="text-[11px] text-white/20 mb-1">Includes: 30 workflows, prompt libraries, setup guides, templates</p>
    </div>
    <div class="flex items-center justify-between pt-3 border-t border-white/[0.06]">
      <div class="flex items-center gap-2">
        <span class="text-sm font-bold text-white/90">45</span>
        <span class="text-xs text-white/25 font-mono">credits</span>
        <span class="text-xs text-white/20 line-through font-mono ml-1">60</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-[11px] text-[#00FFC6]/50 font-mono">928+ deployed</span>
        <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <svg class="w-4 h-4 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </div>
      </div>
    </div>
  </div>
</div>"""

    # Featured creations carousel
    carousel_html = '<div class="cr py-[120px] border-b border-white/[0.04] rv"><div class="flex items-center justify-between mb-6"><div><h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-white tracking-[-0.03em] leading-[1.15]">Featured Creations</h2><p class="text-sm text-white/25 font-mono mt-2">Most deployed intelligence systems in the network</p></div></div><div class="cr-inner">'
    for n in NICHES[:6]:
        sys_name = SYSTEM_NAMES[n["id"]]
        outcome = OUTCOMES[n["id"]]
        icon = _svg(ICONS[n["id"]], "w-4 h-4")
        carousel_html += f'<div class="cr-item" onclick="openMod(\'{n["id"]}\')"><img src="/images/{n["id"]}.png" alt="" class="cr-img" loading="lazy"><div class="cr-overlay"></div><div class="cr-content"><div class="w-7 h-7 rounded-lg flex items-center justify-center mb-2" style="background:{n["color"]}22;border:1px solid {n["color"]}35"><div style="color:{n["color"]}">{icon}</div></div><h3 class="text-sm font-semibold text-white mb-0.5">{sys_name}</h3><p class="text-[11px] text-white/40 font-mono truncate">{outcome[:50]}...</p></div></div>'
    carousel_html += '</div></div>'

    coin_html = ""
    pack_names = ["Recon Pack", "Operator Pack", "Strategic Deployment Pack", "Senior Architect Reserve"]
    pack_descs = ["Test one system. No commitment.", "Most operators begin here. 4 full deployments.", "For operators running multiple systems.", "For advanced operators. Enterprise-tier access."]
    for i, p in enumerate(COIN_PACKS):
        is_best = i == 1
        bonus = p["bonus"]
        tag = '<span class="absolute -top-2 left-1/2 -translate-x-1/2 bg-[#00FFC6]/15 text-[#00FFC6]/70 text-xs font-semibold px-2 py-0.5 rounded-full font-mono tracking-wider">MOST POPULAR</span>' if is_best else ""
        border = "border-[#00FFC6]/15 bg-[#00FFC6]/[0.02]" if is_best else "border-white/[0.06] bg-transparent"
        bonus_html = f'<span class="text-emerald-400 text-xs font-mono">+{bonus} free</span>' if bonus else ""
        coin_html += f"""
<button onclick="buy('{p['id']}')" class="relative {border} hover:border-white/[0.12] rounded-xl p-4 text-left transition-all duration-300 group hover:scale-[1.01]">
  {tag}
  <div class="flex items-center justify-between mb-1.5">
    <div>
      <span class="font-semibold text-white text-sm">{pack_names[i]}</span>
      <span class="text-white/20 text-[12px] font-mono ml-2">{p['coins']} credits</span>
    </div>
    {bonus_html}
  </div>
  <p class="text-[12px] text-white/20 font-mono mb-2">{pack_descs[i]}</p>
  <div class="flex items-center justify-between">
    <span class="text-base font-bold text-white/90">${p['price']:.2f}</span>
    <span class="text-xs text-white/20 group-hover:text-[#00FFC6]/60 transition font-mono">Purchase</span>
  </div>
</button>"""

    cases_html = ""
    case_images = ["case-ecom", "case-content", "case-crypto", "case-leads", "case-saas"]
    for i, c in enumerate(CASE_STUDIES):
        img = case_images[i] if i < len(case_images) else "case-ecom"
        cases_html += f"""
<div class="flex-shrink-0 w-[360px] bg-[#0F1115] rounded-xl border border-white/[0.06] overflow-hidden snap-start">
  <div class="h-28 relative overflow-hidden bg-[#0A0A0C]">
    <img src="/images/{img}.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-40" loading="lazy">
    <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(15,17,21,0.9) 0%, transparent 60%)"></div>
  </div>
  <div class="p-4">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-[12px] text-[#00FFC6]/40 font-mono">@{c['name']}</span>
      <span class="text-xs bg-white/[0.03] border border-white/[0.06] rounded-full px-1.5 py-0.5 text-white/20 font-mono">{c['role']}</span>
    </div>
    <div class="flex items-center gap-2 mb-2">
      <span class="text-[12px] text-white/30 font-mono">{c['system']}</span>
      <span class="text-[12px] text-[#00FFC6]/60 font-mono font-medium">{c['result']}</span>
    </div>
    <p class="text-xs text-white/30 leading-relaxed font-mono">"{c['quote']}"</p>
  </div>
</div>"""

    js = _build_js()

    preloads = "".join(f'<link rel="preload" as="image" href="/images/{n["id"]}.png">\n' for n in NICHES)
    preloads += '<link rel="preload" as="video" href="/images/hero.mp4">\n'
    preloads += '<link rel="preload" as="video" href="/images/avatar.mp4">\n'
    for n in NICHES:
        preloads += f'<link rel="preload" as="video" href="/images/{n["id"]}.mp4">\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NemoClaw — Operational Intelligence Network</title>
{preloads}
<script src="https://cdn.tailwindcss.com"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
*{{font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}
html{{scroll-behavior:smooth;background:#05070B}}
body{{background:#05070B;color:#E8E8EC;min-height:100vh;overflow-x:hidden}}
.grd{{background-image:linear-gradient(rgba(255,255,255,.004) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.004) 1px,transparent 1px);background-size:64px 64px;background-position:center center}}
.grd::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 0%,rgba(0,212,170,.025),transparent 70%)}}
.mod{{perspective:800px}}
.mod::after{{content:'';position:absolute;inset:-1px;border-radius:20px;background:linear-gradient(135deg,transparent 40%,rgba(255,255,255,.015) 50%,transparent 60%);opacity:0;transition:opacity .2s;pointer-events:none;z-index:2}}
.mod:hover::after{{opacity:1}}
.mod:hover{{box-shadow:0 0 40px rgba(0,255,198,.05),0 0 80px rgba(0,255,198,.025);transform:translateY(-6px)}}
.mod-inner{{transition:transform .15s ease-out;transform-style:preserve-3d}}
.rv{{opacity:0;transform:translateY(24px);transition:all .8s cubic-bezier(.16,1,.3,1)}}
.rv.vis{{opacity:1;transform:translateY(0)}}
@keyframes fi{{from{{opacity:0;transform:translateY(12px) scale(.98)}}to{{opacity:1;transform:translateY(0) scale(1)}}}}
.ani{{animation:fi .5s cubic-bezier(.16,1,.3,1)}}
@keyframes fl{{0%{{transform:translateY(0) scale(1);opacity:1}}100%{{transform:translateY(-80px) scale(.4);opacity:0}}}}
.fly{{position:fixed;pointer-events:none;z-index:9999;animation:fl .8s ease-out forwards}}
@keyframes pd{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
.pd{{animation:pd 2.5s ease-in-out infinite}}
@keyframes sh{{0%{{transform:translateX(-100%)}}100%{{transform:translateX(100%)}}}}
.sh{{position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.015),transparent);animation:sh 3s infinite}}
.db{{background:rgba(0,0,0,.55);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);transition:opacity .4s ease}}
.dp{{transition:transform .4s cubic-bezier(.16,1,.3,1)}}
.gl{{background:rgba(15,17,21,.85);backdrop-filter:blur(18px) saturate(1.2);-webkit-backdrop-filter:blur(18px) saturate(1.2);border-bottom:1px solid rgba(255,255,255,.04)}}
.btnp{{background:linear-gradient(135deg,#00FFC6,#00D99C);transition:all .2s cubic-bezier(.16,1,.3,1);box-shadow:0 4px 20px rgba(0,212,170,.2);color:#05070B;font-weight:600;position:relative;overflow:hidden}}
.btnp:hover{{background:linear-gradient(135deg,#00FFD6,#00FFC6);transform:scale(1.015);box-shadow:0 6px 28px rgba(0,212,170,.3)}}
.btnp:active{{transform:scale(.98);box-shadow:0 2px 12px rgba(0,212,170,.15)}}
.btnpglow{{position:relative;overflow:hidden}}
.btnpglow::before{{content:'';position:absolute;inset:-2px;border-radius:inherit;background:linear-gradient(135deg,rgba(0,212,170,.5),rgba(0,212,170,.2));z-index:-1;opacity:0;transition:opacity .3s}}
.btnpglow:hover::before{{opacity:1}}
.ripple{{position:absolute;border-radius:50%;background:rgba(255,255,255,.3);transform:scale(0);animation:rippleAnim .6s ease-out;pointer-events:none}}
@keyframes rippleAnim{{to{{transform:scale(4);opacity:0}}}}
.btns{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);color:rgba(232,232,236,.6);transition:all .2s ease;position:relative;overflow:hidden}}
.btns:hover{{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);color:rgba(232,232,236,.8)}}
.btns:active{{transform:scale(.97)}}
.op0{{opacity:0}} .op100{{opacity:1}} .pev{{pointer-events:none}} .txf{{transform:translateX(100%)}}
.stk{{background:linear-gradient(180deg,rgba(13,13,15,.95),rgba(13,13,15,.98));border-top:1px solid rgba(255,255,255,.06);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px)}}
.noise{{position:fixed;inset:0;z-index:9998;pointer-events:none;opacity:.018;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-repeat:repeat;background-size:256px 256px}}
.st0>div:nth-child(1){{transition-delay:0ms}}
.st0>div:nth-child(2){{transition-delay:80ms}}
.st0>div:nth-child(3){{transition-delay:160ms}}
.st0>div:nth-child(4){{transition-delay:240ms}}
.st0>div:nth-child(5){{transition-delay:320ms}}
.st0>div:nth-child(6){{transition-delay:400ms}}
.st0>div:nth-child(7){{transition-delay:480ms}}
.st0>div:nth-child(8){{transition-delay:560ms}}
.st0>div:nth-child(9){{transition-delay:640ms}}
.st0>div:nth-child(10){{transition-delay:720ms}}
.st0>div:nth-child(11){{transition-delay:800ms}}
.st0>div:nth-child(12){{transition-delay:880ms}}
@keyframes countUp{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.cv{{display:inline-block;animation:countUp .4s ease-out forwards}}
@keyframes tp{{0%{{transform:translateX(0) scaleX(1)}}50%{{transform:translateX(50%) scaleX(.8)}}100%{{transform:translateX(100%) scaleX(1)}}}}
.tpb{{animation:tp var(--t) linear forwards}}
@keyframes shimmer{{0%{{background-position:-200% 0}}100%{{background-position:200% 0}}}}
.shim{{background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.02) 50%,transparent 100%);background-size:200% 100%;animation:shimmer 2s infinite}}
::-webkit-scrollbar{{width:3px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:rgba(0,255,198,.15);border-radius:4px}}
::-webkit-scrollbar-thumb:hover{{background:rgba(0,255,198,.3)}}
.topology-node{{transition:all .3s ease}}
@keyframes pulse-line{{0%,100%{{opacity:.1}}50%{{opacity:.3}}}}
.topology-line{{animation:pulse-line 3s ease-in-out infinite}}
.term-cursor::after{{content:'\u258C';animation:blink 1s step-end infinite;color:rgba(0,212,170,.4)}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0}}}}
#pc{{position:absolute;inset:0;z-index:0;pointer-events:none;opacity:.35}}
@keyframes cr{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.cr{{overflow:hidden;position:relative}}
.cr-inner{{display:flex;gap:16px;animation:cr 30s linear infinite;width:max-content}}
.cr-inner:hover{{animation-play-state:paused}}
.cr-item{{flex-shrink:0;width:320px;height:200px;border-radius:12px;overflow:hidden;position:relative;cursor:pointer;border:1px solid rgba(255,255,255,.06);transition:border-color .3s}}
.cr-item:hover{{border-color:rgba(0,255,198,.25)}}
.cr-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55;transition:opacity .5s;pointer-events:none}}
.cr-item:hover .cr-img{{opacity:.8}}
.cr-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(15,17,21,.95) 0%,rgba(15,17,21,.3) 60%,transparent 100%);pointer-events:none}}
.cr-content{{position:absolute;bottom:0;left:0;right:0;padding:16px;pointer-events:none}}
@keyframes pg{{0%,100%{{opacity:1;transform:scaleX(1)}}50%{{opacity:.3;transform:scaleX(.8)}}}}
.pg{{animation:pg 2s ease-in-out infinite}}
@keyframes urg{{0%{{opacity:0;transform:translateY(4px)}}100%{{opacity:1;transform:translateY(0)}}}}
.urg{{animation:urg .3s ease-out forwards}}
.av-modal{{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.7);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);transition:opacity .4s ease}}
.av-modal.hidden{{display:none}}
.av-box{{background:rgba(15,17,21,.95);border:1px solid rgba(255,255,255,.08);border-radius:20px;overflow:hidden;max-width:480px;width:90%;box-shadow:0 24px 80px rgba(0,0,0,.5)}}
.av-vid{{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}}
.av-body{{padding:20px}}
.qo.selected{{background:rgba(0,255,198,.08)!important;border-color:rgba(0,255,198,.3)!important;color:rgba(0,255,198,.8)!important;font-weight:600}}
@keyframes shim{{0%{{background-position:-200% 0}}100%{{background-position:200% 0}}}}
.shimm{{background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.02) 50%,transparent 100%);background-size:200% 100%;animation:shim 2s infinite}}
@media(max-width:640px){{.mg{{grid-template-columns:1fr!important}}.hm{{display:none!important}}.cr-item{{width:260px;height:160px}}}}
</style>
</head>
<body>
<div class="noise"></div>

<div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-10">

  <!-- NAV -->
  <nav class="sticky top-0 z-50 backdrop-blur-xl bg-[#05070B]/80 border-b border-white/[0.04] -mx-5 sm:-mx-8 lg:-mx-10 px-5 sm:px-8 lg:px-10">
    <div class="flex items-center justify-between h-[56px] max-w-[1440px] mx-auto">
      <div class="flex items-center gap-3">
        <div class="w-7 h-7 rounded-lg bg-[#00FFC6] flex items-center justify-center text-[12px] font-black text-black">N</div>
        <span class="font-semibold text-sm text-white/80">NemoClaw</span>
        <span class="hidden sm:inline text-xs text-white/10 uppercase tracking-[.12em] font-mono">intel network</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1.5 bg-white/[0.04] border border-white/[0.06] rounded-full px-2.5 py-1 font-mono">
          <svg class="w-3 h-3 text-[#00FFC6]/70" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          <span id="bal" class="text-white/80 tabular-nums text-xs">0</span>
        </div>
        <button onclick="showShop()" class="btns px-2.5 py-1 rounded-lg text-[12px] font-medium font-mono">Credits</button>
        <div class="hidden sm:flex items-center gap-1.5 bg-white/[0.03] border border-white/[0.06] rounded-full px-2.5 py-1 font-mono">
          <span class="text-[12px] text-white/20">TIER</span>
          <span id="rank" class="text-[12px]">Recruit</span>
        </div>
      </div>
    </div>
  </nav>

  <!-- HERO -->
  <div class="relative min-h-[90vh] flex items-center py-16 sm:py-20 rv overflow-hidden">
    <video autoplay muted loop playsinline poster="/images/hero.png"
           class="absolute inset-0 w-full h-full object-cover opacity-[0.12] pointer-events-none"
           preload="metadata">
      <source src="/images/hero.mp4" type="video/mp4">
    </video>
    <div class="absolute inset-0" style="background:linear-gradient(to right, rgba(13,13,15,0.95) 0%, rgba(13,13,15,0.7) 50%, rgba(13,13,15,0.4) 100%)"></div>
    <div class="grd absolute inset-0 -mx-5 sm:-mx-8 lg:-mx-10"></div>
    <canvas id="pc"></canvas>
    <div class="relative z-10 grid lg:grid-cols-2 gap-8 lg:gap-12 items-center max-w-[1280px] mx-auto w-full">
      <div>
        <div class="inline-flex items-center gap-2 bg-white/[0.03] border border-white/[0.06] rounded-full px-3.5 py-1.5 text-xs text-white/20 font-mono tracking-wider uppercase mb-6">
          <span class="w-1.5 h-1.5 rounded-full bg-[#00FFC6] pd"></span>
          operational intelligence infrastructure
        </div>
        <h1 class="text-[42px] sm:text-[56px] lg:text-[72px] font-extrabold leading-[1.1] tracking-[-0.03em] mb-5 text-balance">
          Deploy AI systems that<br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#00FFC6] via-[#00FFD6] to-[#00D99C]">automate income, operations, and growth.</span>
        </h1>
        <p class="text-base sm:text-lg text-white/40 max-w-xl leading-[1.5] font-medium tracking-[-0.01em]">Ready-to-deploy AI workflows, automation frameworks, and operational systems used by 2,184+ operators to build scalable online businesses.</p>
        <div class="mt-8 flex flex-col sm:flex-row items-start gap-4">
          <button onclick="document.getElementById('modules').scrollIntoView({{behavior:'smooth'}})" class="btnp btnpglow px-8 py-3.5 rounded-xl text-sm">
              Browse Systems
          </button>
          <button onclick="preview(niches[0].id)" class="btns px-8 py-3.5 rounded-xl text-sm font-mono">
            Watch Demo
          </button>
        </div>
        <div class="flex items-center gap-6 mt-8 text-xs text-white/15 font-mono">
          <span class="flex items-center gap-1"><span class="text-[#00FFC6]/60 font-semibold cv" data-count="2184">0</span> deployments</span>
          <span class="w-px h-3 bg-white/[0.06]"></span>
          <span class="flex items-center gap-1"><span class="text-[#00FFC6]/60 font-semibold cv" data-count="143">0</span> active operators</span>
          <span class="w-px h-3 bg-white/[0.06]"></span>
          <span class="flex items-center gap-1"><span class="text-white/30 font-semibold cv" data-count="10">0</span> systems released</span>
        </div>
      </div>
      <div class="hidden lg:flex justify-end">
        <div class="relative bg-[#0F1115] rounded-2xl border border-white/[0.08] overflow-hidden shadow-2xl w-[420px] flex-shrink-0">
          <div class="flex items-center gap-1.5 px-4 py-2.5 border-b border-white/[0.04] bg-[#0A0A0C]">
            <div class="w-2 h-2 rounded-full bg-red-400/30"></div>
            <div class="w-2 h-2 rounded-full bg-amber-400/30"></div>
            <div class="w-2 h-2 rounded-full bg-[#00FFC6]/30"></div>
            <span class="text-xs text-white/10 font-mono ml-2">operational terminal — v3.7.1</span>
          </div>
          <div class="p-4 space-y-3 text-[12px] font-mono">
            <div class="grid grid-cols-3 gap-2 mb-3">
              <div class="bg-white/[0.02] rounded-lg p-2 border border-white/[0.04]">
                <div class="text-xs text-white/15 uppercase tracking-wider">Active</div>
                <div class="text-sm font-bold text-[#00FFC6] tabular-nums">143</div>
                <div class="text-xs text-white/10">active operators</div>
              </div>
              <div class="bg-white/[0.02] rounded-lg p-2 border border-white/[0.04]">
                <div class="text-xs text-white/15 uppercase tracking-wider">Deployed</div>
                <div class="text-sm font-bold text-white/80 tabular-nums">2,184</div>
                <div class="text-xs text-white/10">deployments</div>
              </div>
              <div class="bg-white/[0.02] rounded-lg p-2 border border-white/[0.04]">
                <div class="text-xs text-white/15 uppercase tracking-wider">Queue</div>
                <div class="text-sm font-bold text-amber-400/70 tabular-nums">3</div>
                <div class="text-xs text-white/10">deploying</div>
              </div>
            </div>
            <div class="relative w-full h-48 rounded-lg overflow-hidden bg-[#0A0A0C]">
              <img src="/images/network-bg.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-40" loading="lazy">
              <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(10,10,12,0.8) 0%, transparent 50%)"></div>
              <div class="absolute bottom-3 left-3 right-3 grid grid-cols-2 gap-2 text-xs">
                <div class="flex items-center gap-2"><span class="w-1 h-1 rounded-full bg-[#00FFC6]"></span><span class="text-white/20">system online</span></div>
                <div class="flex items-center justify-end gap-2"><span class="text-white/20">last drop</span><span class="text-white/10">3m ago</span></div>
              </div>
            </div>
            <div class="pt-2 border-t border-white/[0.04]">
              <div class="text-xs text-white/15 term-cursor">$ intelligence routing active — 10 systems available for deployment</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TRUST SIGNALS -->
  <div class="py-16 sm:py-20 border-b border-white/[0.04] rv">
    <div class="max-w-4xl mx-auto">
      <div class="flex flex-wrap items-center justify-center gap-6 sm:gap-10">
        <div class="flex items-center gap-2 text-xs text-white/20 font-mono">
          <svg class="w-4 h-4 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          Secure checkout
        </div>
        <div class="flex items-center gap-2 text-xs text-white/20 font-mono">
          <svg class="w-4 h-4 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Encrypted payments
        </div>
        <div class="flex items-center gap-2 text-xs text-white/20 font-mono">
          <svg class="w-4 h-4 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          Instant delivery
        </div>
        <div class="flex items-center gap-2 text-xs text-white/20 font-mono">
          <svg class="w-4 h-4 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Built with OpenAI + Claude
        </div>
        <div class="flex items-center gap-2 text-xs text-white/20 font-mono">
          <svg class="w-4 h-4 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          Email support
        </div>
      </div>
    </div>
  </div>

  <!-- HOW DEPLOYMENT WORKS -->
  <div class="py-[120px] border-b border-white/[0.04] rv">
    <div class="max-w-[1280px] mx-auto px-4 sm:px-6">
      <h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-white tracking-[-0.03em] mb-4 text-center leading-[1.15]">How Deployment Works</h2>
      <p class="text-base text-white/30 text-center mb-16 max-w-xl mx-auto leading-relaxed">From purchase to live system in under 90 minutes.</p>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
          <div class="w-8 h-8 rounded-lg bg-[#00FFC6]/10 flex items-center justify-center text-[#00FFC6] font-bold text-sm mb-3">1</div>
          <h3 class="text-sm font-semibold text-white mb-1">Choose a system</h3>
          <p class="text-xs text-white/30 leading-relaxed">Browse AI automation frameworks built for your business model.</p>
        </div>
        <div class="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
          <div class="w-8 h-8 rounded-lg bg-[#00FFC6]/10 flex items-center justify-center text-[#00FFC6] font-bold text-sm mb-3">2</div>
          <h3 class="text-sm font-semibold text-white mb-1">Deploy infrastructure</h3>
          <p class="text-xs text-white/30 leading-relaxed">Receive templates, workflows, prompts, and setup documentation instantly.</p>
        </div>
        <div class="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
          <div class="w-8 h-8 rounded-lg bg-[#00FFC6]/10 flex items-center justify-center text-[#00FFC6] font-bold text-sm mb-3">3</div>
          <h3 class="text-sm font-semibold text-white mb-1">Launch automation</h3>
          <p class="text-xs text-white/30 leading-relaxed">Connect APIs, configure workflows, and activate your system.</p>
        </div>
        <div class="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
          <div class="w-8 h-8 rounded-lg bg-[#00FFC6]/10 flex items-center justify-center text-[#00FFC6] font-bold text-sm mb-3">4</div>
          <h3 class="text-sm font-semibold text-white mb-1">Scale operations</h3>
          <p class="text-xs text-white/30 leading-relaxed">Monitor performance, optimize workflows, and grow revenue on autopilot.</p>
        </div>
      </div>
    </div>
  </div>

  {carousel_html}

  <!-- LIVE FEED -->
  <div class="fixed bottom-24 left-4 z-[90] max-w-xs hidden sm:block">
    <div class="text-xs text-white/8 font-mono mb-1 uppercase tracking-wider">live feed</div>
    <div id="feed" class="space-y-1"></div>
  </div>

  <!-- MODULES -->
  <div class="relative py-[120px] rv overflow-hidden" id="modules">
    <img src="/images/deployment-bg.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.03] pointer-events-none" loading="lazy">
    <div class="relative z-10">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-white tracking-[-0.03em] leading-[1.15]">Intelligence Systems</h2>
        <p class="text-sm text-white/25 font-mono mt-2">Deployable operational frameworks — verified by 2,184+ operators</p>
      </div>
      <div class="flex items-center gap-2">
        <input id="modSearch" type="text" placeholder="Search systems..." oninput="filterMods()" class="bg-white/[0.04] border border-white/[0.06] rounded-xl px-4 py-2.5 text-sm text-white/60 placeholder-white/15 font-mono outline-none focus:border-[#00FFC6]/40 transition-colors w-44 sm:w-56">
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-2 mb-6">
      <button onclick="filterCategory('all')" class="cf bg-[#00FFC6]/15 text-[#00FFC6] border border-[#00FFC6]/25 rounded-full px-3 py-1 text-xs font-mono transition-all" data-cat="all">All Systems</button>
      <button onclick="filterCategory('automation')" class="cf bg-white/[0.04] text-white/40 border border-white/[0.06] rounded-full px-3 py-1 text-xs font-mono transition-all" data-cat="automation">Automation</button>
      <button onclick="filterCategory('growth')" class="cf bg-white/[0.04] text-white/40 border border-white/[0.06] rounded-full px-3 py-1 text-xs font-mono transition-all" data-cat="growth">Growth</button>
      <button onclick="filterCategory('monetization')" class="cf bg-white/[0.04] text-white/40 border border-white/[0.06] rounded-full px-3 py-1 text-xs font-mono transition-all" data-cat="monetization">Monetization</button>
      <button onclick="filterCategory('lifestyle')" class="cf bg-white/[0.04] text-white/40 border border-white/[0.06] rounded-full px-3 py-1 text-xs font-mono transition-all" data-cat="lifestyle">Lifestyle</button>
      <button onclick="filterCategory('free')" class="cf bg-white/[0.04] text-white/40 border border-white/[0.06] rounded-full px-3 py-1 text-xs font-mono transition-all" data-cat="free">Free</button>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 st0" id="modGrid">
      {bundle_card}
      {mod_html}
    </div>
  </div>

  <!-- TIER PROGRESSION -->
  <div class="py-[120px] border-t border-white/[0.04] rv overflow-hidden relative">
    <img src="/images/clearance-bg.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.04] pointer-events-none" loading="lazy">
    <div class="relative z-10 max-w-[1280px] mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-white tracking-[-0.03em] leading-[1.15]">Operator Progression</h2>
          <p class="text-sm text-white/25 font-mono mt-2">Deploy systems to advance your operational rank</p>
        </div>
        <div class="text-right">
          <div class="text-xs text-white/12 font-mono uppercase tracking-wider">Current Tier</div>
          <div id="rank2" class="text-base font-bold text-white/80">Recruit</div>
        </div>
      </div>
      <div class="flex items-center justify-center mb-8">
        <div class="flex items-center gap-6 sm:gap-8 text-[12px] font-mono">
          <div class="flex flex-col items-center gap-1"><img src="/images/rank-recruit.png" alt="" class="w-16 h-16 rounded-full object-cover opacity-60 mb-1"><span class="text-white/20 text-[11px]">Recruit</span></div>
          <span class="text-white/10 text-lg">&rarr;</span>
          <div class="flex flex-col items-center gap-1"><img src="/images/rank-analyst.png" alt="" class="w-16 h-16 rounded-full object-cover opacity-60 mb-1"><span class="text-white/20 text-[11px]">Analyst</span></div>
          <span class="text-white/10 text-lg">&rarr;</span>
          <div class="flex flex-col items-center gap-1"><img src="/images/rank-operator.png" alt="" class="w-16 h-16 rounded-full object-cover opacity-60 mb-1"><span class="text-white/20 text-[11px]">Operator</span></div>
          <span class="text-white/10 text-lg">&rarr;</span>
          <div class="flex flex-col items-center gap-1"><img src="/images/rank-strategist.png" alt="" class="w-16 h-16 rounded-full object-cover opacity-60 mb-1"><span class="text-white/20 text-[11px]">Strategist</span></div>
          <span class="text-white/10 text-lg">&rarr;</span>
          <div class="flex flex-col items-center gap-1"><img src="/images/rank-architect.png" alt="" class="w-16 h-16 rounded-full object-cover opacity-60 mb-1"><span class="text-white/20 text-[11px]">Senior Architect</span></div>
          <span class="text-white/10 text-lg">&rarr;</span>
          <div class="flex flex-col items-center gap-1"><img src="/images/rank-phantom.png" alt="" class="w-16 h-16 rounded-full object-cover opacity-80 ring-1 ring-[#00FFC6]/20 mb-1"><span class="text-[#00FFC6]/60 text-[11px]">Senior Architect</span></div>
        </div>
        <span class="text-[12px] text-white/15 font-mono" id="progLabel">0 / 10 systems</span>
      </div>
      <div class="w-full h-1.5 rounded-full bg-white/[0.04] overflow-hidden">
        <div class="h-full rounded-full bg-gradient-to-r from-[#00FFC6] to-[#00D99C] transition-all duration-700" id="rankBar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <!-- DEPLOYED RESULTS -->
  <div class="relative py-[120px] border-t border-white/[0.04] rv overflow-hidden">
    <img src="/images/network-bg.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.03] pointer-events-none" loading="lazy">
    <div class="relative z-10">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-white tracking-[-0.03em] leading-[1.15]">Verified Deployments</h2>
        <p class="text-sm text-white/25 font-mono mt-2">Operator-submitted results from the network</p>
      </div>
    </div>
    <div class="flex items-start gap-4 overflow-x-auto pb-4 snap-x snap-mandatory" style="-webkit-overflow-scrolling:touch;scrollbar-width:none">
      {cases_html}
    </div>
  </div>

  <!-- PHANTOM TIER -->
  <div class="relative py-[120px] border-t border-white/[0.04] rv overflow-hidden" id="pro">
    <img src="/images/phantom.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.06] pointer-events-none" loading="lazy">
    <div class="absolute inset-0" style="background:linear-gradient(to bottom, rgba(13,13,15,0.6) 0%, rgba(13,13,15,0.9) 100%)"></div>
    <div class="relative z-10 max-w-[640px] mx-auto text-center px-4 sm:px-6">
      <div class="inline-flex items-center gap-2 bg-white/[0.02] border border-white/[0.06] rounded-full px-3.5 py-1.5 text-xs text-white/20 font-mono tracking-wider uppercase mb-4">
        <span class="w-1.5 h-1.5 rounded-full bg-[#00FFC6]/40 pd"></span>
        advanced operational layer
      </div>
      <h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-extrabold text-white tracking-[-0.03em] mb-3 leading-[1.15]">Strategic Access</h2>
      <p class="text-xs text-white/25 mb-4 max-w-sm mx-auto font-mono">This intelligence layer is not publicly listed. Access requires operator track record verification.</p>
      <div class="bg-white/[0.02] rounded-xl border border-white/[0.06] p-4 mb-5 text-left">
        <div class="text-xs text-white/15 font-mono uppercase tracking-wider mb-3">Strategic tier includes</div>
        <div class="grid grid-cols-2 gap-2 text-[12px] font-mono">
          <div class="flex items-center gap-2 text-white/25"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Hidden intelligence archive</div>
          <div class="flex items-center gap-2 text-white/25"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Daily intelligence drops</div>
          <div class="flex items-center gap-2 text-white/25"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Private operator frameworks</div>
          <div class="flex items-center gap-2 text-white/25"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Black archive access</div>
          <div class="flex items-center gap-2 text-white/25"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Early-access systems</div>
          <div class="flex items-center gap-2 text-white/25"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Operator-only dashboards</div>
        </div>
      </div>
      <button onclick="showSub()" class="btnp btnpglow px-10 py-3.5 rounded-xl text-sm w-full sm:w-auto">
        Request Strategic Access
      </button>
      <p class="text-xs text-white/8 mt-2 font-mono">Requires Strategist tier eligibility. Application review: 24-48 hours.</p>
    </div>
  </div>

  <!-- CTA -->
  <div class="py-[120px] border-t border-white/[0.04] text-center rv px-4 sm:px-6">
    <h2 class="text-[32px] sm:text-[40px] lg:text-[48px] font-bold text-white tracking-[-0.03em] mb-3 leading-[1.15]">Ready to Deploy?</h2>
    <p class="text-xs text-white/25 mb-6 font-mono">12,400+ operators already deployed intelligence systems</p>
    <button onclick="document.getElementById('modules').scrollIntoView({{behavior:'smooth'}})" class="btnp btnpglow px-10 py-4 rounded-xl text-sm">
      Access Intelligence Systems
    </button>
  </div>

  <footer class="relative py-16 text-center text-xs text-white/10 border-t border-white/[0.04] font-mono overflow-hidden">
    <img src="/images/footer-bg.png" alt="" class="absolute inset-0 w-full h-full object-cover opacity-[0.03] pointer-events-none" loading="lazy">
    <div class="relative z-10 max-w-2xl mx-auto">
      <div class="flex flex-wrap items-center justify-center gap-4 mb-4 text-white/15">
        <span class="hover:text-white/30 cursor-pointer transition-colors">Terms of Service</span>
        <span class="text-white/5">|</span>
        <span class="hover:text-white/30 cursor-pointer transition-colors">Privacy Policy</span>
        <span class="text-white/5">|</span>
        <span class="hover:text-white/30 cursor-pointer transition-colors">Refund Policy</span>
        <span class="text-white/5">|</span>
        <button onclick="wa()" class="hover:text-white/30 transition-colors">Contact Support</button>
      </div>
      <div class="flex items-center justify-center gap-3 mb-4 text-white/10">
        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        Secure payments &middot; Instant delivery &middot; 30-day refund guarantee
      </div>
      <p class="text-white/8">NemoClaw &copy; {today}. All systems are digital products. Results vary by implementation.</p>
      <button onclick="toggleAdmin()" class="mt-3 text-white/3 hover:text-white/8 transition-colors">&#9670;</button>
    </div>
  </footer>
</div>

<!-- MOBILE STICKY CTA -->
<div class="fixed bottom-0 left-0 right-0 z-40 sm:hidden">
  <div class="stk px-5 py-3">
    <button onclick="document.getElementById('modules').scrollIntoView({{behavior:'smooth'}})" class="btnp btnpglow w-full py-3.5 rounded-xl text-sm">
      Browse Systems
    </button>
  </div>
</div>



<!-- DRAWER -->
<div id="dr" class="fixed inset-0 z-[100] hidden">
  <div id="drb" class="db absolute inset-0 op0 pev" onclick="closeDr()"></div>
  <div id="drp" class="dp absolute right-0 top-0 bottom-0 w-full max-w-[720px] bg-[#0F1115] border-l border-white/[0.08] shadow-2xl txf">
    <div class="flex items-center justify-between px-6 h-[52px] border-b border-white/[0.06]">
      <span class="text-sm font-semibold text-white/70">Intelligence System</span>
      <button onclick="closeDr()" class="w-7 h-7 rounded-full bg-white/[0.04] hover:bg-white/[0.08] flex items-center justify-center text-white/30 hover:text-white/60 transition-all text-sm">&times;</button>
    </div>

    <!-- Module Detail -->
    <div id="drMod" class="drc hidden overflow-y-auto" style="height:calc(100% - 52px);max-height:90vh">
      <div class="h-48 flex items-center justify-center bg-[#0A0A0C] border-b border-white/[0.06] relative overflow-hidden">
        <div class="absolute inset-0 opacity-[0.08]" style="background:radial-gradient(circle at 50% 50%, #00FFC6, transparent 70%)"></div>
        <img id="dmBg" class="absolute inset-0 w-full h-full object-cover opacity-60" src="" alt="">
        <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(15,17,21,0.95) 0%, rgba(15,17,21,0.3) 60%, transparent 100%)"></div>
        <div id="dmIcon" class="text-white/40 relative z-10">{_svg("", "w-10 h-10")}</div>
      </div>
      <div class="p-5">
        <div class="text-xs text-[#00FFC6]/40 font-mono uppercase tracking-wider mb-2" id="dmSys">SYSTEM</div>
        <h3 class="text-base font-bold text-white mb-0.5" id="dmTitle">System</h3>
        <p class="text-[12px] text-white/20 font-mono mb-2" id="dmOps">0 deployments</p>
        <p class="text-xs text-[#00FFC6]/60 mt-1 font-mono" id="dmOut">Outcome</p>
        <p class="text-xs text-white/35 mt-3 mb-4 leading-relaxed" id="dmDesc">Description</p>
        <div class="bg-white/[0.03] rounded-xl border border-white/[0.06] p-3 mb-4">
          <div class="text-xs text-white/15 uppercase tracking-wider mb-2 font-mono">System Requirements</div>
          <div class="flex items-center gap-2 text-xs text-white/30 font-mono mb-1">
            <span>Difficulty</span>
            <span id="dmDiff">
              <div class="flex gap-1">
                {"".join(f'<div class="w-2 h-2 rounded-full bg-white/[0.06]"></div>' for _ in range(10))}
              </div>
            </span>
          </div>
          <div class="text-xs text-white/25 font-mono space-y-1 mt-2">
            <div class="flex items-center gap-2"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Deployment guide & configuration</div>
            <div class="flex items-center gap-2"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Workflow templates (8-12 files)</div>
            <div class="flex items-center gap-2"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> AI prompt libraries & automation</div>
            <div class="flex items-center gap-2"><svg class="w-2.5 h-2.5 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Monetization architecture docs</div>
          </div>
        </div>
        <div class="bg-white/[0.03] rounded-xl border border-white/[0.06] p-3 mb-4 flex items-center justify-between">
          <span class="text-[12px] text-white/20 font-mono">Deployment Cost</span>
          <span id="dmPrice"><span class="text-white/30 line-through text-xs font-mono">$35</span> <span class="text-white font-semibold text-sm" id="dmCost">15 credits</span></span>
        </div>
        <button id="dmBtn" onclick="dl()" class="btnp btnpglow w-full px-6 py-3.5 rounded-xl font-semibold text-sm">
          Deploy System
        </button>
        <div class="mt-4 pt-4 border-t border-white/[0.06]">
          <div class="text-xs text-white/15 uppercase tracking-wider mb-2 font-mono">Operators also deployed</div>
          <div id="dmRelated" class="space-y-2"></div>
        </div>
      </div>
    </div>

    <!-- Preview -->
    <div id="drPrev" class="drc hidden overflow-y-auto" style="height:calc(100% - 52px);max-height:90vh">
        <div class="h-40 flex items-center justify-center bg-[#0F1115] border-b border-white/[0.06] relative overflow-hidden">
          <div class="absolute inset-0 opacity-[0.03]" style="background:radial-gradient(circle at 50% 50%, #00FFC6, transparent 70%)"></div>
          <img id="dpImg" class="absolute inset-0 w-full h-full object-cover op0 transition-opacity duration-500" src="" alt="Preview" onload="this.classList.remove('op0')" onerror="this.style.display='none'">
          <div class="text-center relative z-10">
            <div id="dpIcon" class="text-white/30 mb-1">{_svg("", "w-12 h-12")}</div>
            <h3 class="text-white font-bold text-sm" id="dpTitle">System</h3>
            <p class="text-white/25 text-[12px] mt-0.5 font-mono" id="dpSub">SYSTEM</p>
            <p class="text-[#00FFC6]/50 text-xs mt-0.5 font-mono" id="dpOut">Outcome</p>
          </div>
        </div>
      <div class="p-5">
        <div class="text-[12px] text-white/20 mb-3 font-mono">Preview — Full deployment system unlocked on purchase</div>
        <div class="bg-white/[0.02] rounded-xl border border-white/[0.06] p-3 mb-4">
          <div class="text-xs text-white/12 uppercase tracking-wider mb-2 font-mono">System Contents</div>
          <div class="text-xs text-white/25 space-y-1.5 font-mono">
            <div class="flex items-center gap-2"><svg class="w-2 h-2 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Framework documentation</div>
            <div class="flex items-center gap-2"><svg class="w-2 h-2 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Implementation examples</div>
            <div class="flex items-center gap-2"><svg class="w-2 h-2 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> AI automation workflows</div>
            <div class="flex items-center gap-2"><svg class="w-2 h-2 text-[#00FFC6]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Configuration templates</div>
          </div>
        </div>
        <button onclick="closeDr(); setTimeout(function(){{ if(selected) openMod(selected.id); }}, 300)" class="btnp btnpglow w-full px-6 py-3 rounded-xl font-semibold text-sm">
          Deploy System
        </button>
        <button onclick="closeDr()" class="text-white/20 hover:text-white/40 text-xs w-full mt-2 transition font-mono">Cancel</button>
      </div>
    </div>

    <!-- Deployment Questions -->
    <div id="drQuestions" class="drc hidden overflow-y-auto" style="height:calc(100% - 52px);max-height:90vh">
      <div class="h-40 flex items-center justify-center bg-[#0A0A0C] border-b border-white/[0.06] relative overflow-hidden">
        <div class="absolute inset-0 opacity-[0.06]" style="background:radial-gradient(circle at 50% 50%, #00FFC6, transparent 70%)"></div>
        <div class="text-center relative z-10">
          <div class="w-10 h-10 rounded-xl bg-[#00FFC6]/10 border border-[#00FFC6]/20 flex items-center justify-center mx-auto mb-2">
            <svg class="w-5 h-5 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          </div>
          <h3 class="text-white font-bold text-sm">Deployment Calibration</h3>
          <p class="text-white/30 text-[11px] mt-0.5 font-mono" id="dqSysName">Tailor this system to your operations</p>
        </div>
      </div>
      <div class="p-6">
        <div class="space-y-6">
          <div>
            <label class="text-xs text-white/40 font-mono uppercase tracking-wider mb-2 block">Experience Level</label>
            <div class="grid grid-cols-3 gap-2">
              <button onclick="selectQ('exp','beginner',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">Beginner</button>
              <button onclick="selectQ('exp','intermediate',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">Intermediate</button>
              <button onclick="selectQ('exp','advanced',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">Advanced</button>
            </div>
          </div>
          <div>
            <label class="text-xs text-white/40 font-mono uppercase tracking-wider mb-2 block">Primary Goal</label>
            <div class="grid grid-cols-3 gap-2">
              <button onclick="selectQ('goal','revenue',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">Revenue</button>
              <button onclick="selectQ('goal','automation',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">Automation</button>
              <button onclick="selectQ('goal','learning',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">Learn</button>
            </div>
          </div>
          <div>
            <label class="text-xs text-white/40 font-mono uppercase tracking-wider mb-2 block">Time Available Daily</label>
            <div class="grid grid-cols-3 gap-2">
              <button onclick="selectQ('time','30min',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">30 min</button>
              <button onclick="selectQ('time','1hr',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">1 hour</button>
              <button onclick="selectQ('time','2hr',this)" class="qo bg-white/[0.04] border border-white/[0.06] rounded-lg p-2.5 text-center text-xs text-white/40 hover:border-[#00FFC6]/25 hover:text-white/70 transition-all font-mono">2+ hours</button>
            </div>
          </div>
        </div>
        <div class="mt-6 pt-4 border-t border-white/[0.06]">
          <button id="dqDeploy" onclick="startTailoredDeploy()" disabled class="btnp btnpglow w-full px-6 py-3.5 rounded-xl font-semibold text-sm opacity-50 cursor-not-allowed">
            Calibrate &amp; Deploy
          </button>
          <button onclick="closeDr()" class="text-white/20 hover:text-white/40 text-xs w-full mt-2 transition font-mono">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Shop -->
    <div id="drShop" class="drc hidden overflow-y-auto" style="height:calc(100% - 52px);max-height:90vh">
      <div class="p-5">
        <div class="text-center mb-5">
          <div class="w-11 h-11 rounded-xl bg-[#00FFC6]/10 border border-[#00FFC6]/20 flex items-center justify-center mx-auto mb-3">
            <svg class="w-5 h-5 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          </div>
          <h2 class="text-base font-bold text-white tracking-tight">Intel Credits</h2>
          <p class="text-[12px] text-white/20 font-mono mt-1">Purchase credits to deploy systems. Never expire.</p>
        </div>
        <div class="grid grid-cols-1 gap-2">{coin_html}</div>
        <button onclick="closeDr()" class="text-white/15 hover:text-white/30 text-[12px] w-full mt-4 transition font-mono">Back to vault</button>
      </div>
    </div>

    <!-- Buy -->
    <div id="drBuy" class="drc hidden overflow-y-auto" style="height:calc(100% - 52px);max-height:90vh">
      <div class="p-6 text-center">
        <div class="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4" style="background:rgba(0,212,170,.1);border:1px solid rgba(0,212,170,.2)">
          <svg class="w-6 h-6 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        </div>
        <h3 class="text-base font-bold text-white mb-1">Complete Purchase</h3>
        <p class="text-[12px] text-white/25 mb-4 font-mono">Credits added instantly to your vault.</p>
        <div class="bg-white/[0.03] rounded-xl border border-white/[0.06] p-3 mb-4 text-left">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[12px] text-white/20 font-mono">Package</span>
            <span class="text-white font-semibold text-xs" id="bpName">Recon Pack</span>
          </div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-[12px] text-white/20 font-mono">Credits</span>
            <span class="text-white/80 text-[12px] font-mono" id="bpCoins">15</span>
          </div>
          <div class="flex items-center justify-between pt-2 border-t border-white/[0.06]">
            <span class="text-[12px] text-white/20 font-mono">Total</span>
            <span class="text-white font-bold text-sm" id="bpPrice">$9.00</span>
          </div>
        </div>
        <button onclick="confirmBuy()" class="btnp btnpglow w-full px-6 py-3.5 rounded-xl font-semibold text-sm mb-2">
          Purchase Credits
        </button>
        <p class="text-xs text-white/10 font-mono" id="bpNote">Processing via Stripe checkout &middot; Credits deposited on confirmation</p>
      </div>
    </div>

    <!-- Subscribe Clearance -->
    <div id="drSub" class="drc hidden overflow-y-auto" style="height:calc(100% - 52px);max-height:90vh">
      <div class="p-6 text-center">
        <div class="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4" style="background:rgba(0,212,170,.1);border:1px solid rgba(0,212,170,.2)">
          <svg class="w-6 h-6 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        </div>
        <h3 class="text-base font-bold text-white mb-1">Strategic Access</h3>
        <p class="text-[12px] text-white/25 mb-1 font-mono">$199/month &middot; Application required</p>
        <p class="text-[12px] text-white/15 mb-4 font-mono">Advanced tier: private frameworks, strategic modules, daily intelligence briefings, dedicated support.</p>
        <button onclick="subPro()" class="btnp btnpglow w-full px-6 py-3.5 rounded-xl font-semibold text-sm mb-2">
          Request Strategic Access
        </button>
        <p class="text-xs text-white/10 font-mono">Application review: 24-48 hours. Strategist rank suggested.</p>
        <button onclick="closeDr()" class="text-white/15 hover:text-white/30 text-[12px] mt-2 transition font-mono">Start with a free system</button>
      </div>
    </div>

    <!-- Lead Capture Modal (exit intent) -->
    <div id="lcModal" class="fixed inset-0 z-[9999] flex items-center justify-center hidden" style="background:rgba(0,0,0,0.6);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)" onclick="if(event.target===this)closeLC()">
      <div class="bg-[#0F1115] border border-white/[0.08] rounded-2xl p-8 max-w-[480px] w-[92%] shadow-2xl text-center ani">
        <div class="w-10 h-10 rounded-full bg-[#00FFC6]/10 border border-[#00FFC6]/20 flex items-center justify-center mx-auto mb-3">
          <svg class="w-5 h-5 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        </div>
        <h3 class="text-sm font-bold text-white mb-1">Get 5 Free Credits</h3>
        <p class="text-xs text-white/30 font-mono mb-4">Enter your email to unlock a free deployment packet + bonus credits.</p>
        <div class="flex gap-2">
          <input id="lcEmail" type="email" placeholder="your@email.com" class="flex-1 bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-3 text-xs text-white placeholder-white/15 outline-none focus:border-[#00FFC6]/40 transition-colors font-mono">
          <button onclick="capLC()" class="btnp px-5 py-3 rounded-xl font-semibold text-xs whitespace-nowrap">Claim</button>
        </div>
        <p class="text-xs text-red-400/30 font-mono mt-2 min-h-[16px]" id="lcErr"></p>
        <button onclick="closeLC()" class="text-xs text-white/15 hover:text-white/30 mt-2 transition font-mono">No thanks</button>
      </div>
    </div>
  </div>
</div>

<!-- TOAST -->
<div id="toast" class="fixed top-4 right-4 z-[150] hidden ani" style="max-width:320px">
  <div class="gl bg-[#0F1115]/90 border border-white/[0.08] rounded-xl p-3.5 shadow-2xl shadow-black/40 overflow-hidden">
    <div class="flex items-start gap-2.5">
      <div class="w-5 h-5 rounded-full bg-[#00FFC6]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
        <svg class="w-3 h-3 text-[#00FFC6]/60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <div class="min-w-0 flex-1">
        <h3 class="text-xs font-semibold text-white/80 mb-0.5" id="toT">System Deployed</h3>
        <p class="text-xs text-white/30 leading-relaxed font-mono" id="toM">Operational.</p>
      </div>
      <button onclick="closeToast()" class="flex-shrink-0 w-4 h-4 rounded-full bg-white/[0.04] hover:bg-white/[0.08] flex items-center justify-center text-white/30 hover:text-white/60 text-xs transition-all">&times;</button>
    </div>
    <div class="absolute bottom-0 left-0 right-0 h-[2px] bg-white/[0.04]">
      <div id="tpb" class="h-full bg-[#00FFC6]/40 rounded-full" style="width:0%"></div>
    </div>
  </div>
</div>

<!-- AVATAR GREETING -->
<div id="avModal" class="av-modal hidden" onclick="if(event.target===this)closeAv()">
  <div class="av-box">
    <video id="avVid" autoplay muted loop playsinline poster="/images/avatar.png" class="av-vid">
      <source src="/images/avatar.mp4" type="video/mp4">
    </video>
    <div class="av-body text-center">
      <div class="w-10 h-10 rounded-full bg-[#00FFC6]/10 border border-[#00FFC6]/20 flex items-center justify-center mx-auto mb-3">
        <svg class="w-5 h-5 text-[#00FFC6]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      </div>
      <h3 class="text-base font-bold text-white mb-1" id="avTitle">Welcome, Operator</h3>
      <p class="text-xs text-white/30 font-mono mb-4 leading-relaxed" id="avDesc">I have 10 intelligence systems ready for deployment. Browse the collection and deploy what fits your operations.</p>
      <button onclick="closeAv();document.getElementById('modules').scrollIntoView({{behavior:'smooth'}})" class="btnp btnpglow w-full px-6 py-3 rounded-xl font-semibold text-sm mb-2" id="avBtn">
        Browse Systems
      </button>
      <button onclick="closeAv()" class="text-xs text-white/25 hover:text-white/50 transition font-mono">Browse first</button>
    </div>
  </div>
</div>

<!-- ADMIN -->
<div id="adminP" class="fixed bottom-4 right-4 z-50 hidden">
  <div class="bg-[#0F1115] border border-white/[0.08] rounded-xl p-4 shadow-2xl shadow-black/40 max-w-xs text-xs font-mono" style="max-height:70vh;overflow-y:auto">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs font-semibold text-white/50">Admin Terminal</span>
      <button onclick="document.getElementById('adminP').classList.add('hidden')" class="w-4 h-4 rounded-full bg-white/[0.04] hover:bg-white/[0.08] flex items-center justify-center text-white/30 hover:text-white/60 text-xs transition-all">&times;</button>
    </div>
    <div class="space-y-1 text-white/30">
      <div class="flex justify-between"><span>Intel Credits</span><span class="text-white/70" id="adCoins">0</span></div>
      <div class="flex justify-between"><span>XP</span><span class="text-white/70" id="adXp">0</span></div>
      <div class="flex justify-between"><span>Rank</span><span class="text-white/70" id="adRank">Recruit</span></div>
      <div class="flex justify-between"><span>Streak</span><span class="text-amber-400/60" id="adStk">0</span></div>
      <div class="flex justify-between"><span>Systems</span><span class="text-white/70" id="adDl">0</span></div>
    </div>
    <div class="mt-2 pt-2 border-t border-white/[0.06]">
      <div class="text-xs text-white/10 mb-1">Deployed Systems</div>
      <div class="text-xs text-white/20" id="adList">None</div>
    </div>
    <button onclick="resetState()" class="text-xs text-red-400/30 hover:text-red-400/50 mt-2 transition-colors">Reset Operator Data</button>
  </div>
</div>

<script>
{js}

var activeCat='all';
function filterMods(){{
  var q=document.getElementById('modSearch').value.toLowerCase();
  document.querySelectorAll('.mod').forEach(function(c){{
    var t=c.querySelector('h3').textContent.toLowerCase();
    var catMatch=activeCat==='all'||c.dataset.category===activeCat;
    var searchMatch=t.includes(q);
    c.style.display=(catMatch&&searchMatch)?'':'none'
  }})
}}
window._origFilterCategory=window.filterCategory;
window.filterCategory=function(cat){{activeCat=cat;window._origFilterCategory(cat);filterMods()}}
</script>
</body>
</html>"""


def build_admin_page() -> str:
    today = datetime.now().strftime("%B %d, %Y %H:%M")
    opts = "".join(
        f'<option value="{n["id"]}">{SYSTEM_NAMES[n["id"]]} ({n["pdf_cost"]} cr)</option>\n'
        for n in NICHES
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NemoClaw — Admin Panel</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
*{{font-family:'Inter',system-ui,sans-serif}}
body{{background:#05070B;color:#E8E8EC}}
.mono{{font-family:'JetBrains Mono',monospace!important}}
.card{{background:rgba(15,17,21,1);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:16px}}
.sv{{font-size:24px;font-weight:700;color:#00FFC6;font-family:'JetBrains Mono',monospace}}
.sl{{font-size:10px;color:rgba(255,255,255,.25);font-family:'JetBrains Mono',monospace;margin-top:2px}}
.bb{{background:rgba(255,255,255,.04);border-radius:4px;height:6px;overflow:hidden}}
.bf{{height:100%;border-radius:4px;background:linear-gradient(90deg,#00FFC6,#00D99C);transition:width .6s ease}}
.tb{{font-size:9px;color:rgba(255,255,255,.2);text-transform:uppercase;letter-spacing:.1em;padding-bottom:6px;font-family:'JetBrains Mono',monospace}}
.tr{{font-size:10px;color:rgba(255,255,255,.4);padding:4px 0;border-bottom:1px solid rgba(255,255,255,.03);font-family:'JetBrains Mono',monospace}}
.tr:last-child{{border-bottom:none}}
::-webkit-scrollbar{{width:2px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.06);border-radius:4px}}
</style>
</head>
<body class="p-4 sm:p-6 max-w-5xl mx-auto">
  <div class="flex items-center justify-between mb-6">
    <div>
      <div class="flex items-center gap-2 mb-1">
        <div class="w-6 h-6 rounded-lg bg-[#00FFC6] flex items-center justify-center text-[12px] font-black text-black">N</div>
        <h1 class="text-sm font-bold text-white/80">Admin Terminal</h1>
      </div>
      <p class="text-xs text-white/20 mono">{today}</p>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-[12px] text-white/15 mono" id="sLive">connected</span>
      <a href="/" class="text-xs text-white/25 hover:text-white/50 transition-colors mono">&larr; Vault</a>
    </div>
  </div>

  <!-- Stat Cards -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6" id="stats">
    <div class="card"><div class="sv" id="sTotal">-</div><div class="sl">PDFs Generated</div></div>
    <div class="card"><div class="sv" id="sUptime">-</div><div class="sl">Uptime</div></div>
    <div class="card"><div class="sv" id="sOk">-</div><div class="sl">Successful</div></div>
    <div class="card"><div class="sv" id="sErr">-</div><div class="sl">Errors</div></div>
  </div>
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
    <div class="card"><div class="sv" id="sEmails">-</div><div class="sl">Emails Captured</div></div>
    <div class="card"><div class="sv" id="sAvgSize">-</div><div class="sl">Avg PDF Size</div></div>
    <div class="card"><div class="sv" id="sStripe">-</div><div class="sl">Stripe</div></div>
    <div class="card"><div class="sv" id="sSmtp">-</div><div class="sl">SMTP</div></div>
  </div>

  <div class="grid sm:grid-cols-2 gap-4 mb-6">
    <div class="card">
      <div class="text-[12px] font-semibold text-white/60 mb-3">By Niche</div>
      <div id="nb" class="space-y-2"><div class="text-[12px] text-white/20 mono">Loading...</div></div>
    </div>
    <div class="card">
      <div class="flex items-center justify-between mb-3">
        <div class="text-[12px] font-semibold text-white/60">Recent Requests</div>
        <span class="text-xs text-white/10 mono" id="sReqCount">0</span>
      </div>
      <div class="tb" style="display:grid;grid-template-columns:1fr 1fr 1fr 60px"><span>Time</span><span>Niche</span><span>IP</span><span>Status</span></div>
      <div id="rr" class="max-h-64 overflow-y-auto"><div class="text-[12px] text-white/20 mono">Loading...</div></div>
    </div>
  </div>

  <!-- Manual PDF Generator -->
  <div class="card mb-6">
    <div class="text-[12px] font-semibold text-white/60 mb-3">Manual PDF Generation</div>
    <div class="flex gap-2 items-start sm:items-center flex-col sm:flex-row">
      <select id="mn" class="bg-white/[0.04] border border-white/[0.08] rounded-lg px-3 py-2 text-xs text-white/70 mono outline-none focus:border-[#00FFC6]/40 transition-colors w-full sm:w-auto">
        {opts}
      </select>
      <button onclick="genPDF()" class="bg-[#00FFC6]/15 hover:bg-[#00FFC6]/25 text-[#00FFC6] text-[12px] font-semibold px-4 py-2 rounded-lg transition-colors mono">Generate</button>
      <span id="ms" class="text-xs text-white/20 mono"></span>
    </div>
  </div>

  <footer class="text-center text-xs text-white/10 mono border-t border-white/[0.04] pt-4 mt-4">
    NemoClaw Admin &middot; <a href="/" class="text-white/15 hover:text-white/30">Vault</a>
  </footer>

<script>
var pi = null;
function fmtBytes(b) {{
  if (!b) return '0 B';
  var u = ['B','KB','MB','GB']; var i = 0;
  while (b >= 1024 && i < 3) {{ b /= 1024; i++; }}
  return b.toFixed(1) + ' ' + u[i];
}}
function load() {{
  fetch('/admin-api/stats').then(function(r){{return r.json()}}).then(function(d) {{
    document.getElementById('sTotal').textContent = d.total || 0;
    document.getElementById('sUptime').textContent = d.uptime || '-';
    document.getElementById('sOk').textContent = d.ok_count || 0;
    document.getElementById('sErr').textContent = d.error_count || 0;
    document.getElementById('sEmails').textContent = d.emails_captured || 0;
    document.getElementById('sAvgSize').textContent = fmtBytes(d.avg_size);
    document.getElementById('sStripe').textContent = d.stripe_enabled ? 'Live' : 'Sim';
    document.getElementById('sStripe').style.color = d.stripe_enabled ? '#00FFC6' : '#F59E0B';
    document.getElementById('sSmtp').textContent = d.smtp_enabled ? 'Live' : 'Off';
    document.getElementById('sSmtp').style.color = d.smtp_enabled ? '#00FFC6' : '#6B6B78';
    document.getElementById('sReqCount').textContent = (d.recent||[]).length + ' shown';
    var ns = Object.keys(d.niche_breakdown || {{}});
    document.getElementById('sLive').textContent = new Date().toLocaleTimeString();
    var nb = document.getElementById('nb'); nb.innerHTML = '';
    var mx = Math.max(1, ...Object.values(d.niche_breakdown || {{}}));
    Object.entries(d.niche_breakdown || {{}}).forEach(function(e) {{
      var pct = (e[1] / mx * 100).toFixed(0);
      var div = document.createElement('div'); div.className = 'flex items-center gap-2';
      div.innerHTML = '<span class="mono text-xs text-white/35 w-28 truncate">' + e[0] + '</span><div class="bb flex-1"><div class="bf" style="width:' + Math.min(pct, 100) + '%"></div></div><span class="mono text-xs text-[#00FFC6]/60 w-6 text-right">' + e[1] + '</span>';
      nb.appendChild(div);
    }});
    var rr = document.getElementById('rr'); rr.innerHTML = '';
    if (!d.recent || !d.recent.length) {{ rr.innerHTML = '<div class="text-[12px] text-white/20 mono">No requests.</div>'; }}
    else {{ d.recent.forEach(function(r) {{
      var ts = new Date(r.time * 1000).toLocaleTimeString([], {{hour:'2-digit',minute:'2-digit'}});
      var sc = r.status === 'ok' ? 'text-emerald-400/60' : (r.status === 'error' ? 'text-red-400/60' : 'text-white/20');
      var row = document.createElement('div'); row.className = 'tr'; row.style.display = 'grid'; row.style.gridTemplateColumns = '1fr 1fr 1fr 60px';
      row.innerHTML = '<span>' + ts + '</span><span class="truncate">' + (r.niche || '') + '</span><span class="truncate">' + (r.ip || '') + '</span><span class="' + sc + '">' + (r.status||'') + '</span>';
      rr.appendChild(row);
    }}); }}
  }}).catch(function() {{
    ['sTotal','sUptime','sOk','sErr','sEmails','sAvgSize'].forEach(function(id) {{ document.getElementById(id).textContent = 'ERR'; }});
    document.getElementById('nb').innerHTML = '<div class="text-[12px] text-red-400/40 mono">Connection failed.</div>';
    document.getElementById('rr').innerHTML = '<div class="text-[12px] text-red-400/40 mono">Connection failed.</div>';
  }});
}}
window.genPDF = function() {{
  var id = document.getElementById('mn').value;
  document.getElementById('ms').textContent = 'Generating...';
  fetch('/admin-api/generate-pdf', {{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{niche_id:id}})}})
  .then(function(r){{if(!r.ok)throw Error('Fail');return r.blob()}})
  .then(function(b){{var u=URL.createObjectURL(b);var a=document.createElement('a');a.href=u;a.download=id+'.pdf';document.body.appendChild(a);a.click();setTimeout(function(){{document.body.removeChild(a);URL.revokeObjectURL(u)}},300);document.getElementById('ms').textContent='Done.';setTimeout(load,500)}})
  .catch(function(e){{document.getElementById('ms').textContent='Error: '+(e.message||'')}});
}};
load(); if (pi) clearInterval(pi); pi = setInterval(load, 5000);
</script>
</body>
</html>"""
