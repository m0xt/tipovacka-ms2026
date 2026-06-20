#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor stránky pro tipovačku MS 2026.

Tipy hráčů jsou statické (turnaj už běží, tipy se nemění) a jsou zapsané přímo tady.
Měnící se data = výsledky odehraných zápasů -> soubor results.json.

Workflow aktualizace:
  1) doplň/uprav výsledky v results.json   (formát: "<číslo zápasu>": [góly_domácí, góly_hosté])
  2) spusť:  python3 build.py
  3) commitni a pushni -> GitHub Pages se aktualizuje

Až skončí turnaj, do CONFIG nastav "champion" na vítězný tým (česky, přesně jak je
v tipech na vítěze), tím se přičte bonus 5 bodů hráčům, kteří ho trefili.
"""

import json
import datetime
import pathlib

HERE = pathlib.Path(__file__).parent

PLAYERS = [
    "Tomis ml.", "Ďurfina", "Hodovanec", "Sváťa", "Prokůpek",
    "Olča", "Lékarník", "Šámal", "Jarda Plechatý",
]

# tip na celkového vítěze turnaje (ve stejném pořadí jako PLAYERS)
CHAMPIONS = [
    "Španělsko", "Brazílie", "Francie", "Španělsko", "Argentina",
    "Brazílie", "Španělsko", "Argentina", "Argentina",
]

CONFIG = {
    "pointsPerMatch": 1,   # bod za správně tipnutý výsledek (1/0/2)
    "championBonus": 5,    # bonus za správně tipnutého vítěze turnaje
    "champion": None,      # až bude znám vítěz turnaje, dej sem jeho jméno (česky)
}

# (domácí, hosté, "tipy") – tipy = 9 znaků 1/0/2 v pořadí PLAYERS
#   1 = výhra domácích, 0 = remíza, 2 = výhra hostů
MATCHES = [
    ("Mexiko", "JAR", "111111111"),
    ("Jižní Korea", "Česko", "022022220"),
    ("Kanada", "Bosna a Hercegovina", "102021020"),
    ("USA", "Paraguay", "101110021"),
    ("Katar", "Švýcarsko", "212002222"),
    ("Brazílie", "Maroko", "111111101"),
    ("Haiti", "Skotsko", "202220222"),
    ("Austrálie", "Turecko", "212002022"),
    ("Německo", "Curacao", "111111111"),
    ("Nizozemsko", "Japonsko", "111101111"),
    ("Pobřeží slonoviny", "Ekvádor", "022211220"),
    ("Švédsko", "Tunisko", "111011110"),
    ("Španělsko", "Kapverdy", "111111111"),
    ("Belgie", "Egypt", "121000121"),
    ("Saudská Arábie", "Uruguay", "222222222"),
    ("Írán", "Nový Zéland", "102100020"),
    ("Francie", "Senegal", "111111111"),
    ("Irák", "Norsko", "202002222"),
    ("Argentina", "Alžírsko", "111011111"),
    ("Rakousko", "Jordánsko", "111111111"),
    ("Portugalsko", "DR Kongo", "111111111"),
    ("Anglie", "Chorvatsko", "111101121"),
    ("Ghana", "Panama", "111111101"),
    ("Uzbekistán", "Kolumbie", "222021212"),
    ("Česko", "JAR", "112110111"),
    ("Švýcarsko", "Bosna a Hercegovina", "111011121"),
    ("Kanada", "Katar", "121011000"),
    ("Mexiko", "Jižní Korea", "111111111"),
    ("USA", "Austrálie", "121001011"),
    ("Skotsko", "Maroko", "221012020"),
    ("Brazílie", "Haiti", "111111111"),
    ("Turecko", "Paraguay", "021020010"),
    ("Nizozemsko", "Švédsko", "111001121"),
    ("Německo", "Pobřeží slonoviny", "111111111"),
    ("Ekvádor", "Curacao", "111111111"),
    ("Tunisko", "Japonsko", "212202010"),
    ("Španělsko", "Saudská Arábie", "111111111"),
    ("Belgie", "Írán", "111001111"),
    ("Uruguay", "Kapverdy", "111111111"),
    ("Nový Zéland", "Egypt", "222202022"),
    ("Argentina", "Rakousko", "111110111"),
    ("Francie", "Irák", "111111111"),
    ("Norsko", "Senegal", "201020120"),
    ("Jordánsko", "Alžírsko", "202022222"),
    ("Portugalsko", "Uzbekistán", "111111111"),
    ("Anglie", "Ghana", "111111111"),
    ("Panama", "Chorvatsko", "202222222"),
    ("Kolumbie", "DR Kongo", "112111101"),
    ("Švýcarsko", "Kanada", "001000110"),
    ("Bosna a Hercegovina", "Katar", "121011010"),
    ("Maroko", "Haiti", "111111111"),
    ("Skotsko", "Brazílie", "222222222"),
    ("JAR", "Jižní Korea", "211020020"),
    ("Česko", "Mexiko", "202001122"),
    ("Curacao", "Pobřeží slonoviny", "222222022"),
    ("Ekvádor", "Německo", "202012222"),
    ("Tunisko", "Nizozemsko", "222222220"),
    ("Japonsko", "Švédsko", "102220021"),
    ("Turecko", "USA", "101022210"),
    ("Paraguay", "Austrálie", "111000111"),
    ("Norsko", "Francie", "222222222"),
    ("Senegal", "Irák", "111001011"),
    ("Kapverdy", "Saudská Arábie", "002211222"),
    ("Uruguay", "Španělsko", "202002222"),
    ("Nový Zéland", "Belgie", "222202222"),
    ("Egypt", "Írán", "111110010"),
    ("Panama", "Anglie", "202222222"),
    ("Chorvatsko", "Ghana", "111111111"),
    ("Kolumbie", "Portugalsko", "222000220"),
    ("DR Kongo", "Uzbekistán", "102011020"),
    ("Alžírsko", "Rakousko", "102022021"),
    ("Jordánsko", "Argentina", "222222222"),
]


def build_data():
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    matches = []
    for i, (home, away, tips) in enumerate(MATCHES, start=1):
        matches.append({
            "n": i,
            "home": home,
            "away": away,
            "tips": [int(c) for c in tips],
        })
    return {
        "players": PLAYERS,
        "champions": CHAMPIONS,
        "config": CONFIG,
        "matches": matches,
        "results": results,
        "updated": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tipovačka MS 2026 🏆</title>
<style>
  :root{
    --bg:#0b1020; --bg2:#121a30; --card:#161f38; --card2:#1c2742;
    --line:#26304d; --txt:#e9edf7; --mut:#90a0c0; --acc:#3ea6ff;
    --gold:#ffd24a; --silver:#cfd6e6; --bronze:#e0915a;
    --ok:#37d39b; --bad:#ff5f6d; --pend:#5a6890;
  }
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    background:linear-gradient(180deg,#0b1020,#0d1428 40%,#0b1020);color:var(--txt);
    -webkit-font-smoothing:antialiased;line-height:1.45}
  a{color:var(--acc)}
  .wrap{max-width:1100px;margin:0 auto;padding:20px 16px 64px}
  header.top{text-align:center;padding:18px 0 6px}
  header.top h1{margin:0;font-size:clamp(26px,5vw,40px);letter-spacing:.5px}
  header.top .sub{color:var(--mut);margin-top:4px;font-size:14px}
  .updated{color:var(--mut);font-size:12.5px;margin-top:8px}
  .updated b{color:var(--txt)}

  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:20px 0}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
  .stat .lab{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.6px}
  .stat .val{font-size:24px;font-weight:700;margin-top:4px}
  .stat .val.sm{font-size:18px}

  nav.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 16px;position:sticky;top:0;
    background:rgba(11,16,32,.85);backdrop-filter:blur(8px);padding:10px 0;z-index:5;border-bottom:1px solid var(--line)}
  nav.tabs button{background:var(--card);border:1px solid var(--line);color:var(--mut);
    padding:8px 14px;border-radius:999px;cursor:pointer;font-size:14px;font-weight:600;transition:.15s}
  nav.tabs button:hover{color:var(--txt)}
  nav.tabs button.active{background:var(--acc);border-color:var(--acc);color:#06121f}

  section{display:none;animation:fade .2s ease}
  section.show{display:block}
  @keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1}}
  h2.sec{font-size:18px;margin:6px 0 14px;display:flex;align-items:center;gap:8px}

  table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);
    border-radius:14px;overflow:hidden}
  th,td{padding:11px 12px;text-align:left;border-bottom:1px solid var(--line);font-size:14px}
  th{color:var(--mut);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.5px;background:var(--bg2)}
  tr:last-child td{border-bottom:none}
  tbody tr:hover{background:var(--card2)}
  td.num,th.num{text-align:center}

  /* leaderboard */
  .lb td.rank{font-weight:800;font-size:16px;text-align:center;width:54px}
  .lb tr.r1{background:linear-gradient(90deg,rgba(255,210,74,.14),transparent)}
  .lb tr.r2{background:linear-gradient(90deg,rgba(207,214,230,.10),transparent)}
  .lb tr.r3{background:linear-gradient(90deg,rgba(224,145,90,.10),transparent)}
  .lb .pts{font-weight:800;font-size:17px}
  .lb .name{font-weight:600}
  .medal{font-size:18px}
  .champ-pill{display:inline-block;font-size:12px;color:var(--mut);background:var(--bg2);
    border:1px solid var(--line);border-radius:999px;padding:2px 9px}
  .champ-pill.hit{color:#06121f;background:var(--gold);border-color:var(--gold);font-weight:700}

  .bar{height:8px;background:var(--bg2);border-radius:999px;overflow:hidden;margin-top:6px;min-width:90px}
  .bar > i{display:block;height:100%;background:linear-gradient(90deg,var(--acc),#7ad0ff)}

  .badge{display:inline-block;font-size:11px;font-weight:700;border-radius:6px;padding:2px 7px}
  .b1{background:rgba(62,166,255,.18);color:#7cc4ff}
  .b0{background:rgba(255,210,74,.18);color:var(--gold)}
  .b2{background:rgba(170,120,255,.20);color:#c3a6ff}

  /* tip dots */
  .dot{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:7px;
    font-size:12px;font-weight:700;margin:1px}
  .dot.ok{background:rgba(55,211,155,.18);color:var(--ok)}
  .dot.bad{background:rgba(255,95,109,.15);color:var(--bad)}
  .dot.pend{background:var(--bg2);color:var(--pend)}

  .matchcell{font-weight:600}
  .score{font-weight:800;letter-spacing:.5px}
  .score .o{color:var(--mut);font-weight:600}
  .muted{color:var(--mut)}
  .right{text-align:right}
  .center{text-align:center}

  .grid-players{display:flex;flex-wrap:wrap;gap:4px}
  .legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--mut);font-size:12.5px;margin:0 0 12px}
  .legend span{display:inline-flex;align-items:center;gap:6px}
  .swatch{width:14px;height:14px;border-radius:4px;display:inline-block}

  .scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:14px}
  .matrix th.pl{writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;font-size:11px;padding:8px 4px}
  .matrix td,.matrix th{padding:6px 6px;text-align:center;font-size:12px}
  .matrix td.mh{text-align:left;white-space:nowrap;font-weight:600;font-size:12.5px}

  .funfact{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:12px}
  .funfact h3{margin:0 0 6px;font-size:14px;color:var(--acc)}
  .funfact p{margin:0;font-size:14px}
  .big{font-size:20px;font-weight:800}

  footer{margin-top:40px;text-align:center;color:var(--mut);font-size:12.5px}
  @media(max-width:640px){
    th,td{padding:9px 8px;font-size:13px}
    .hide-sm{display:none}
  }
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <h1>🏆 Tipovačka MS&nbsp;2026</h1>
    <div class="sub">Žebříček a statistiky naší tipovací soutěže</div>
    <div class="updated">Aktualizováno: <b id="updated"></b> · <span id="progress"></span></div>
  </header>

  <div class="cards" id="cards"></div>

  <nav class="tabs" id="tabs">
    <button data-t="zebricek" class="active">🏅 Žebříček</button>
    <button data-t="zapasy">⚽ Odehrané zápasy</button>
    <button data-t="vsechny">📋 Všechny tipy</button>
    <button data-t="staty">📊 Statistiky</button>
    <button data-t="vitez">👑 Tip na vítěze</button>
  </nav>

  <section id="zebricek" class="show">
    <h2 class="sec">🏅 Pořadí</h2>
    <div class="scroll"><table class="lb"><thead><tr>
      <th class="num">#</th><th>Hráč</th><th class="num">Body</th>
      <th class="num hide-sm">Trefeno</th><th class="hide-sm">Úspěšnost</th><th>Tip na vítěze</th>
    </tr></thead><tbody id="lbBody"></tbody></table></div>
    <p class="muted" style="font-size:12.5px;margin-top:10px">
      Body = počet správně tipnutých výsledků (1&nbsp;bod/zápas). Bonus za vítěze turnaje (+5&nbsp;bodů)
      se přičte po finále.</p>
  </section>

  <section id="zapasy">
    <h2 class="sec">⚽ Odehrané zápasy</h2>
    <div class="legend">
      <span><i class="swatch" style="background:rgba(55,211,155,.6)"></i> trefil</span>
      <span><i class="swatch" style="background:rgba(255,95,109,.5)"></i> netrefil</span>
      <span><span class="badge b1">1</span> výhra domácích · <span class="badge b0">0</span> remíza · <span class="badge b2">2</span> výhra hostů</span>
    </div>
    <div class="scroll"><table><thead id="zHead"></thead><tbody id="zBody"></tbody></table></div>
  </section>

  <section id="vsechny">
    <h2 class="sec">📋 Všechny tipy (72 zápasů)</h2>
    <div class="legend">
      <span><span class="dot ok">1</span> trefený tip</span>
      <span><span class="dot bad">2</span> mimo</span>
      <span><span class="dot pend">1</span> zatím neodehráno</span>
    </div>
    <div class="scroll"><table class="matrix"><thead id="mHead"></thead><tbody id="mBody"></tbody></table></div>
  </section>

  <section id="staty">
    <h2 class="sec">📊 Statistiky</h2>
    <div id="funfacts"></div>
    <h2 class="sec" style="margin-top:24px">Úspěšnost hráčů</h2>
    <div class="scroll"><table><thead><tr>
      <th>Hráč</th><th class="num">Trefeno</th><th class="num">Odehráno</th><th>Úspěšnost</th>
    </tr></thead><tbody id="succBody"></tbody></table></div>
  </section>

  <section id="vitez">
    <h2 class="sec">👑 Tipy na celkového vítěze</h2>
    <p class="muted" style="font-size:13px;margin-top:-6px">Za trefeného vítěze turnaje je bonus +5 bodů (vyhodnotí se po finále).</p>
    <div class="scroll"><table><thead><tr><th>Vítěz</th><th class="num">Počet tipů</th><th>Tipující</th></tr></thead>
      <tbody id="champBody"></tbody></table></div>
  </section>

  <footer>
    Postaveno z Google Sheetu tipovačky · výsledky se aktualizují automaticky během dne ·
    1&nbsp;bod za trefený výsledek, +5 za vítěze turnaje
  </footer>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const {players, champions, config, matches, results, updated} = DATA;

function outcome(h,a){ return h>a?1 : (h===a?0:2); }
const res = {}; // n -> {h,a,o}
for(const k in results){ const [h,a]=results[k]; res[+k]={h,a,o:outcome(h,a)}; }
const playedNums = matches.filter(m=>res[m.n]).map(m=>m.n);
const playedCount = playedNums.length;

// ---- standings ----
const stats = players.map((name,i)=>({i,name,correct:0,played:0,champ:champions[i]}));
for(const m of matches){
  const r=res[m.n]; if(!r) continue;
  players.forEach((_,i)=>{ stats[i].played++; if(m.tips[i]===r.o) stats[i].correct++; });
}
stats.forEach(s=>{
  s.champBonus = (config.champion && s.champ===config.champion) ? config.championBonus : 0;
  s.points = s.correct*config.pointsPerMatch + s.champBonus;
  s.rate = s.played? s.correct/s.played : 0;
});
const ranked = [...stats].sort((a,b)=> b.points-a.points || b.rate-a.rate || a.name.localeCompare(b.name,'cs'));
// dense-ish competition ranking (stejné body = stejné místo)
let lastPts=null, lastRank=0;
ranked.forEach((s,idx)=>{ if(s.points!==lastPts){lastRank=idx+1; lastPts=s.points;} s.rank=lastRank; });

const pct = x=> (x*100).toFixed(0)+' %';
const esc = s=> String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

// ---- header bits ----
document.getElementById('updated').textContent = updated;
document.getElementById('progress').innerHTML = `odehráno <b>${playedCount}</b> / ${matches.length} zápasů`;

// ---- stat cards ----
const leader = ranked[0];
const bestRate = [...stats].filter(s=>s.played>0).sort((a,b)=>b.rate-a.rate)[0];
const avgPts = (stats.reduce((s,x)=>s+x.points,0)/stats.length).toFixed(1);
const tightGap = ranked.length>1 ? (ranked[0].points-ranked[1].points) : 0;
document.getElementById('cards').innerHTML = [
  card('Vedoucí', leader? `${medal(1)} ${esc(leader.name)}` : '–', leader? `${leader.points} b.` : '', true),
  card('Nejlepší úspěšnost', bestRate? esc(bestRate.name):'–', bestRate? pct(bestRate.rate):'' , true),
  card('Odehráno', `${playedCount} / ${matches.length}`, 'zápasů'),
  card('Náskok v čele', tightGap>0? `+${tightGap} b.` : 'dělené 1.', ''),
].join('');
function card(lab,val,sub,sm){ return `<div class="stat"><div class="lab">${lab}</div>
  <div class="val ${sm?'sm':''}">${val}</div>${sub?`<div class="muted" style="font-size:12px;margin-top:2px">${sub}</div>`:''}</div>`; }
function medal(r){ return r===1?'🥇':r===2?'🥈':r===3?'🥉':''; }

// ---- leaderboard ----
document.getElementById('lbBody').innerHTML = ranked.map(s=>{
  const champHit = config.champion && s.champ===config.champion;
  return `<tr class="${s.rank<=3?'r'+s.rank:''}">
    <td class="rank">${s.rank<=3?medal(s.rank):s.rank}</td>
    <td class="name">${esc(s.name)}</td>
    <td class="num"><span class="pts">${s.points}</span>${s.champBonus?` <span class="muted" style="font-size:11px">(+${s.champBonus})</span>`:''}</td>
    <td class="num hide-sm">${s.correct}/${s.played}</td>
    <td class="hide-sm"><div class="bar"><i style="width:${(s.rate*100).toFixed(0)}%"></i></div><span class="muted" style="font-size:11px">${pct(s.rate)}</span></td>
    <td><span class="champ-pill ${champHit?'hit':''}">${esc(s.champ)}${champHit?' ✓':''}</span></td>
  </tr>`;
}).join('');

// ---- played matches table ----
document.getElementById('zHead').innerHTML = `<tr>
  <th class="num">#</th><th>Zápas</th><th class="center">Výsledek</th>
  ${players.map(p=>`<th class="center hide-sm" title="${esc(p)}">${esc(shortName(p))}</th>`).join('')}
</tr>`;
function shortName(p){ return p.length>9? p.slice(0,8)+'…' : p; }
const playedSorted = matches.filter(m=>res[m.n]).sort((a,b)=>b.n-a.n);
document.getElementById('zBody').innerHTML = playedSorted.map(m=>{
  const r=res[m.n];
  return `<tr>
    <td class="num muted">${m.n}</td>
    <td class="matchcell">${esc(m.home)} – ${esc(m.away)}</td>
    <td class="center"><span class="score">${r.h}<span class="o">:</span>${r.a}</span> <span class="badge b${r.o}">${r.o}</span></td>
    ${m.tips.map(t=>`<td class="center hide-sm"><span class="dot ${t===r.o?'ok':'bad'}">${t}</span></td>`).join('')}
  </tr>`;
}).join('');

// ---- all tips matrix ----
document.getElementById('mHead').innerHTML = `<tr>
  <th class="num">#</th><th>Zápas</th><th class="center">Výsl.</th>
  ${players.map(p=>`<th class="pl">${esc(p)}</th>`).join('')}
</tr>`;
document.getElementById('mBody').innerHTML = matches.map(m=>{
  const r=res[m.n];
  const scoreCell = r? `<span class="score">${r.h}<span class="o">:</span>${r.a}</span>` : '<span class="muted">–</span>';
  return `<tr>
    <td class="num muted">${m.n}</td>
    <td class="mh">${esc(m.home)} – ${esc(m.away)}</td>
    <td class="center">${scoreCell}</td>
    ${m.tips.map(t=>{
      let cls='pend'; if(r) cls = (t===r.o)?'ok':'bad';
      return `<td><span class="dot ${cls}">${t}</span></td>`;
    }).join('')}
  </tr>`;
}).join('');

// ---- success table ----
document.getElementById('succBody').innerHTML = [...stats].sort((a,b)=>b.rate-a.rate||b.correct-a.correct).map(s=>`
  <tr><td class="name">${esc(s.name)}</td><td class="num">${s.correct}</td><td class="num">${s.played}</td>
  <td><div class="bar"><i style="width:${(s.rate*100).toFixed(0)}%"></i></div>
  <span class="muted" style="font-size:11px">${pct(s.rate)}</span></td></tr>`).join('');

// ---- fun facts ----
const funfacts = [];
if(playedCount>0){
  // most surprising played match = fewest correct tips
  let surprise=null, surpC=99;
  let banker=null, bankC=-1;
  for(const m of playedSorted){
    const r=res[m.n]; const c=m.tips.filter(t=>t===r.o).length;
    if(c<surpC){surpC=c; surprise=m;}
    if(c>bankC){bankC=c; banker=m;}
  }
  funfacts.push(fact('🤯 Největší překvapení',
    `${esc(surprise.home)} – ${esc(surprise.away)} (${res[surprise.n].h}:${res[surprise.n].a}) trefilo jen <span class="big">${surpC}</span> z ${players.length} tipujících.`));
  funfacts.push(fact('✅ Nejjistější trefa',
    `${esc(banker.home)} – ${esc(banker.away)} (${res[banker.n].h}:${res[banker.n].a}) trefilo <span class="big">${bankC}</span> z ${players.length}.`));
}
// unanimous predictions (all same tip) – among all matches
const unanimous = matches.filter(m=>m.tips.every(t=>t===m.tips[0]));
const unanimousPlayed = unanimous.filter(m=>res[m.n]);
const unanimousHit = unanimousPlayed.filter(m=>m.tips[0]===res[m.n].o).length;
funfacts.push(fact('🤝 Jednomyslné tipy',
  `Na <span class="big">${unanimous.length}</span> zápasů tipli všichni stejně` +
  (unanimousPlayed.length? ` — z ${unanimousPlayed.length} odehraných jich vyšlo <span class="big">${unanimousHit}</span>.` : '.')));
// biggest goal fest
if(playedCount>0){
  let fest=null, festG=-1;
  for(const m of playedSorted){ const r=res[m.n]; if(r.h+r.a>festG){festG=r.h+r.a; fest=m;} }
  funfacts.push(fact('🎯 Nejvíc gólů',
    `${esc(fest.home)} – ${esc(fest.away)} <span class="big">${res[fest.n].h}:${res[fest.n].a}</span> (${festG} gólů).`));
}
document.getElementById('funfacts').innerHTML = funfacts.join('');
function fact(h,p){ return `<div class="funfact"><h3>${h}</h3><p>${p}</p></div>`; }

// ---- champion picks ----
const byChamp = {};
champions.forEach((c,i)=>{ (byChamp[c]=byChamp[c]||[]).push(players[i]); });
document.getElementById('champBody').innerHTML = Object.entries(byChamp)
  .sort((a,b)=>b[1].length-a[1].length).map(([c,ps])=>{
    const hit = config.champion && c===config.champion;
    return `<tr><td class="name">${esc(c)}${hit?' 👑':''}</td><td class="num">${ps.length}</td>
      <td class="muted">${ps.map(esc).join(', ')}</td></tr>`;
  }).join('');

// ---- tabs ----
document.getElementById('tabs').addEventListener('click',e=>{
  const b=e.target.closest('button'); if(!b) return;
  document.querySelectorAll('nav.tabs button').forEach(x=>x.classList.toggle('active',x===b));
  document.querySelectorAll('section').forEach(s=>s.classList.toggle('show',s.id===b.dataset.t));
  window.scrollTo({top:0,behavior:'smooth'});
});
</script>
</body>
</html>
"""


def main():
    data = build_data()
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    (HERE / "index.html").write_text(html, encoding="utf-8")
    pc = len(data["results"])
    print(f"OK: index.html vygenerován ({len(data['matches'])} zápasů, {pc} výsledků, {data['updated']})")


if __name__ == "__main__":
    main()
