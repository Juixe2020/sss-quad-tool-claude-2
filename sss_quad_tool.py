import streamlit as st
import json
import requests

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="SSS/Quad Tool | Tennis Betting Dashboard",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CUSTOM THEME / CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0B1215;
    --bg-sec:    #1E293B;
    --accent:    #10B981;
    --accent-dim:#0d9268;
    --slate:     #334155;
    --text:      #E2E8F0;
    --muted:     #94A3B8;
    --border:    rgba(16,185,129,0.18);
    --glow:      0 0 24px rgba(16,185,129,0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] {
    background-color: var(--bg-sec) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px; }
#MainMenu, footer, header { visibility: hidden; }

.brand-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1.25rem;
}
.brand-title {
    font-family: 'Space Mono', monospace; font-size: 1.55rem;
    font-weight: 700; color: var(--accent); letter-spacing: -0.5px;
}
.brand-sub { font-size: 0.75rem; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; }

.section-label {
    font-family: 'Space Mono', monospace; font-size: 0.68rem;
    letter-spacing: 3px; text-transform: uppercase; color: var(--accent); margin-bottom: 0.6rem;
}
.match-card {
    background: var(--slate); border: 1px solid var(--border); border-radius: 14px;
    padding: 1.4rem 1.8rem; box-shadow: var(--glow); margin-bottom: 1rem;
    position: relative; overflow: hidden;
}
.match-card::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%; background: var(--accent); border-radius: 4px 0 0 4px;
}
.match-title { font-family: 'Space Mono', monospace; font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 0.2rem; }
.match-meta { font-size: 0.82rem; color: var(--muted); letter-spacing: 0.5px; }

.quad-card {
    background: var(--bg-sec); border: 1px solid var(--border); border-radius: 12px;
    padding: 1.2rem 1.3rem; height: 100%; box-shadow: var(--glow);
}
.quad-card:hover { border-color: var(--accent); }
.quad-header { display: flex; align-items: center; gap: 8px; margin-bottom: 0.65rem; }
.quad-icon { font-size: 1.2rem; }
.quad-title { font-family: 'Space Mono', monospace; font-size: 0.75rem; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent); }
.quad-body { font-size: 0.86rem; color: var(--muted); line-height: 1.65; }
.quad-body strong { color: var(--text); }

.verdict-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(16,185,129,0.04));
    border: 1px solid var(--accent); border-radius: 12px;
    padding: 1.3rem 1.6rem; margin-top: 1.2rem;
    display: flex; justify-content: space-between; align-items: center;
}
.verdict-label { font-family: 'Space Mono', monospace; font-size: 0.68rem; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
.verdict-pick { font-family: 'Space Mono', monospace; font-size: 1.3rem; font-weight: 700; color: var(--accent); }
.confidence-num { font-family: 'Space Mono', monospace; font-size: 2.1rem; font-weight: 700; line-height: 1; }
.confidence-tag { font-size: 0.7rem; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-top: 3px; }

.method-card {
    background: rgba(16,185,129,0.05); border: 1px solid var(--border);
    border-radius: 10px; padding: 0.9rem 1rem; margin-bottom: 0.7rem;
}
.method-title { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--accent); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.4rem; }
.method-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.55; }

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background-color: #0f1923 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border);
    gap: 4px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

[data-testid="stButton"] button {
    background: linear-gradient(135deg, var(--accent-dim), var(--accent)) !important;
    color: #fff !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; border: none !important;
    border-radius: 8px !important; padding: 0.6rem 1.6rem !important;
    font-weight: 700 !important; width: 100% !important;
}
[data-testid="stButton"] button:hover { opacity: 0.88 !important; }

