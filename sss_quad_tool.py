import streamlit as st
import json
import requests
import pandas as pd
import base64
from datetime import datetime
from io import StringIO

st.set_page_config(page_title="SSS/Quad Tool", page_icon="🎾", layout="wide", initial_sidebar_state="expanded")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{--bg:#0B1215;--bg-sec:#1E293B;--accent:#10B981;--accent-dim:#0d9268;--slate:#334155;--text:#E2E8F0;--muted:#94A3B8;--border:rgba(16,185,129,0.18);--glow:0 0 24px rgba(16,185,129,0.15);}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--bg)!important;color:var(--text)!important;}
[data-testid="stSidebar"]{background-color:var(--bg-sec)!important;border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text)!important;}
.block-container{padding:2rem 2.5rem!important;max-width:1400px;}
#MainMenu,footer,header{visibility:hidden;}
.brand-header{display:flex;align-items:center;gap:12px;margin-bottom:2rem;border-bottom:1px solid var(--border);padding-bottom:1.25rem;}
.brand-title{font-family:'Space Mono',monospace;font-size:1.55rem;font-weight:700;color:var(--accent);letter-spacing:-0.5px;}
.brand-sub{font-size:0.75rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-top:2px;}
.section-label{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:3px;text-transform:uppercase;color:var(--accent);margin-bottom:0.6rem;}
.match-card{background:var(--slate);border:1px solid var(--border);border-radius:14px;padding:1.4rem 1.8rem;box-shadow:var(--glow);margin-bottom:1rem;position:relative;overflow:hidden;}
.match-card::before{content:'';position:absolute;top:0;left:0;width:4px;height:100%;background:var(--accent);border-radius:4px 0 0 4px;}
.match-title{font-family:'Space Mono',monospace;font-size:1.2rem;font-weight:700;color:#fff;margin-bottom:0.2rem;}
.match-meta{font-size:0.82rem;color:var(--muted);letter-spacing:0.5px;}
.quad-card{background:var(--bg-sec);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.3rem;height:100%;box-shadow:var(--glow);}
.quad-card:hover{border-color:var(--accent);}
.quad-header{display:flex;align-items:center;gap:8px;margin-bottom:0.65rem;}
.quad-icon{font-size:1.2rem;}
.quad-title{font-family:'Space Mono',monospace;font-size:0.75rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent);}
.quad-body{font-size:0.86rem;color:var(--muted);line-height:1.65;}
.quad-body strong{color:var(--text);}
.verdict-banner{background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(16,185,129,0.04));border:1px solid var(--accent);border-radius:12px;padding:1.3rem 1.6rem;margin-top:1.2rem;display:flex;justify-content:space-between;align-items:center;}
.verdict-label{font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:3px;text-transform:uppercase;color:var(--muted);margin-bottom:4px;}
.verdict-pick{font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;color:var(--accent);}
.confidence-num{font-family:'Space Mono',monospace;font-size:2.1rem;font-weight:700;line-height:1;}
.confidence-tag{font-size:0.7rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-top:3px;}
.method-card{background:rgba(16,185,129,0.05);border:1px solid var(--border);border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.7rem;}
.method-title{font-family:'Space Mono',monospace;font-size:0.75rem;color:var(--accent);letter-spacing:1px;text-transform:uppercase;margin-bottom:0.4rem;}
.method-desc{font-size:0.8rem;color:var(--muted);line-height:1.55;}
.stat-card{background:var(--bg-sec);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.4rem;text-align:center;box-shadow:var(--glow);}
.stat-card-value{font-family:'Space Mono',monospace;font-size:1.8rem;font-weight:700;line-height:1;margin-bottom:4px;}
.stat-card-label{font-size:0.68rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;}
.odds-book-card{background:var(--bg-sec);border:1px solid var(--border);border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.4rem;}
.odds-book-name{font-family:'Space Mono',monospace;font-size:0.72rem;color:var(--accent);letter-spacing:1px;text-transform:uppercase;}
.auto-fill-badge{display:inline-block;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);color:#10B981;font-family:monospace;font-size:0.65rem;letter-spacing:1.5px;padding:2px 8px;border-radius:4px;text-transform:uppercase;margin-bottom:0.6rem;}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input{background-color:#0f1923!important;border:1px solid var(--border)!important;border-radius:8px!important;color:var(--text)!important;}
[data-testid="stTextInput"] label,[data-testid="stSelectbox"] label,[data-testid="stNumberInput"] label{color:var(--muted)!important;font-size:0.78rem!important;letter-spacing:1px!important;}
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid var(--border);gap:4px;}
[data-testid="stTabs"] [data-baseweb="tab"]{font-family:'Space Mono',monospace!important;font-size:0.72rem!important;letter-spacing:2px!important;text-transform:uppercase!important;color:var(--muted)!important;background:transparent!important;border:none!important;padding:0.6rem 1.2rem!important;}
[data-testid="stTabs"] [aria-selected="true"]{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}
[data-testid="stButton"] button{background:linear-gradient(135deg,var(--accent-dim),var(--accent))!important;color:#fff!important;font-family:'Space Mono',monospace!important;font-size:0.78rem!important;letter-spacing:2px!important;text-transform:uppercase!important;border:none!important;border-radius:8px!important;padding:0.6rem 1.6rem!important;font-weight:700!important;width:100%!important;}
[data-testid="stButton"] button:hover{opacity:0.88!important;}
[data-testid="stSelectbox"] > div > div{background-color:var(--bg-sec)!important;border:1px solid var(--border)!important;border-radius:8px!important;color:var(--text)!important;}
.custom-divider{border:none;border-top:1px solid var(--border);margin:1.4rem 0;}
.form-section-title{font-family:'Space Mono',monospace;font-size:0.72rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--accent);margin-bottom:0.8rem;margin-top:1rem;padding-bottom:0.4rem;border-bottom:1px solid var(--border);}
[data-testid="stDataEditor"]{border:1px solid var(--border)!important;border-radius:10px!important;}
[data-testid="stRadio"] label{font-family:'Space Mono',monospace!important;font-size:0.72rem!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
PREFERRED_BOOKS = ["bet365", "williamhill", "betfair", "unibet", "ladbrokes", "skybet"]
BOOK_LABELS = {
    "bet365": "Bet365",
    "williamhill": "William Hill",
    "betfair": "Betfair Exchange",
    "unibet": "Unibet",
    "ladbrokes": "Ladbrokes",
    "skybet": "SkyBet",
    "paddypower": "Paddy Power",
    "coral": "Coral",
    "betfair_ex_uk": "Betfair Exchange (UK)",
    "betvictor": "BetVictor",
    "boylesports": "BoyleSports",
    "draftkings": "DraftKings",
    "fanduel": "FanDuel",
    "pinnacle": "Pinnacle",
}

# ── GITHUB CSV ────────────────────────────────────────────────────────────────
CSV_COLS = ["Date","Match","Tournament","Surface","Pick","Odds",
            "Stake (units)","Confidence %","Methodology","Result","P&L (units)","Notes"]
CSV_PATH = "results.csv"

def _gh_headers():
    return {"Authorization": "token " + st.secrets.get("GITHUB_TOKEN",""),
            "Accept": "application/vnd.github.v3+json"}

def _gh_repo():
    return st.secrets.get("GITHUB_REPO","")

def load_csv_from_github():
    url  = "https://api.github.com/repos/" + _gh_repo() + "/contents/" + CSV_PATH
    resp = requests.get(url, headers=_gh_headers(), timeout=10)
    if resp.status_code == 404:
        return pd.DataFrame(columns=CSV_COLS)
    resp.raise_for_status()
    content = base64.b64decode(resp.json()["content"]).decode("utf-8")
    df = pd.read_csv(StringIO(content))
    for col in ["Stake (units)","Confidence %","P&L (units)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def save_csv_to_github(df, msg="Update results.csv"):
    url     = "https://api.github.com/repos/" + _gh_repo() + "/contents/" + CSV_PATH
    encoded = base64.b64encode(df.to_csv(index=False).encode()).decode()
    get_r   = requests.get(url, headers=_gh_headers(), timeout=10)
    payload = {"message": msg, "content": encoded}
    if get_r.status_code == 200:
        payload["sha"] = get_r.json()["sha"]
    requests.put(url, headers=_gh_headers(), json=payload, timeout=15).raise_for_status()

def american_to_decimal(odds_str):
    try:
        o = int(str(odds_str).replace("+","").strip())
        return round(o/100+1,4) if o>0 else round(100/abs(o)+1,4)
    except:
        return 0.0

def decimal_to_american(dec):
    try:
        dec = float(dec)
        if dec >= 2.0:
            return "+" + str(int(round((dec-1)*100)))
        else:
            return str(int(round(-100/(dec-1))))
    except:
        return "—"

def calc_pnl(odds_str, stake, result):
    d = american_to_decimal(odds_str)
    if result == "WIN":  return round((d-1)*stake, 2)
    if result == "LOSS": return round(-stake, 2)
    return 0.0

# ── THE ODDS API ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=180)
def fetch_tennis_odds():
    """Fetch live tennis odds from The Odds API across all bookmakers."""
    key = st.secrets.get("ODDS_API_KEY","")
    if not key:
        return []
    try:
        resp = requests.get(
            "https://api.the-odds-api.com/v4/sports/tennis/odds/",
            params={
                "apiKey": key,
                "regions": "uk,eu",
                "markets": "h2h",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        return resp.json()
    except Exception:
        return []

def extract_odds_for_match(odds_data, p1_name, p2_name, preferred_book):
    """
    Find the best odds match from The Odds API data for a given match.
    Returns (p1_decimal, p2_decimal, book_used) or (None, None, None).
    """
    if not odds_data:
        return None, None, None

    p1_last = p1_name.split(",")[0].split()[-1].lower()
    p2_last = p2_name.split(",")[0].split()[-1].lower()

    best_event = None
    best_score = 0
    for event in odds_data:
        names = [c["name"].lower() for c in event.get("bookmakers",[{}])[0].get("markets",[{}])[0].get("outcomes",[])]
        if not names:
            # try home/away from event title
            title = event.get("home_team","").lower() + " " + event.get("away_team","").lower()
            names = [title]
        score = sum(1 for n in names if p1_last in n or p2_last in n)
        if score > best_score:
            best_score = score
            best_event = event

    if not best_event or best_score == 0:
        return None, None, None

    # Find the preferred bookmaker, fall back to first available
    bookmakers = best_event.get("bookmakers", [])
    chosen_book = None
    for bm in bookmakers:
        if bm["key"] == preferred_book:
            chosen_book = bm
            break
    if not chosen_book and bookmakers:
        chosen_book = bookmakers[0]
    if not chosen_book:
        return None, None, None

    outcomes = chosen_book.get("markets",[{}])[0].get("outcomes",[])
    p1_dec, p2_dec = None, None
    for o in outcomes:
        name_lower = o["name"].lower()
        if p1_last in name_lower:
            p1_dec = o["price"]
        elif p2_last in name_lower:
            p2_dec = o["price"]

    book_label = BOOK_LABELS.get(chosen_book["key"], chosen_book.get("title", chosen_book["key"]))
    return p1_dec, p2_dec, book_label

def get_available_books(odds_data, p1_name, p2_name):
    """Return list of (key, label) for all books offering this match."""
    if not odds_data:
        return []
    p1_last = p1_name.split(",")[0].split()[-1].lower()
    p2_last = p2_name.split(",")[0].split()[-1].lower()
    for event in odds_data:
        bookmakers = event.get("bookmakers", [])
        # Check if this event is for our match
        all_outcomes = []
        for bm in bookmakers:
            for mkt in bm.get("markets",[]):
                all_outcomes += [o["name"].lower() for o in mkt.get("outcomes",[])]
        if any(p1_last in n or p2_last in n for n in all_outcomes):
            books = [(bm["key"], BOOK_LABELS.get(bm["key"], bm.get("title", bm["key"]))) for bm in bookmakers]
            # Sort: preferred books first
            preferred = [(k,l) for k,l in books if k in PREFERRED_BOOKS]
            others    = [(k,l) for k,l in books if k not in PREFERRED_BOOKS]
            preferred.sort(key=lambda x: PREFERRED_BOOKS.index(x[0]) if x[0] in PREFERRED_BOOKS else 99)
            return preferred + others
    return []

# ── API-TENNIS (RapidAPI) ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_player_stats(player_name):
    """
    Fetch player ranking, recent form, and key surface strength from API-Tennis.
    Returns dict with: ranking, form (last 5), surface_strength, nationality
    """
    key = st.secrets.get("RAPIDAPI_KEY","")
    if not key:
        return {}
    try:
        # Search for player
        search_resp = requests.get(
            "https://api-tennis.p.rapidapi.com/tennis/",
            params={"method": "get_players", "search": player_name},
            headers={
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": "api-tennis.p.rapidapi.com",
            },
            timeout=8,
        )
        if search_resp.status_code != 200:
            return {}
        players = search_resp.json().get("result", [])
        if not players:
            return {}

        # Take the best name match
        player_last = player_name.split(",")[0].strip().lower()
        best = None
        for p in players:
            full = (p.get("player_name","") + " " + p.get("player_key","")).lower()
            if player_last in full:
                best = p
                break
        if not best:
            best = players[0]

        player_key = best.get("player_key","")
        if not player_key:
            return {}

        # Fetch player details
        detail_resp = requests.get(
            "https://api-tennis.p.rapidapi.com/tennis/",
            params={"method": "get_players", "player_key": player_key},
            headers={
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": "api-tennis.p.rapidapi.com",
            },
            timeout=8,
        )
        if detail_resp.status_code != 200:
            return {}
        detail = detail_resp.json().get("result", [{}])
        if not detail:
            return {}
        p = detail[0]

        ranking = p.get("player_rank", "") or p.get("ranking","")
        return {
            "ranking":   "#" + str(ranking) if ranking else "—",
            "name":      p.get("player_name", player_name),
            "hand":      p.get("player_hand",""),
            "country":   p.get("player_country",""),
        }
    except Exception:
        return {}

@st.cache_data(ttl=1800)
def fetch_player_recent_form(player_name):
    """Fetch last 5 match results for a player."""
    key = st.secrets.get("RAPIDAPI_KEY","")
    if not key:
        return "—"
    try:
        resp = requests.get(
            "https://api-tennis.p.rapidapi.com/tennis/",
            params={"method": "get_H2H", "player_1": player_name, "player_2": ""},
            headers={
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": "api-tennis.p.rapidapi.com",
            },
            timeout=8,
        )
        if resp.status_code != 200:
            return "—"
        data = resp.json()
        # Extract last 5 from player_1_wins + player_2_wins sorted by date
        p1_wins = data.get("result",{}).get("player_1_wins",[])
        p2_wins = data.get("result",{}).get("player_2_wins",[])
        results = []
        for m in p1_wins:
            results.append({"date": m.get("match_date",""), "result": "W"})
        for m in p2_wins:
            results.append({"date": m.get("match_date",""), "result": "L"})
        results.sort(key=lambda x: x["date"], reverse=True)
        form = " ".join(r["result"] for r in results[:5])
        return form if form else "—"
    except Exception:
        return "—"

# ── LIVE MATCH FEED ───────────────────────────────────────────────────────────
@st.cache_data(ttl=120)
def fetch_live_tennis():
    key = st.secrets.get("SPORTRADAR_KEY","")
    if not key:
        return []
    try:
        resp = requests.get(
            "https://api.sportradar.us/tennis/trial/v3/en/schedules/live/summaries.json",
            params={"api_key": key}, timeout=8,
        )
        if resp.status_code != 200:
            return []
        games = []
        for s in resp.json().get("summaries",[]):
            se   = s.get("sport_event",{})
            comp = se.get("competitors",[])
            if len(comp) < 2:
                continue
            ctx        = se.get("sport_event_context",{})
            tournament = ctx.get("competition",{}).get("name","Unknown")
            status     = s.get("sport_event_status",{}).get("status","scheduled")
            games.append({
                "p1": comp[0].get("name","Player 1"),
                "p2": comp[1].get("name","Player 2"),
                "tournament": tournament,
                "round": ctx.get("round",{}).get("name","—"),
                "surface": surface_from_tournament(tournament),
                "status": status,
            })
        return games
    except Exception:
        return []

def surface_from_tournament(t):
    t = t.lower()
    if any(x in t for x in ["clay","monte","roland","barcelona","madrid","rome","hamburg"]):
        return "Clay"
    if any(x in t for x in ["wimbledon","queens","eastbourne","halle","grass"]):
        return "Grass"
    if any(x in t for x in ["indoor","rotterdam","vienna","paris masters","sofia","marseille"]):
        return "Hard (Indoor)"
    return "Hard (Outdoor)"

def status_badge(status):
    if status == "in_progress": return "🔴 LIVE"
    if status == "scheduled":   return "🟡 UPCOMING"
    return "⚪ " + status.replace("_"," ").upper()

def get_live_matches():
    api = fetch_live_tennis()
    if api:
        return api
    return [
        {"p1":"Draper, Jack",           "p2":"Medvedev, Daniil",       "tournament":"ATP Indian Wells Men Singles",        "round":"Quarterfinal","surface":"Hard (Outdoor)","status":"in_progress"},
        {"p1":"Alcaraz, Carlos",        "p2":"Norrie, Cameron",         "tournament":"ATP Indian Wells Men Singles",        "round":"Quarterfinal","surface":"Hard (Outdoor)","status":"scheduled"},
        {"p1":"Bautista Agut, Roberto", "p2":"Royer, Valentin",         "tournament":"ATP Challenger Cap Cana Men Singles", "round":"—",           "surface":"Clay",          "status":"in_progress"},
        {"p1":"Navone, Mariano",        "p2":"Mochizuki, Shintaro",     "tournament":"ATP Challenger Cap Cana Men Singles", "round":"—",           "surface":"Clay",          "status":"in_progress"},
        {"p1":"Moutet, Corentin",       "p2":"Halys, Quentin",          "tournament":"ATP Challenger Phoenix Men Singles",  "round":"—",           "surface":"Hard (Outdoor)","status":"scheduled"},
    ]

# ── MATCH DATA (archive) ──────────────────────────────────────────────────────
MATCHES = {
    "🎾 Draper [15] vs. Medvedev [4] — ATP Indian Wells QF": {
        "p1":"Jack Draper","p1_seed":"#15","p1_odds":"+145","p2":"Daniil Medvedev","p2_seed":"#4","p2_odds":"-175",
        "tournament":"ATP Indian Wells Masters","round":"Quarterfinal","surface":"Hard (Outdoor)","time":"Tonight · Stadium 1",
        "h2h":"Medvedev leads 3-1","recent_p1":"W W W W L","recent_p2":"W W L W W","total":"23.5 games","surface_speed":"Medium-Fast",
        "q1":{"title":"Statistical Profile","icon":"📊","body":"Draper break-point conversion: <strong>47%</strong>. Medvedev first-serve points won: <strong>76%</strong>. H2H: Medvedev 3-1. Draper tiebreak record 2026: <strong>7/9 (77%)</strong>."},
        "q2":{"title":"Environmental Context","icon":"🌵","body":"IW night sessions: <strong>heavy, dense air</strong>. Altitude ~480m reduces serve dominance. Wind: calm. IW plays ~6% slower than tour average."},
        "q3":{"title":"Psychological / Narrative","icon":"🧠","body":"Draper riding <strong>alpha momentum</strong> after beating Djokovic. Defending his 2025 title. Medvedev faded mid-match vs Fils."},
        "q4":{"title":"The Verdict","icon":"🏆","pick":"Draper ML + Over 22.5 Games","confidence":68,"body":"Momentum, tiebreak dominance, heavy night air. Value: <strong>Draper ML (+145)</strong> + optional <strong>Over 22.5</strong>."},
        "sss":{"Stats":62,"Surface":55,"Situation":80},
    },
    "🎾 Pegula [5] vs. Rybakina [6] — WTA Indian Wells R16": {
        "p1":"Jessica Pegula","p1_seed":"#5","p1_odds":"+110","p2":"Elena Rybakina","p2_seed":"#6","p2_odds":"-130",
        "tournament":"WTA Indian Wells Masters","round":"Round of 16","surface":"Hard (Outdoor)","time":"Tonight · Court 2",
        "h2h":"Rybakina leads 4-2","recent_p1":"W W L W W","recent_p2":"W L W W W","total":"19.5 games","surface_speed":"Medium-Fast",
        "q1":{"title":"Statistical Profile","icon":"📊","body":"Rybakina: <strong>68% first serve in</strong>, <strong>92mph</strong> avg 2nd serve. Pegula wins <strong>41%</strong> return games. Rybakina BP save: <strong>71%</strong>."},
        "q2":{"title":"Environmental Context","icon":"🌵","body":"IW evening: <strong>mild (65F)</strong>, low humidity. Favours big servers — <strong>edge Rybakina</strong>. Evening sessions play 4% faster."},
        "q3":{"title":"Psychological / Narrative","icon":"🧠","body":"Pegula with <strong>renewed motivation</strong> post-2025 US Open. Rybakina quietly dominant. Pegula durable in long 3rd sets."},
        "q4":{"title":"The Verdict","icon":"🏆","pick":"Rybakina ML + Under 20.5 Games","confidence":61,"body":"Rybakina serve neutralises Pegula on faster night court. <strong>Rybakina ML (-130)</strong> is the lean."},
        "sss":{"Stats":58,"Surface":70,"Situation":52},
    },
    "🎾 Svitolina def. Swiatek — WTA IW R16 (RESULT)": {
        "p1":"Elina Svitolina","p1_seed":"—","p1_odds":"+280 (pre)","p2":"Iga Swiatek","p2_seed":"#1","p2_odds":"-380 (pre)",
        "tournament":"WTA Indian Wells Masters","round":"R16 — Final: 6-2, 4-6, 6-4","surface":"Hard (Outdoor)","time":"March 12",
        "h2h":"Swiatek led 12-3","recent_p1":"W W L W W","recent_p2":"W W W W L","total":"28 games (actual)","surface_speed":"Medium-Fast",
        "q1":{"title":"Statistical Profile","icon":"📊","body":"Svitolina won <strong>78% first serve pts</strong> — career high vs Swiatek. Swiatek UFE: <strong>41</strong>. Svitolina: <strong>5 breaks</strong>."},
        "q2":{"title":"Environmental Context","icon":"🌵","body":"IW evening favoured <strong>flat hitters</strong>. Svitolina compact groundstrokes thrived. Swiatek topspin lost margin."},
        "q3":{"title":"Psychological / Narrative","icon":"🧠","body":"Svitolina <strong>war mentality</strong> — nothing to lose. Swiatek fatigued after tight R2. Crowd shifted after set 1."},
        "q4":{"title":"The Verdict","icon":"🏆","pick":"— Match Completed —","confidence":0,"body":"Low-prob upset (<strong>+280 ~26%</strong>). Lesson: <strong>rest differential</strong> matters more than H2H at Masters level."},
        "sss":{"Stats":30,"Surface":50,"Situation":65},
    },
}

# ── AI HELPERS ────────────────────────────────────────────────────────────────
def call_claude(prompt):
    api_key = st.secrets.get("ANTHROPIC_API_KEY","")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in Streamlit secrets.")
    system = (
        "You are an elite tennis betting analyst specialising in the SSS Method and Quadrant Research Method. "
        "Respond with ONLY a valid JSON object — no preamble, no markdown fences, no extra text. "
        'Required: {"q1":{"title":"Statistical Profile","icon":"📊","body":"HTML <strong> only"},'
        '"q2":{"title":"Environmental Context","icon":"🌵","body":"HTML <strong> only"},'
        '"q3":{"title":"Psychological / Narrative","icon":"🧠","body":"HTML <strong> only"},'
        '"q4":{"title":"The Verdict","icon":"🏆","pick":"concrete pick","confidence":72,"body":"HTML <strong> only"},'
        '"sss":{"Stats":65,"Surface":70,"Situation":58},"summary":"one sentence"} '
        "Rules: SSS 0-100 integers, confidence 0-100 integer, body ONLY <strong> tags, pick must be concrete."
    )
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
        json={"model":"claude-sonnet-4-20250514","max_tokens":1800,"system":system,
              "messages":[{"role":"user","content":prompt}]},
        timeout=45,
    )
    resp.raise_for_status()
    raw = resp.json()["content"][0]["text"].strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1][4:] if parts[1].startswith("json") else parts[1]
    return json.loads(raw.strip())

def build_prompt(d):
    return (
        "Analyse this tennis match using the SSS Method and Quadrant Research Method:\n"
        "MATCH: " + d["p1"] + " vs " + d["p2"] + "\n"
        "TOURNAMENT: " + d["tournament"] + " — " + d["round"] + "\n"
        "SURFACE: " + d["surface"] + " | Speed: " + d["court_speed"] + " | CONDITIONS: " + d["conditions"] + "\n"
        "P1 — " + d["p1"] + ": Seed/Ranking " + d["p1_seed"] + ", Odds " + d["p1_odds"]
        + ", Form (last 5) " + d["p1_form"] + ", Strengths: " + d["p1_strength"] + "\n"
        "P2 — " + d["p2"] + ": Seed/Ranking " + d["p2_seed"] + ", Odds " + d["p2_odds"]
        + ", Form (last 5) " + d["p2_form"] + ", Strengths: " + d["p2_strength"] + "\n"
        "H2H: " + d["h2h"] + " | Total Line: " + d["total_line"] + "\n"
        "Generate a full SSS/Quadrant breakdown and concrete betting verdict."
    )

# ── RENDER HELPERS ────────────────────────────────────────────────────────────
def form_badges(form_str):
    return "".join(
        '<span style="color:' + ("#10B981" if r.upper()=="W" else "#EF4444") + ';font-weight:700;font-size:0.9rem;margin-right:3px;">' + r.upper() + "</span>"
        for r in str(form_str).strip().split() if r.upper() in ("W","L")
    )

def render_match_header(p1, p2, tournament, round_, surface, time_):
    st.markdown(
        '<div class="match-card"><div class="match-title">' + p1 + ' vs. ' + p2 + '</div>'
        '<div class="match-meta">🏆 ' + tournament + ' &nbsp;·&nbsp; ' + round_ + ' &nbsp;·&nbsp; 🎾 ' + surface + ' &nbsp;·&nbsp; 🕐 ' + time_ + '</div></div>',
        unsafe_allow_html=True
    )

def render_players(p1, p1_seed, p1_odds, p1_form, p2, p2_seed, p2_odds, p2_form):
    ca,cb,cc = st.columns([3,2,1])
    with ca: st.markdown("**" + p1 + "** &nbsp; `" + str(p1_seed) + "`", unsafe_allow_html=True)
    with cb: st.markdown("Form: " + form_badges(p1_form), unsafe_allow_html=True)
    with cc: st.markdown('<span style="background:#0d9268;color:#fff;padding:3px 10px;border-radius:6px;font-family:monospace;font-weight:700;">' + str(p1_odds) + '</span>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#475569;font-family:monospace;font-size:0.75rem;letter-spacing:3px;margin:4px 0;">— VS —</p>', unsafe_allow_html=True)
    ca2,cb2,cc2 = st.columns([3,2,1])
    with ca2: st.markdown("**" + p2 + "** &nbsp; `" + str(p2_seed) + "`", unsafe_allow_html=True)
    with cb2: st.markdown("Form: " + form_badges(p2_form), unsafe_allow_html=True)
    with cc2: st.markdown('<span style="background:#0d9268;color:#fff;padding:3px 10px;border-radius:6px;font-family:monospace;font-weight:700;">' + str(p2_odds) + '</span>', unsafe_allow_html=True)

def render_sss(sss):
    st.markdown('<div class="section-label">SSS SCORE BREAKDOWN</div>', unsafe_allow_html=True)
    for key, val in sss.items():
        c1,c2,c3 = st.columns([1,6,0.5])
        with c1: st.markdown('<span style="font-family:monospace;font-size:0.8rem;color:#10B981;">' + key + '</span>', unsafe_allow_html=True)
        with c2: st.progress(min(int(val),100)/100)
        with c3: st.markdown('<span style="font-family:monospace;font-size:0.8rem;color:#94A3B8;">' + str(val) + '</span>', unsafe_allow_html=True)
    avg = sum(min(int(v),100) for v in sss.values())//3
    st.markdown('<p style="font-family:monospace;font-size:0.8rem;color:#64748B;margin-top:4px;">SSS COMPOSITE: <span style="color:#10B981;font-weight:700;">' + str(avg) + '/100</span></p>', unsafe_allow_html=True)

def render_quads(match):
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">QUADRANT BREAKDOWN</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    for col,qk in zip([c1,c2,c3],["q1","q2","q3"]):
        q = match[qk]
        with col:
            st.markdown(
                '<div class="quad-card"><div class="quad-header">'
                '<span class="quad-icon">' + q["icon"] + '</span>'
                '<span class="quad-title">' + q["title"] + '</span>'
                '</div><div class="quad-body">' + q["body"] + '</div></div>',
                unsafe_allow_html=True
            )
    q4   = match["q4"]
    conf = int(q4.get("confidence",0))
    if conf > 0:
        cc = "#10B981" if conf>=65 else "#F59E0B" if conf>=50 else "#EF4444"
        cl = "HIGH" if conf>=65 else "MODERATE" if conf>=50 else "LOW"
        st.markdown(
            '<div class="verdict-banner"><div>'
            '<div class="verdict-label">🏆 Q4 — The Verdict</div>'
            '<div class="verdict-pick">' + q4["pick"] + '</div>'
            '<div style="font-size:0.85rem;color:#94A3B8;margin-top:0.5rem;max-width:500px;line-height:1.6;">' + q4["body"] + '</div>'
            '</div><div style="text-align:center;">'
            '<div class="confidence-num" style="color:' + cc + ';">' + str(conf) + '%</div>'
            '<div class="confidence-tag">Confidence</div>'
            '<div style="font-size:0.68rem;color:' + cc + ';letter-spacing:2px;margin-top:3px;">' + cl + '</div>'
            '</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="verdict-banner"><div>'
            '<div class="verdict-label">🏆 Q4 — Post-Match Analysis</div>'
            '<div class="verdict-pick" style="color:#94A3B8;">— Match Completed —</div>'
            '<div style="font-size:0.85rem;color:#94A3B8;margin-top:0.5rem;max-width:580px;line-height:1.6;">' + q4["body"] + '</div>'
            '</div></div>',
            unsafe_allow_html=True
        )

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:0.5rem 0 1.5rem;'><div style='font-size:2.4rem;margin-bottom:6px;'>🎾</div><div style='font-family:\"Space Mono\",monospace;font-size:1.1rem;color:#10B981;font-weight:700;'>SSS/QUAD TOOL</div><div style='font-size:0.68rem;color:#64748B;letter-spacing:2px;text-transform:uppercase;margin-top:2px;'>Tennis Betting Intelligence</div></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">📐 Methodology</div>', unsafe_allow_html=True)
    for icon,label,desc in [
        ("📊","S1 — Stats","H2H records, win/loss trends, serve & return efficiency, break-point conversion, tiebreak records."),
        ("🌡️","S2 — Surface","Court speed rating, bounce height, environmental factors including humidity, wind, altitude."),
        ("🧠","S3 — Situation","Fatigue signals, rest differential, psychological Alpha status, crowd dynamics, tournament context."),
    ]:
        st.markdown('<div class="method-card"><div class="method-title">' + icon + ' ' + label + '</div><div class="method-desc">' + desc + '</div></div>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔲 Quadrant Method</div>', unsafe_allow_html=True)
    for icon,label,desc in [
        ("📊","Q1 — Statistical Profile","Hard data: break-point conversion, seasonal metrics, serve stats, H2H records."),
        ("🌵","Q2 — Environmental Context","Court physics, weather, altitude — how they bias outcomes toward playing styles."),
        ("🧠","Q3 — Psychological / Narrative","Motivations, revenge arcs, momentum, confidence levels, crowd dynamics."),
        ("🏆","Q4 — The Verdict","Synthesis into a final pick, reasoning, and confidence rating (0-100%)."),
    ]:
        st.markdown('<div class="method-card"><div class="method-title">' + icon + ' ' + label + '</div><div class="method-desc">' + desc + '</div></div>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:#475569;text-align:center;line-height:1.6;">For educational purposes only.<br>Gamble responsibly. 18+.</div>', unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="brand-header"><div style="font-size:2rem;">🎾</div><div><div class="brand-title">SSS / QUAD TOOL</div><div class="brand-sub">Tennis Betting Intelligence · Powered by AI</div></div></div>', unsafe_allow_html=True)

tab_archive, tab_ai, tab_log = st.tabs(["📁  Match Archive", "🤖  AI Quad Generator", "📊  Results Log"])

# ════════════════════════════════════════════════════════════
# TAB 1 — ARCHIVE
# ════════════════════════════════════════════════════════════
with tab_archive:
    st.markdown('<div class="section-label" style="margin-top:1rem;">SELECT MATCH</div>', unsafe_allow_html=True)
    selected = st.selectbox("match", options=list(MATCHES.keys()), label_visibility="collapsed")
    match = MATCHES[selected]
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    render_match_header(match["p1"],match["p2"],match["tournament"],match["round"],match["surface"],match["time"])
    render_players(match["p1"],match["p1_seed"],match["p1_odds"],match["recent_p1"],match["p2"],match["p2_seed"],match["p2_odds"],match["recent_p2"])
    st.markdown("<br>", unsafe_allow_html=True)
    cs1,cs2,cs3 = st.columns(3)
    with cs1: st.metric("H2H", match["h2h"])
    with cs2: st.metric("Total Line", match["total"])
    with cs3: st.metric("Court Speed", match["surface_speed"])
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    render_sss(match["sss"])
    render_quads(match)
    st.markdown('<div style="text-align:center;margin-top:3rem;font-size:0.68rem;color:#334155;letter-spacing:1.5px;text-transform:uppercase;">SSS/Quad Tool · For analytical purposes only · Always gamble responsibly</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 2 — AI QUAD GENERATOR
# ════════════════════════════════════════════════════════════
with tab_ai:
    st.markdown('<div class="section-label" style="margin-top:1rem;">AI-Powered Match Analysis</div>', unsafe_allow_html=True)

    input_mode = st.radio(
        "Input mode", ["🔴  Live & Upcoming Matches", "✏️  Manual Entry"],
        horizontal=True, label_visibility="collapsed", key="input_mode",
    )
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Defaults
    pre = {"p1_name":"","p2_name":"","tournament":"","round":"—","surface":"Hard (Outdoor)",
           "p1_seed":"—","p2_seed":"—","p1_odds":"—","p2_odds":"—",
           "p1_form":"—","p2_form":"—","p1_strength":"","p2_strength":""}

    # ══ LIVE MODE ════════════════════════════════════════════
    if input_mode == "🔴  Live & Upcoming Matches":
        st.markdown('<div class="section-label">Select a Match</div>', unsafe_allow_html=True)
        live_matches = get_live_matches()

        if not live_matches:
            st.warning("No live or upcoming matches found. Switch to Manual Entry.")
        else:
            labels = []
            for m in live_matches:
                labels.append(status_badge(m["status"]) + "  " + m["p1"] + " vs " + m["p2"] + "  ·  " + m["tournament"])

            chosen_label = st.selectbox("live_match_select", labels, label_visibility="collapsed", key="live_match_sel")
            chosen_idx   = labels.index(chosen_label)
            chosen       = live_matches[chosen_idx]

            st.markdown(
                '<div class="match-card" style="margin-top:0.8rem;">'
                '<div class="match-title">' + chosen["p1"] + ' vs. ' + chosen["p2"] + '</div>'
                '<div class="match-meta">🏆 ' + chosen["tournament"] + ' &nbsp;·&nbsp; ' + chosen["round"] + ' &nbsp;·&nbsp; 🎾 ' + chosen["surface"] + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

            # ── Sportsbook selector & odds fetch ──
            st.markdown('<div class="form-section-title">📚 Sportsbook & Odds</div>', unsafe_allow_html=True)

            odds_data     = fetch_tennis_odds()
            avail_books   = get_available_books(odds_data, chosen["p1"], chosen["p2"])
            book_labels   = [label for _,label in avail_books] if avail_books else [l for k,l in BOOK_LABELS.items() if k in PREFERRED_BOOKS]
            book_keys     = [key for key,_ in avail_books] if avail_books else [k for k in PREFERRED_BOOKS]

            if not avail_books:
                st.markdown('<p style="color:#F59E0B;font-size:0.82rem;margin-bottom:0.5rem;">⚠️ No odds found for this match yet — enter manually below or try another match.</p>', unsafe_allow_html=True)

            bk1, bk2 = st.columns([2,3])
            with bk1:
                selected_book_label = st.selectbox("Sportsbook", book_labels, key="book_sel")
                selected_book_key   = book_keys[book_labels.index(selected_book_label)] if book_labels else "bet365"

            p1_dec, p2_dec, book_used = extract_odds_for_match(odds_data, chosen["p1"], chosen["p2"], selected_book_key)
            p1_american = decimal_to_american(p1_dec) if p1_dec else "—"
            p2_american = decimal_to_american(p2_dec) if p2_dec else "—"

            with bk2:
                if p1_dec and p2_dec:
                    st.markdown(
                        '<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:8px;padding:0.6rem 1rem;margin-top:1.6rem;">'
                        '<span style="font-family:monospace;font-size:0.75rem;color:#10B981;letter-spacing:1px;">LIVE ODDS FROM ' + selected_book_label.upper() + '</span><br>'
                        '<span style="font-family:monospace;font-size:0.9rem;color:#E2E8F0;">' + chosen["p1"].split(",")[0] + ': <strong>' + p1_american + '</strong> &nbsp;|&nbsp; ' + chosen["p2"].split(",")[0] + ': <strong>' + p2_american + '</strong></span>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div style="padding:0.6rem 0;font-size:0.82rem;color:#94A3B8;">Enter odds manually in the fields below.</div>', unsafe_allow_html=True)

            # ── Fetch player stats ──
            st.markdown('<div class="form-section-title">👤 Player Stats</div>', unsafe_allow_html=True)
            stats_col1, stats_col2 = st.columns(2)

            with stats_col1:
                with st.spinner("Fetching " + chosen["p1"].split(",")[0] + " stats..."):
                    p1_stats = fetch_player_stats(chosen["p1"])
                    p1_form_api = fetch_player_recent_form(chosen["p1"])

            with stats_col2:
                with st.spinner("Fetching " + chosen["p2"].split(",")[0] + " stats..."):
                    p2_stats = fetch_player_stats(chosen["p2"])
                    p2_form_api = fetch_player_recent_form(chosen["p2"])

            pre.update({
                "p1_name":    chosen["p1"],
                "p2_name":    chosen["p2"],
                "tournament": chosen["tournament"],
                "round":      chosen["round"],
                "surface":    chosen["surface"],
                "p1_seed":    p1_stats.get("ranking","—"),
                "p2_seed":    p2_stats.get("ranking","—"),
                "p1_odds":    p1_american,
                "p2_odds":    p2_american,
                "p1_form":    p1_form_api if p1_form_api and p1_form_api != "—" else "—",
                "p2_form":    p2_form_api if p2_form_api and p2_form_api != "—" else "—",
                "p1_strength": (p1_stats.get("hand","") + " handed" if p1_stats.get("hand") else ""),
                "p2_strength": (p2_stats.get("hand","") + " handed" if p2_stats.get("hand") else ""),
            })

            st.markdown('<div class="auto-fill-badge">⚡ Auto-filled — edit as needed</div>', unsafe_allow_html=True)

    # ══ FORM (shared between both modes) ═════════════════════
    if input_mode == "✏️  Manual Entry":
        st.markdown('<div class="form-section-title">⚔️ Players</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="form-section-title">⚔️ Players & Details</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        p1_name     = st.text_input("Player 1 Name",     value=pre["p1_name"],    placeholder="e.g. Jack Draper",         key="p1n")
        p1_seed     = st.text_input("P1 Ranking",        value=pre["p1_seed"],    placeholder="e.g. #15",                 key="p1s")
        p1_odds     = st.text_input("P1 Odds",           value=pre["p1_odds"],    placeholder="e.g. +145",                key="p1o")
        p1_form     = st.text_input("P1 Last 5 Results", value=pre["p1_form"],    placeholder="W W L W W",                key="p1f")
        p1_strength = st.text_input("P1 Key Strengths",  value=pre["p1_strength"],placeholder="e.g. Big serve, tiebreaks",key="p1st")
    with fc2:
        p2_name     = st.text_input("Player 2 Name",     value=pre["p2_name"],    placeholder="e.g. Daniil Medvedev",     key="p2n")
        p2_seed     = st.text_input("P2 Ranking",        value=pre["p2_seed"],    placeholder="e.g. #4",                  key="p2s")
        p2_odds     = st.text_input("P2 Odds",           value=pre["p2_odds"],    placeholder="e.g. -175",                key="p2o")
        p2_form     = st.text_input("P2 Last 5 Results", value=pre["p2_form"],    placeholder="W W W L W",                key="p2f")
        p2_strength = st.text_input("P2 Key Strengths",  value=pre["p2_strength"],placeholder="e.g. Baseline, return",   key="p2st")

    st.markdown('<div class="form-section-title">🏟️ Match Context</div>', unsafe_allow_html=True)
    mc1, mc2, mc3 = st.columns(3)
    surf_opts   = ["Hard (Outdoor)","Hard (Indoor)","Clay","Grass"]
    surf_idx    = surf_opts.index(pre["surface"]) if pre["surface"] in surf_opts else 0
    with mc1:
        tournament = st.text_input("Tournament", value=pre["tournament"], placeholder="e.g. ATP Indian Wells", key="tourn")
        round_     = st.text_input("Round",      value=pre["round"],      placeholder="e.g. Quarterfinal",     key="rnd")
    with mc2:
        surface     = st.selectbox("Surface",     surf_opts, index=surf_idx, key="surf")
        court_speed = st.selectbox("Court Speed", ["Slow","Medium-Slow","Medium","Medium-Fast","Fast"], key="spd")
    with mc3:
        h2h        = st.text_input("H2H Record",       value="", placeholder="e.g. Medvedev leads 3-1", key="h2h")
        total_line = st.text_input("Games Total Line", value="", placeholder="e.g. 22.5",                key="tot")
    conditions = st.text_input("Conditions / Extra Notes", value="", placeholder="e.g. Night session, heavy air, crowd factor...", key="cond")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🤖  Generate AI Analysis"):
        if not p1_name or not p2_name:
            st.error("Please enter both player names before generating.")
        else:
            form_data = {
                "p1": p1_name,  "p1_seed": p1_seed or "—",  "p1_odds": p1_odds or "—",
                "p1_form": p1_form or "—",  "p1_strength": p1_strength or "—",
                "p2": p2_name,  "p2_seed": p2_seed or "—",  "p2_odds": p2_odds or "—",
                "p2_form": p2_form or "—",  "p2_strength": p2_strength or "—",
                "tournament": tournament or "Unknown",  "round": round_ or "—",
                "surface": surface,  "court_speed": court_speed,
                "h2h": h2h or "No H2H data",  "total_line": total_line or "—",
                "conditions": conditions or "Standard conditions",
            }
            with st.spinner("🤖 Claude is generating your analysis..."):
                try:
                    result = call_claude(build_prompt(form_data))
                    st.session_state["ai_result"] = result
                    st.session_state["ai_form"]   = form_data
                    st.session_state.pop("pick_logged", None)
                except requests.exceptions.HTTPError as e:
                    st.error("API error " + str(e.response.status_code) + ": " + e.response.text[:300])
                    st.session_state.pop("ai_result", None)
                except Exception as e:
                    st.error("Error: " + str(e))
                    st.session_state.pop("ai_result", None)

    # ── AI Result Display ─────────────────────────────────────
    if "ai_result" in st.session_state and "ai_form" in st.session_state:
        result = st.session_state["ai_result"]
        fd     = st.session_state["ai_form"]

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">AI-Generated Analysis</div>', unsafe_allow_html=True)
        if result.get("summary"):
            st.markdown('<p style="color:#94A3B8;font-size:0.88rem;font-style:italic;margin-bottom:1rem;">💬 ' + result["summary"] + '</p>', unsafe_allow_html=True)

        render_match_header(fd["p1"],fd["p2"],fd["tournament"],fd["round"],fd["surface"],fd["court_speed"] + " court")
        render_players(fd["p1"],fd["p1_seed"],fd["p1_odds"],fd["p1_form"],fd["p2"],fd["p2_seed"],fd["p2_odds"],fd["p2_form"])
        st.markdown("<br>", unsafe_allow_html=True)
        as1,as2,as3 = st.columns(3)
        with as1: st.metric("H2H", fd["h2h"])
        with as2: st.metric("Total Line", fd["total_line"])
        with as3: st.metric("Surface", fd["surface"])
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        render_sss(result["sss"])
        render_quads(result)

        # ── Log This Pick ─────────────────────────────────────
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">📋 Log This Pick</div>', unsafe_allow_html=True)
        lc1,lc2,lc3 = st.columns(3)
        with lc1:
            log_pick  = st.text_input("Pick",  value=result["q4"].get("pick",""), key="log_pick")
            log_odds  = st.text_input("Odds",  value=fd.get("p1_odds",""),        key="log_odds")
        with lc2:
            log_stake  = st.number_input("Stake (units)", min_value=0.5, max_value=100.0, value=1.0, step=0.5, key="log_stake")
            log_method = st.selectbox("Methodology", ["Quad","SSS","SSS + Quad"], key="log_method")
        with lc3:
            log_notes = st.text_input("Notes (optional)", placeholder="e.g. High confidence, night session", key="log_notes")

        if st.session_state.get("pick_logged"):
            st.success("✅ Pick logged! View it in the Results Log tab.")
        else:
            if st.button("📋  Log Pick to Results"):
                try:
                    df_existing = load_csv_from_github()
                    new_row = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Match": fd["p1"] + " vs " + fd["p2"],
                        "Tournament": fd["tournament"], "Surface": fd["surface"],
                        "Pick": log_pick, "Odds": log_odds,
                        "Stake (units)": log_stake,
                        "Confidence %": result["q4"].get("confidence",""),
                        "Methodology": log_method, "Result": "PENDING",
                        "P&L (units)": "", "Notes": log_notes,
                    }
                    df_new = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
                    save_csv_to_github(df_new, "Log: " + fd["p1"] + " vs " + fd["p2"])
                    st.session_state["pick_logged"] = True
                    st.rerun()
                except Exception as e:
                    st.error("Failed to log pick: " + str(e))

        st.markdown('<div style="text-align:center;margin-top:3rem;font-size:0.68rem;color:#334155;letter-spacing:1.5px;text-transform:uppercase;">AI analysis by Claude · Educational purposes only · Gamble responsibly</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 3 — RESULTS LOG
# ════════════════════════════════════════════════════════════
with tab_log:
    st.markdown('<div class="section-label" style="margin-top:1rem;">Results Log & Performance Tracker</div>', unsafe_allow_html=True)

    try:
        df = load_csv_from_github()
    except Exception as e:
        st.error("Could not load results: " + str(e))
        st.info("Make sure GITHUB_TOKEN and GITHUB_REPO are set in your Streamlit secrets.")
        st.stop()

    if df.empty:
        st.markdown('<div style="text-align:center;padding:4rem;color:#475569;"><div style="font-size:3rem;margin-bottom:1rem;">📋</div><div style="font-family:monospace;font-size:0.85rem;letter-spacing:2px;">NO PICKS LOGGED YET</div><div style="font-size:0.8rem;margin-top:0.5rem;">Generate an AI analysis and log your first pick.</div></div>', unsafe_allow_html=True)
    else:
        settled   = df[df["Result"].isin(["WIN","LOSS"])]
        wins      = len(settled[settled["Result"]=="WIN"])
        losses    = len(settled[settled["Result"]=="LOSS"])
        total     = len(settled)
        strike    = str(round(wins/total*100)) + "%" if total>0 else "—"
        pnl_sum   = float(settled["P&L (units)"].sum()) if total>0 else 0.0
        pending   = len(df[df["Result"]=="PENDING"])
        stake_sum = float(settled["Stake (units)"].sum()) if total>0 else 0
        roi       = str(round(pnl_sum/stake_sum*100,1)) + "%" if stake_sum>0 else "—"

        st.markdown('<div class="section-label">Performance Summary</div>', unsafe_allow_html=True)
        sc1,sc2,sc3,sc4,sc5,sc6 = st.columns(6)
        for col,val,label,color in [
            (sc1, total,  "Settled",    "#E2E8F0"),
            (sc2, wins,   "Wins",       "#10B981"),
            (sc3, losses, "Losses",     "#EF4444"),
            (sc4, strike, "Strike Rate","#10B981" if total>0 and wins/total>=0.5 else "#F59E0B"),
            (sc5, ("+" if pnl_sum>=0 else "")+str(round(pnl_sum,2))+"u", "Total P&L", "#10B981" if pnl_sum>=0 else "#EF4444"),
            (sc6, roi,    "ROI",        "#10B981" if roi!="—" and not roi.startswith("-") else "#EF4444"),
        ]:
            with col:
                st.markdown('<div class="stat-card"><div class="stat-card-value" style="color:' + color + ';">' + str(val) + '</div><div class="stat-card-label">' + label + '</div></div>', unsafe_allow_html=True)

        if pending > 0:
            st.markdown('<p style="color:#F59E0B;font-family:monospace;font-size:0.75rem;margin-top:0.8rem;letter-spacing:1px;">⏳ ' + str(pending) + ' PENDING RESULT' + ('S' if pending>1 else '') + '</p>', unsafe_allow_html=True)

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">All Picks — Click any cell to edit</div>', unsafe_allow_html=True)

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "Date":          st.column_config.TextColumn("Date",       disabled=True),
                "Match":         st.column_config.TextColumn("Match",      disabled=True),
                "Tournament":    st.column_config.TextColumn("Tournament", disabled=True),
                "Surface":       st.column_config.TextColumn("Surface",    disabled=True),
                "Pick":          st.column_config.TextColumn("Pick",       disabled=True),
                "Odds":          st.column_config.TextColumn("Odds"),
                "Stake (units)": st.column_config.NumberColumn("Stake",    format="%.1f", min_value=0),
                "Confidence %":  st.column_config.NumberColumn("Conf %",   format="%d",   min_value=0, max_value=100),
                "Methodology":   st.column_config.SelectboxColumn("Method",options=["Quad","SSS","SSS + Quad"]),
                "Result":        st.column_config.SelectboxColumn("Result",options=["PENDING","WIN","LOSS"]),
                "P&L (units)":   st.column_config.NumberColumn("P&L",     format="%.2f"),
                "Notes":         st.column_config.TextColumn("Notes"),
            },
            key="results_editor",
        )

        for i, row in edited_df.iterrows():
            if row["Result"] in ("WIN","LOSS") and (pd.isna(row["P&L (units)"]) or row["P&L (units)"] == 0):
                edited_df.at[i,"P&L (units)"] = calc_pnl(str(row["Odds"]), float(row["Stake (units)"] or 1), row["Result"])

        if st.button("💾  Save Changes to GitHub"):
            try:
                save_csv_to_github(edited_df, "Update results via app editor")
                st.success("✅ Saved to GitHub!")
                st.rerun()
            except Exception as e:
                st.error("Save failed: " + str(e))

        st.markdown('<div style="text-align:center;margin-top:3rem;font-size:0.68rem;color:#334155;letter-spacing:1.5px;text-transform:uppercase;">Results saved to GitHub · Gamble responsibly</div>', unsafe_allow_html=True)