[data-testid="stSelectbox"] > div > div {
    background-color: var(--bg-sec) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

.custom-divider { border: none; border-top: 1px solid var(--border); margin: 1.4rem 0; }

.form-section-title {
    font-family: 'Space Mono', monospace; font-size: 0.72rem;
    letter-spacing: 2.5px; text-transform: uppercase; color: var(--accent);
    margin-bottom: 0.8rem; margin-top: 1rem;
    padding-bottom: 0.4rem; border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MATCH DATA (Archive)
# ─────────────────────────────────────────
MATCHES = {
    "🎾 Draper [15] vs. Medvedev [4] — ATP Indian Wells QF": {
        "p1": "Jack Draper", "p1_seed": "#15", "p1_odds": "+145",
        "p2": "Daniil Medvedev", "p2_seed": "#4", "p2_odds": "-175",
        "tournament": "ATP Indian Wells Masters", "round": "Quarterfinal",
        "surface": "Hard (Outdoor)", "time": "Tonight · Stadium 1",
        "h2h": "Medvedev leads 3–1", "recent_p1": "W W W W L", "recent_p2": "W W L W W",
        "total": "23.5 games", "surface_speed": "Medium-Fast",
        "q1": {"title": "Statistical Profile", "icon": "📊",
               "body": "Draper's break-point conversion sits at <strong>47%</strong> this hard-court swing — elite for his age bracket. Medvedev's first-serve points won: <strong>76%</strong> on hard courts in 2026, the highest on tour. H2H: Medvedev 3–1, but Draper's lone win came at an indoor Masters. Draper's tiebreak record in 2026: <strong>7/9 (77%)</strong>."},
        "q2": {"title": "Environmental Context", "icon": "🌵",
               "body": "Indian Wells night sessions carry <strong>heavy, dense air</strong> — ball travels slower, rallies extend. This benefits baseline counterpunchers. Medvedev thrives in these conditions historically. Altitude ~480m mildly reducing serve dominance. Wind forecast: calm (< 5mph). Court speed: IW plays ~6% slower than tour average."},
        "q3": {"title": "Psychological / Narrative", "icon": "🧠",
               "body": "Draper is riding <strong>alpha status momentum</strong> — just took out World No.1 Djokovic. He's defending his 2025 title, adding emotional fuel. Medvedev struggled with a mid-match fade vs. Fils in R16. Draper's crowd support is massive in California."},
        "q4": {"title": "The Verdict", "icon": "🏆",
               "pick": "Draper ML + Over 22.5 Games", "confidence": 68,
               "body": "Draper's momentum, tiebreak dominance, and heavy night conditions tip this in his favour. Medvedev's serve will be suppressed. Value play: <strong>Draper ML (+145)</strong> with optional cover on <strong>Over 22.5</strong>."},
        "sss": {"Stats": 62, "Surface": 55, "Situation": 80},
    },
    "🎾 Pegula [5] vs. Rybakina [6] — WTA Indian Wells R16": {
        "p1": "Jessica Pegula", "p1_seed": "#5", "p1_odds": "+110",
        "p2": "Elena Rybakina", "p2_seed": "#6", "p2_odds": "-130",
        "tournament": "WTA Indian Wells Masters", "round": "Round of 16",
        "surface": "Hard (Outdoor)", "time": "Tonight · Court 2",
        "h2h": "Rybakina leads 4–2", "recent_p1": "W W L W W", "recent_p2": "W L W W W",
        "total": "19.5 games", "surface_speed": "Medium-Fast",
        "q1": {"title": "Statistical Profile", "icon": "📊",
               "body": "Rybakina's serve: <strong>68% first-serve in</strong>, <strong>92mph average</strong> second serve. Pegula wins <strong>41%</strong> of return games — top-5 WTA. Rybakina's break-point save rate: <strong>71%</strong> in 2026."},
        "q2": {"title": "Environmental Context", "icon": "🌵",
               "body": "IW evening conditions: <strong>mild (65°F)</strong>, low humidity. Ball conditions favour big servers — <strong>slight edge to Rybakina</strong>. Evening sessions historically play 4% faster."},
        "q3": {"title": "Psychological / Narrative", "icon": "🧠",
               "body": "Pegula enters with <strong>renewed motivation</strong> post-2025 US Open run. Rybakina quietly dominant. Pegula known for durability in long third sets. Rybakina high variance on big points."},
        "q4": {"title": "The Verdict", "icon": "🏆",
               "pick": "Rybakina ML + Under 20.5 Games", "confidence": 61,
               "body": "Rybakina's serve neutralises Pegula's return prowess on a faster IW night court. Under is value when her serve clicks. <strong>Rybakina ML (-130)</strong> is the lean."},
        "sss": {"Stats": 58, "Surface": 70, "Situation": 52},
    },
    "🎾 Svitolina def. Swiatek — WTA IW R16 (RESULT ✅)": {
        "p1": "Elina Svitolina", "p1_seed": "—", "p1_odds": "+280 (pre)",
        "p2": "Iga Swiatek", "p2_seed": "#1", "p2_odds": "-380 (pre)",
        "tournament": "WTA Indian Wells Masters", "round": "R16 — Final: 6-2, 4-6, 6-4",
        "surface": "Hard (Outdoor)", "time": "March 12 · Completed",
        "h2h": "Swiatek led 12–3", "recent_p1": "W W L W W", "recent_p2": "W W W W L",
        "total": "28 games (actual)", "surface_speed": "Medium-Fast",
        "q1": {"title": "Statistical Profile", "icon": "📊",
               "body": "Svitolina won <strong>78% of first-serve points</strong> — career high vs Swiatek. Swiatek unforced errors: <strong>41</strong> — highest at IW in 3 years. Svitolina made <strong>5 breaks</strong>."},
        "q2": {"title": "Environmental Context", "icon": "🌵",
               "body": "IW evening air favoured <strong>flatter hitters</strong> — Svitolina's compact groundstrokes thrived. Swiatek's heavy topspin lost margin. Surface speed contributed to Svitolina's flat strategy."},
        "q3": {"title": "Psychological / Narrative", "icon": "🧠",
               "body": "Svitolina's <strong>war mentality</strong> — competing with nothing to lose. Swiatek appeared fatigued after a tight R2. Crowd energy shifted dramatically after the first set."},
        "q4": {"title": "The Verdict", "icon": "🏆",
               "pick": "— Match Completed —", "confidence": 0,
               "body": "Low-probability upset (<strong>+280 implied ~26%</strong>). Key lesson: <strong>rest differential</strong> in back-to-back days matters more than H2H at Masters level."},
        "sss": {"Stats": 30, "Surface": 50, "Situation": 65},
    },
}

# ─────────────────────────────────────────
# AI QUAD GENERATOR
# ─────────────────────────────────────────
def call_claude(prompt: str) -> dict:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in Streamlit secrets. Please add it in your app settings.")

    system = """You are an elite tennis betting analyst specialising in the SSS Method and Quadrant Research Method.

Respond with ONLY a valid JSON object — no preamble, no markdown fences, no extra text.

Required structure:
{
  "q1": { "title": "Statistical Profile", "icon": "📊", "body": "HTML with <strong> tags" },
  "q2": { "title": "Environmental Context", "icon": "🌵", "body": "HTML with <strong> tags" },
  "q3": { "title": "Psychological / Narrative", "icon": "🧠", "body": "HTML with <strong> tags" },
  "q4": { "title": "The Verdict", "icon": "🏆", "pick": "Concrete pick string", "confidence": 72, "body": "HTML with <strong> tags" },
  "sss": { "Stats": 65, "Surface": 70, "Situation": 58 },
  "summary": "One sentence match summary"
}

Rules:
- SSS scores are integers 0-100 representing how much each factor favours the recommended pick
- Confidence is an integer 0-100
- Body fields use ONLY <strong> tags — no other HTML
- Be specific, analytical, and data-driven
- Pick must be concrete: e.g. Player X ML, Over/Under games, or both"""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1800,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        json=payload,
        timeout=45,
    )
    resp.raise_for_status()
    raw = resp.json()["content"][0]["text"].strip()

    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else parts[0]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)


def build_prompt(d: dict) -> str:
    return f"""Analyse this tennis match using the SSS Method and Quadrant Research Method:

MATCH: {d['p1']} vs {d['p2']}
TOURNAMENT: {d['tournament']} — {d['round']}
SURFACE: {d['surface']} | Court speed: {d['court_speed']}
CONDITIONS: {d['conditions']}

PLAYER 1 — {d['p1']}
  Seed/Ranking: {d['p1_seed']}
  Odds: {d['p1_odds']}
  Recent form (last 5): {d['p1_form']}
  Key strength: {d['p1_strength']}

PLAYER 2 — {d['p2']}
  Seed/Ranking: {d['p2_seed']}
  Odds: {d['p2_odds']}
  Recent form (last 5): {d['p2_form']}
  Key strength: {d['p2_strength']}

HEAD TO HEAD: {d['h2h']}
GAMES TOTAL LINE: {d['total_line']}

Generate a full SSS/Quadrant breakdown and concrete verdict."""


# ─────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────
def form_badges(form_str):
    badges = []
    for r in str(form_str).strip().split():
        color = "#10B981" if r.upper() == "W" else "#EF4444"
        badges.append(f'<span style="color:{color};font-weight:700;font-size:0.9rem;margin-right:3px;">{r.upper()}</span>')
    return "".join(badges)


def render_match_header(p1, p2, tournament, round_, surface, time_):
    st.markdown(f"""
    <div class="match-card">
        <div class="match-title">{p1} vs. {p2}</div>
        <div class="match-meta">🏆 {tournament} &nbsp;·&nbsp; {round_} &nbsp;·&nbsp; 🎾 {surface} &nbsp;·&nbsp; 🕐 {time_}</div>
    </div>
    """, unsafe_allow_html=True)


def render_players(p1, p1_seed, p1_odds, p1_form, p2, p2_seed, p2_odds, p2_form):
    ca, cb, cc = st.columns([3, 2, 1])
    with ca:
        st.markdown(f"**{p1}** &nbsp; `{p1_seed}`", unsafe_allow_html=True)
    with cb:
        st.markdown(f"Form: {form_badges(p1_form)}", unsafe_allow_html=True)
    with cc:
        st.markdown(f'<span style="background:#0d9268;color:#fff;padding:3px 10px;border-radius:6px;font-family:monospace;font-weight:700;">{p1_odds}</span>', unsafe_allow_html=True)

    st.markdown('<p style="text-align:center;color:#475569;font-family:monospace;font-size:0.75rem;letter-spacing:3px;margin:4px 0;">— VS —</p>', unsafe_allow_html=True)

    ca2, cb2, cc2 = st.columns([3, 2, 1])
    with ca2:
        st.markdown(f"**{p2}** &nbsp; `{p2_seed}`", unsafe_allow_html=True)
    with cb2:
        st.markdown(f"Form: {form_badges(p2_form)}", unsafe_allow_html=True)
    with cc2:
        st.markdown(f'<span style="background:#0d9268;color:#fff;padding:3px 10px;border-radius:6px;font-family:monospace;font-weight:700;">{p2_odds}</span>', unsafe_allow_html=True)


def render_sss(sss: dict):
    st.markdown('<div class="section-label">SSS SCORE BREAKDOWN</div>', unsafe_allow_html=True)
    for key, val in sss.items():
        c1, c2, c3 = st.columns([1, 6, 0.5])
        with c1:
            st.markdown(f'<span style="font-family:monospace;font-size:0.8rem;color:#10B981;">{key}</span>', unsafe_allow_html=True)
        with c2:
            st.progress(min(int(val), 100) / 100)
        with c3:
            st.markdown(f'<span style="font-family:monospace;font-size:0.8rem;color:#94A3B8;">{val}</span>', unsafe_allow_html=True)
    avg = sum(min(int(v), 100) for v in sss.values()) // 3
    st.markdown(f'<p style="font-family:monospace;font-size:0.8rem;color:#64748B;margin-top:4px;">SSS COMPOSITE: <span style="color:#10B981;font-weight:700;">{avg}/100</span></p>', unsafe_allow_html=True)


def render_quads(match: dict):
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">QUADRANT BREAKDOWN</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, qk in zip([c1, c2, c3], ["q1", "q2", "q3"]):
        q = match[qk]
        with col:
            st.markdown(f"""
            <div class="quad-card">
                <div class="quad-header">
                    <span class="quad-icon">{q['icon']}</span>
                    <span class="quad-title">{q['title']}</span>
                </div>
                <div class="quad-body">{q['body']}</div>
            </div>
            """, unsafe_allow_html=True)

    q4 = match["q4"]
    conf = int(q4.get("confidence", 0))
    if conf > 0:
        conf_color = "#10B981" if conf >= 65 else "#F59E0B" if conf >= 50 else "#EF4444"
        conf_label = "HIGH" if conf >= 65 else "MODERATE" if conf >= 50 else "LOW"
        st.markdown(f"""
        <div class="verdict-banner">
            <div>
                <div class="verdict-label">🏆 Q4 — The Verdict</div>
                <div class="verdict-pick">{q4['pick']}</div>
                <div style="font-size:0.85rem;color:#94A3B8;margin-top:0.5rem;max-width:500px;line-height:1.6;">{q4['body']}</div>
            </div>
            <div style="text-align:center;">
                <div class="confidence-num" style="color:{conf_color};">{conf}%</div>
                <div class="confidence-tag">Confidence</div>
                <div style="font-size:0.68rem;color:{conf_color};letter-spacing:2px;margin-top:3px;">{conf_label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="verdict-banner">
            <div>
                <div class="verdict-label">🏆 Q4 — Post-Match Analysis</div>
                <div class="verdict-pick" style="color:#94A3B8;">— Match Completed —</div>
                <div style="font-size:0.85rem;color:#94A3B8;margin-top:0.5rem;max-width:580px;line-height:1.6;">{q4['body']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:0.5rem 0 1.5rem;'>
        <div style='font-size:2.4rem;margin-bottom:6px;'>🎾</div>
        <div style='font-family:"Space Mono",monospace;font-size:1.1rem;color:#10B981;font-weight:700;'>SSS/QUAD TOOL</div>
        <div style='font-size:0.68rem;color:#64748B;letter-spacing:2px;text-transform:uppercase;margin-top:2px;'>Tennis Betting Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">📐 Methodology</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.8rem;color:#10B981;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.6rem;">▸ The SSS Method</div>', unsafe_allow_html=True)

    for icon, label, desc in [
        ("📊", "S1 — Stats", "H2H records, win/loss trends, serve & return efficiency, break-point conversion, tiebreak records, and high-pressure performance metrics."),
        ("🌡️", "S2 — Surface", "Court speed rating, bounce height, environmental factors including humidity, wind, altitude, and how they interact with each player's game style."),
        ("🧠", "S3 — Situation", "Defending points pressure, physical fatigue signals, rest differential, psychological 'Alpha' status, crowd dynamics, and tournament context."),
    ]:
        st.markdown(f'<div class="method-card"><div class="method-title">{icon} {label}</div><div class="method-desc">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔲 Quadrant Method</div>', unsafe_allow_html=True)

    for icon, label, desc in [
        ("📊", "Q1 — Statistical Profile", "Hard data: break-point conversion, seasonal performance metrics, serve stats, and head-to-head records."),
        ("🌵", "Q2 — Environmental Context", "Court-specific physics, weather conditions, altitude, and how they bias outcomes toward certain playing styles."),
        ("🧠", "Q3 — Psychological / Narrative", "Player motivations, revenge arcs, momentum, confidence levels, and crowd dynamics."),
        ("🏆", "Q4 — The Verdict", "Synthesis of all quadrants into a final pick, reasoning, and confidence rating (0–100%)."),
    ]:
        st.markdown(f'<div class="method-card"><div class="method-title">{icon} {label}</div><div class="method-desc">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:#475569;text-align:center;line-height:1.6;">For educational & analytical purposes only.<br>Gamble responsibly. 18+.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN STAGE
# ─────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <div style="font-size:2rem;">🎾</div>
    <div>
        <div class="brand-title">SSS / QUAD TOOL</div>
        <div class="brand-sub">Tennis Betting Intelligence · Powered by AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_archive, tab_ai = st.tabs(["📁  Match Archive", "🤖  AI Quad Generator"])

# ═══════════════════════════════════════
# TAB 1 — ARCHIVE
# ═══════════════════════════════════════
with tab_archive:
    st.markdown('<div class="section-label" style="margin-top:1rem;">SELECT MATCH</div>', unsafe_allow_html=True)
    selected = st.selectbox("match", options=list(MATCHES.keys()), label_visibility="collapsed")
    match = MATCHES[selected]
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">MATCH PREVIEW</div>', unsafe_allow_html=True)
    render_match_header(match['p1'], match['p2'], match['tournament'], match['round'], match['surface'], match['time'])
    render_players(match['p1'], match['p1_seed'], match['p1_odds'], match['recent_p1'],
                   match['p2'], match['p2_seed'], match['p2_odds'], match['recent_p2'])

    st.markdown("<br>", unsafe_allow_html=True)
    cs1, cs2, cs3 = st.columns(3)
    with cs1: st.metric("H2H", match["h2h"])
    with cs2: st.metric("Total Line", match["total"])
    with cs3: st.metric("Court Speed", match["surface_speed"])

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    render_sss(match["sss"])
    render_quads(match)

    st.markdown('<div style="text-align:center;margin-top:3rem;font-size:0.68rem;color:#334155;letter-spacing:1.5px;text-transform:uppercase;">SSS/Quad Tool · For analytical purposes only · Always gamble responsibly</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════
# TAB 2 — AI QUAD GENERATOR
# ═══════════════════════════════════════
with tab_ai:
    st.markdown('<div class="section-label" style="margin-top:1rem;">AI-Powered Match Analysis</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;font-size:0.88rem;margin-bottom:1.5rem;">Enter any match details below. Claude will generate a full SSS breakdown and Quadrant analysis instantly.</p>', unsafe_allow_html=True)

    # ── Players & Odds ──────────────────
    st.markdown('<div class="form-section-title">⚔️ Players & Odds</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        p1_name     = st.text_input("Player 1 Name", placeholder="e.g. Jack Draper")
        p1_seed     = st.text_input("P1 Seed / Ranking", placeholder="e.g. #15 / World No.15")
        p1_odds     = st.text_input("P1 Odds", placeholder="e.g. +145")
        p1_form     = st.text_input("P1 Last 5 Results", placeholder="W W L W W")
        p1_strength = st.text_input("P1 Key Strength", placeholder="e.g. Tiebreak dominance, big serve")

    with fc2:
        p2_name     = st.text_input("Player 2 Name", placeholder="e.g. Daniil Medvedev")
        p2_seed     = st.text_input("P2 Seed / Ranking", placeholder="e.g. #4 / World No.4")
        p2_odds     = st.text_input("P2 Odds", placeholder="e.g. -175")
        p2_form     = st.text_input("P2 Last 5 Results", placeholder="W W W L W")
        p2_strength = st.text_input("P2 Key Strength", placeholder="e.g. Baseline consistency, return")

    # ── Match Context ───────────────────
    st.markdown('<div class="form-section-title">🏟️ Match Context</div>', unsafe_allow_html=True)

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        tournament  = st.text_input("Tournament", placeholder="e.g. ATP Indian Wells Masters")
        round_      = st.text_input("Round", placeholder="e.g. Quarterfinal")
    with mc2:
        surface     = st.selectbox("Surface", ["Hard (Outdoor)", "Hard (Indoor)", "Clay", "Grass"])
        court_speed = st.selectbox("Court Speed", ["Slow", "Medium-Slow", "Medium", "Medium-Fast", "Fast"])
    with mc3:
        h2h         = st.text_input("H2H Record", placeholder="e.g. Medvedev leads 3-1")
        total_line  = st.text_input("Games Total Line", placeholder="e.g. 22.5")

    conditions = st.text_input(
        "Conditions / Extra Notes",
        placeholder="e.g. Night session, heavy air, defending champion, crowd factor, fatigue concerns..."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("🤖  Generate AI Analysis")

    if generate_clicked:
        if not p1_name or not p2_name:
            st.error("Please enter both player names before generating.")
        else:
            form_data = {
                "p1": p1_name,       "p1_seed": p1_seed or "—",
                "p1_odds": p1_odds or "—", "p1_form": p1_form or "—",
                "p1_strength": p1_strength or "—",
                "p2": p2_name,       "p2_seed": p2_seed or "—",
                "p2_odds": p2_odds or "—", "p2_form": p2_form or "—",
                "p2_strength": p2_strength or "—",
                "tournament": tournament or "Unknown Tournament",
                "round": round_ or "—", "surface": surface,
                "court_speed": court_speed, "h2h": h2h or "No H2H data provided",
                "total_line": total_line or "—",
                "conditions": conditions or "Standard conditions",
            }

            with st.spinner("🤖 Claude is generating your analysis..."):
                try:
                    result = call_claude(build_prompt(form_data))
                    st.session_state["ai_result"] = result
                    st.session_state["ai_form"]   = form_data
                except requests.exceptions.HTTPError as e:
                    st.error(f"API error {e.response.status_code}: {e.response.text[:300]}")
                    st.session_state.pop("ai_result", None)
                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"Could not parse AI response: {e}")
                    st.session_state.pop("ai_result", None)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.pop("ai_result", None)

    # ── Results Display ─────────────────
    if "ai_result" in st.session_state and "ai_form" in st.session_state:
        result = st.session_state["ai_result"]
        fd     = st.session_state["ai_form"]

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">AI-Generated Analysis</div>', unsafe_allow_html=True)

        if result.get("summary"):
            st.markdown(f'<p style="color:#94A3B8;font-size:0.88rem;font-style:italic;margin-bottom:1rem;">💬 {result["summary"]}</p>', unsafe_allow_html=True)

        render_match_header(fd['p1'], fd['p2'], fd['tournament'], fd['round'], fd['surface'], f"{fd['court_speed']} court")
        render_players(fd['p1'], fd['p1_seed'], fd['p1_odds'], fd['p1_form'],
                       fd['p2'], fd['p2_seed'], fd['p2_odds'], fd['p2_form'])

        st.markdown("<br>", unsafe_allow_html=True)
        as1, as2, as3 = st.columns(3)
        with as1: st.metric("H2H", fd["h2h"])
        with as2: st.metric("Total Line", fd["total_line"] or "—")
        with as3: st.metric("Surface", fd["surface"])

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        render_sss(result["sss"])
        render_quads(result)

        st.markdown('<div style="text-align:center;margin-top:3rem;font-size:0.68rem;color:#334155;letter-spacing:1.5px;text-transform:uppercase;">AI analysis by Claude · Educational purposes only · Gamble responsibly</div>', unsafe_allow_html=True)
