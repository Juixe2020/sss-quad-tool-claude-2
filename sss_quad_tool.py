import streamlit as st

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
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
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

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--bg-sec) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* ── Main container ── */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Top banner / wordmark ── */
.brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.25rem;
}
.brand-icon {
    font-size: 2rem;
    line-height: 1;
}
.brand-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.5px;
}
.brand-sub {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Section headers ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.6rem;
}

/* ── Match Preview Card ── */
.match-card {
    background: var(--slate);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    box-shadow: var(--glow);
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.match-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent);
    border-radius: 4px 0 0 4px;
}
.match-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.25rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.25rem;
}
.match-meta {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 1.1rem;
    letter-spacing: 0.5px;
}
.player-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255,255,255,0.04);
    border-radius: 9px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 0.5rem;
}
.player-name {
    font-weight: 600;
    font-size: 1rem;
}
.player-seed {
    font-size: 0.72rem;
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    background: rgba(16,185,129,0.1);
    padding: 2px 7px;
    border-radius: 4px;
    border: 1px solid var(--border);
}
.odds-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #fff;
    background: var(--accent-dim);
    padding: 4px 10px;
    border-radius: 6px;
}
.match-stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-top: 1.1rem;
}
.stat-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 0.55rem 0.8rem;
    text-align: center;
}
.stat-pill-label {
    font-size: 0.67rem;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
}
.stat-pill-value {
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--accent);
    margin-top: 2px;
}

/* ── Quadrant cards ── */
.quad-card {
    background: var(--bg-sec);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    height: 100%;
    box-shadow: var(--glow);
    transition: border-color 0.2s;
}
.quad-card:hover {
    border-color: var(--accent);
}
.quad-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.75rem;
}
.quad-icon {
    font-size: 1.3rem;
}
.quad-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--accent);
}
.quad-body {
    font-size: 0.87rem;
    color: var(--muted);
    line-height: 1.65;
}
.quad-body strong {
    color: var(--text);
}

/* ── Verdict banner ── */
.verdict-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(16,185,129,0.04));
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 1.3rem 1.6rem;
    margin-top: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.verdict-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}
.verdict-pick {
    font-family: 'Space Mono', monospace;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--accent);
}
.confidence-ring {
    text-align: center;
}
.confidence-num {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.confidence-tag {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 3px;
}

/* ── SSS Meter ── */
.sss-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.55rem;
}
.sss-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent);
    width: 75px;
    flex-shrink: 0;
}
.sss-bar-bg {
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    overflow: hidden;
}
.sss-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-dim), var(--accent));
    border-radius: 99px;
}
.sss-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    width: 30px;
    text-align: right;
}

/* ── Sidebar method cards ── */
.method-card {
    background: rgba(16,185,129,0.05);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
}
.method-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.method-desc {
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.55;
}

/* ── Selectbox styling ── */
[data-testid="stSelectbox"] > div > div {
    background-color: var(--bg-sec) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSelectbox"] label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

/* ── Divider ── */
.custom-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.6rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MATCH DATA
# ─────────────────────────────────────────
MATCHES = {
    "🎾 Draper [15] vs. Medvedev [4] — ATP Indian Wells QF": {
        "p1": "Jack Draper", "p1_seed": "#15", "p1_odds": "+145",
        "p2": "Daniil Medvedev", "p2_seed": "#4", "p2_odds": "-175",
        "tournament": "ATP Indian Wells Masters", "round": "Quarterfinal",
        "surface": "Hard (Outdoor)", "time": "Tonight · Stadium 1",
        "h2h": "Medvedev leads 3–1", "recent_p1": "W W W W L", "recent_p2": "W W L W W",
        "total": "23.5 games", "surface_speed": "Medium-Fast",
        "q1": {
            "title": "Statistical Profile",
            "icon": "📊",
            "body": "Draper's break-point conversion sits at <strong>47%</strong> this hard-court swing — elite for his age bracket. Medvedev's first-serve points won: <strong>76%</strong> on hard courts in 2026, the highest on tour. H2H: Medvedev 3–1, but Draper's lone win came at an indoor Masters. Draper's tiebreak record in 2026: <strong>7/9 (77%)</strong>.",
        },
        "q2": {
            "title": "Environmental Context",
            "icon": "🌵",
            "body": "Indian Wells night sessions carry <strong>heavy, dense air</strong> — ball travels slower, rallies extend. This benefits baseline counterpunchers. Medvedev thrives in these conditions historically. Altitude is ~480m, mildly reducing serve dominance. Wind forecast: calm (< 5mph). Court speed: IW plays ~6% slower than tour average.",
        },
        "q3": {
            "title": "Psychological / Narrative",
            "icon": "🧠",
            "body": "Draper is riding <strong>alpha status momentum</strong> — just took out World No.1 Djokovic in straight/three sets. He's defending his 2025 title, adding emotional fuel. Medvedev struggled with a mid-match fade vs. Fils in R16. Draper's crowd support is massive in California. Medvedev historically flat after grinding five-setters.",
        },
        "q4": {
            "title": "The Verdict",
            "icon": "🏆",
            "pick": "Draper ML + Over 22.5 Games",
            "confidence": 68,
            "body": "Draper's momentum, tiebreak dominance, and the heavy night conditions tip this in his favour. Medvedev's serve will be suppressed — expect at least one set going to tiebreak. Value play: <strong>Draper ML (+145)</strong> with optional cover on <strong>Over 22.5</strong>.",
        },
        "sss": {"Stats": 62, "Surface": 55, "Situation": 80},
    },
    "🎾 Pegula [5] vs. Rybakina [6] — WTA Indian Wells R16": {
        "p1": "Jessica Pegula", "p1_seed": "#5", "p1_odds": "+110",
        "p2": "Elena Rybakina", "p2_seed": "#6", "p2_odds": "-130",
        "tournament": "WTA Indian Wells Masters", "round": "Round of 16",
        "surface": "Hard (Outdoor)", "time": "Tonight · Court 2",
        "h2h": "Rybakina leads 4–2", "recent_p1": "W W L W W", "recent_p2": "W L W W W",
        "total": "19.5 games", "surface_speed": "Medium-Fast",
        "q1": {
            "title": "Statistical Profile",
            "icon": "📊",
            "body": "Rybakina's serve is the statistical standout: <strong>68% first-serve in</strong>, <strong>92mph average</strong> on second serve. Pegula wins <strong>41%</strong> of return games — top-5 WTA. Rybakina's backhand break-point save rate: <strong>71%</strong> in 2026. H2H leans Rybakina but Pegula took their last outdoor hard-court meeting.",
        },
        "q2": {
            "title": "Environmental Context",
            "icon": "🌵",
            "body": "IW outdoor hard courts in March evenings: <strong>mild (65°F)</strong>, low humidity post-sunset. Ball conditions favour big servers — <strong>slight edge to Rybakina</strong>. Daytime courts were slow; evening sessions historically play 4% faster. Court 2 at IW has a tighter wind tunnel effect.",
        },
        "q3": {
            "title": "Psychological / Narrative",
            "icon": "🧠",
            "body": "Pegula enters with <strong>renewed motivation</strong> post-2025 US Open run. Rybakina has been quietly dominant but avoided media scrutiny. No revenge arc here — this is a chess match. Pegula is well-known for her durability in long third sets. Rybakina tends to go for broke on big points — high variance player.",
        },
        "q4": {
            "title": "The Verdict",
            "icon": "🏆",
            "pick": "Rybakina ML + Under 20.5 Games",
            "confidence": 61,
            "body": "Rybakina's serve neutralises Pegula's return prowess on a faster IW night court. Under is value — Rybakina closes sets quickly when her serve clicks. Moderate confidence; Pegula's resilience adds uncertainty. <strong>Rybakina ML (-130)</strong> is the lean.",
        },
        "sss": {"Stats": 58, "Surface": 70, "Situation": 52},
    },
    "🎾 Svitolina def. Swiatek — WTA IW R16 (RESULT)": {
        "p1": "Elina Svitolina", "p1_seed": "—", "p1_odds": "+280 (pre-match)",
        "p2": "Iga Swiatek", "p2_seed": "#1", "p2_odds": "-380 (pre-match)",
        "tournament": "WTA Indian Wells Masters", "round": "Round of 16 ✅ COMPLETED",
        "surface": "Hard (Outdoor)", "time": "March 12 · Final score: 6-2, 4-6, 6-4",
        "h2h": "Swiatek led 12–3 pre-match", "recent_p1": "W W L W W", "recent_p2": "W W W W L",
        "total": "Actual: 28 games", "surface_speed": "Medium-Fast",
        "q1": {
            "title": "Statistical Profile",
            "icon": "📊",
            "body": "A massive upset. Svitolina won <strong>78% of first-serve points</strong> (career high vs. Swiatek). Swiatek's unforced error count ballooned to <strong>41</strong> — her highest at IW in 3 years. Svitolina's return game was exceptional: <strong>5 breaks</strong> in the match.",
        },
        "q2": {
            "title": "Environmental Context",
            "icon": "🌵",
            "body": "Played in moderate evening conditions. IW night air favoured <strong>flatter, harder hitters</strong> — Svitolina's compact, penetrating groundstrokes thrived. Swiatek's heavy topspin lost some margin in these conditions. Surface speed contributed to Svitolina's flat-hitting strategy.",
        },
        "q3": {
            "title": "Psychological / Narrative",
            "icon": "🧠",
            "body": "Svitolina brought a <strong>war mentality</strong> — she's been vocal about competing with nothing to lose. Swiatek appeared fatigued after a tight R2 match. The crowd energy shifted dramatically after the first set. Svitolina's resilience in 3-set matches (the \\\"gut set\\\") is elite-level.",
        },
        "q4": {
            "title": "The Verdict",
            "icon": "🏆",
            "pick": "— Match Completed —",
            "confidence": 0,
            "body": "Post-result analysis: This was a low-probability upset (<strong>+280 implied ~26%</strong>). The SSS framework would have graded Situation at 65+ for Svitolina had psychological fatigue signals been priced in. Key lesson: <strong>rest differential</strong> in back-to-back days matters more than H2H at slams/Masters.",
        },
        "sss": {"Stats": 30, "Surface": 50, "Situation": 65},
    },
}

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1.5rem;'>
        <div style='font-size:2.4rem; margin-bottom:6px;'>🎾</div>
        <div style='font-family:"Space Mono",monospace; font-size:1.1rem; color:#10B981; font-weight:700;'>SSS/QUAD TOOL</div>
        <div style='font-size:0.68rem; color:#64748B; letter-spacing:2px; text-transform:uppercase; margin-top:2px;'>Tennis Betting Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">📐 Methodology</div>', unsafe_allow_html=True)

    # SSS Method
    st.markdown("""
    <div style='font-family:"Space Mono",monospace; font-size:0.8rem; color:#10B981; letter-spacing:1px;
                text-transform:uppercase; margin-bottom:0.6rem; margin-top:0.2rem;'>
        ▸ The SSS Method
    </div>
    """, unsafe_allow_html=True)

    for icon, label, desc in [
        ("📊", "S1 — Stats", "H2H records, win/loss trends, serve & return efficiency, break-point conversion, tiebreak records, and high-pressure performance metrics."),
        ("🌡️", "S2 — Surface", "Court speed rating, bounce height, environmental factors including humidity, wind, altitude, and how they interact with each player's game style."),
        ("🧠", "S3 — Situation", "Defending points pressure, physical fatigue signals, rest differential, psychological 'Alpha' status, crowd dynamics, and tournament context."),
    ]:
        st.markdown(f"""
        <div class="method-card">
            <div class="method-title">{icon} {label}</div>
            <div class="method-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔲 Quadrant Method</div>', unsafe_allow_html=True)

    for icon, label, desc in [
        ("📊", "Q1 — Statistical Profile", "Hard data: break-point conversion, seasonal performance metrics, serve stats, and head-to-head records."),
        ("🌵", "Q2 — Environmental Context", "Court-specific physics, weather conditions, altitude, and how they bias outcomes toward certain playing styles."),
        ("🧠", "Q3 — Psychological / Narrative", "Player motivations, revenge arcs, momentum, confidence levels, and crowd dynamics shaping the mental battlefield."),
        ("🏆", "Q4 — The Verdict", "Synthesis of all three quadrants into a final pick, reasoning, and confidence rating (0–100%)."),
    ]:
        st.markdown(f"""
        <div class="method-card">
            <div class="method-title">{icon} {label}</div>
            <div class="method-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#475569; text-align:center; line-height:1.6;'>
        For educational & analytical purposes only.<br>
        Gamble responsibly. 18+.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN STAGE
# ─────────────────────────────────────────

# Brand header
st.markdown("""
<div class="brand-header">
    <div class="brand-icon">🎾</div>
    <div>
        <div class="brand-title">SSS / QUAD TOOL</div>
        <div class="brand-sub">Tennis Betting Intelligence · Indian Wells 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Match Selector
st.markdown('<div class="section-label">SELECT MATCH</div>', unsafe_allow_html=True)
selected = st.selectbox(
    label="select_match",
    options=list(MATCHES.keys()),
    label_visibility="collapsed",
)

match = MATCHES[selected]
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── Match Preview Card ──────────────────
st.markdown('<div class="section-label">MATCH PREVIEW</div>', unsafe_allow_html=True)

def form_badges(form_str):
    badges = []
    for r in form_str.split():
        color = "#10B981" if r == "W" else "#EF4444"
        badges.append(f'<span style="color:{color};font-weight:700;font-size:0.9rem;margin-right:3px;">{r}</span>')
    return "".join(badges)

# Card wrapper open
st.markdown(f"""
<div class="match-card">
    <div class="match-title">{match['p1']} vs. {match['p2']}</div>
    <div class="match-meta">🏆 {match['tournament']} &nbsp;·&nbsp; {match['round']} &nbsp;·&nbsp;
    🎾 {match['surface']} &nbsp;·&nbsp; 🕐 {match['time']}</div>
</div>
""", unsafe_allow_html=True)

# Player rows using native Streamlit columns
col_p1a, col_p1b, col_p1c = st.columns([3, 2, 1])
with col_p1a:
    st.markdown(f"**{match['p1']}** &nbsp; `{match['p1_seed']}`", unsafe_allow_html=True)
with col_p1b:
    st.markdown(f"Form: {form_badges(match['recent_p1'])}", unsafe_allow_html=True)
with col_p1c:
    st.markdown(f'<span style="background:#0d9268;color:#fff;padding:3px 10px;border-radius:6px;font-family:monospace;font-weight:700;">{match["p1_odds"]}</span>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center;color:#475569;font-family:monospace;font-size:0.75rem;letter-spacing:3px;margin:2px 0;">— VS —</p>', unsafe_allow_html=True)

col_p2a, col_p2b, col_p2c = st.columns([3, 2, 1])
with col_p2a:
    st.markdown(f"**{match['p2']}** &nbsp; `{match['p2_seed']}`", unsafe_allow_html=True)
with col_p2b:
    st.markdown(f"Form: {form_badges(match['recent_p2'])}", unsafe_allow_html=True)
with col_p2c:
    st.markdown(f'<span style="background:#0d9268;color:#fff;padding:3px 10px;border-radius:6px;font-family:monospace;font-weight:700;">{match["p2_odds"]}</span>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Stats row
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.metric("H2H", match["h2h"])
with col_s2:
    st.metric("Total Line", match["total"])
with col_s3:
    st.metric("Court Speed", match["surface_speed"])

# ── SSS Meter ──────────────────────────
st.markdown('<div class="section-label">SSS SCORE BREAKDOWN</div>', unsafe_allow_html=True)
sss = match["sss"]

for key, val in sss.items():
    col_label, col_bar, col_val = st.columns([1, 6, 0.5])
    with col_label:
        st.markdown(f'<span style="font-family:monospace;font-size:0.8rem;color:#10B981;">{key}</span>', unsafe_allow_html=True)
    with col_bar:
        st.progress(val / 100)
    with col_val:
        st.markdown(f'<span style="font-family:monospace;font-size:0.8rem;color:#94A3B8;">{val}</span>', unsafe_allow_html=True)

avg = sum(sss.values()) // 3
st.markdown(f'<p style="font-family:monospace;font-size:0.8rem;color:#64748B;margin-top:4px;">SSS COMPOSITE: <span style="color:#10B981;font-weight:700;">{avg}/100</span></p>', unsafe_allow_html=True)
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── Quadrant Breakdown ─────────────────
st.markdown('<div class="section-label">QUADRANT BREAKDOWN</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]
quad_keys = ["q1", "q2", "q3"]

for i, qk in enumerate(quad_keys):
    q = match[qk]
    with cols[i]:
        st.markdown(f"""
        <div class="quad-card">
            <div class="quad-header">
                <span class="quad-icon">{q['icon']}</span>
                <span class="quad-title">{q['title']}</span>
            </div>
            <div class="quad-body">{q['body']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Q4 Verdict ─────────────────────────
q4 = match["q4"]
conf = q4["confidence"]

if conf > 0:
    conf_color = "#10B981" if conf >= 65 else "#F59E0B" if conf >= 50 else "#EF4444"
    conf_label = "HIGH" if conf >= 65 else "MODERATE" if conf >= 50 else "LOW"
    st.markdown(f"""
    <div class="verdict-banner" style="margin-top:1rem;">
        <div>
            <div class="verdict-label">{q4['icon']} Q4 — The Verdict</div>
            <div class="verdict-pick">{q4['pick']}</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:0.5rem; max-width:480px; line-height:1.6;">
                {q4['body']}
            </div>
        </div>
        <div class="confidence-ring">
            <div class="confidence-num" style="color:{conf_color};">{conf}%</div>
            <div class="confidence-tag">Confidence</div>
            <div style="font-size:0.68rem; color:{conf_color}; letter-spacing:2px; margin-top:3px;">{conf_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="verdict-banner" style="margin-top:1rem;">
        <div>
            <div class="verdict-label">{q4['icon']} Q4 — Post-Match Analysis</div>
            <div class="verdict-pick" style="color:#94A3B8;">— Match Completed —</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:0.5rem; max-width:580px; line-height:1.6;">
                {q4['body']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-top:3rem; font-size:0.68rem; color:#334155;
            letter-spacing:1.5px; text-transform:uppercase;'>
    SSS/Quad Tool · For analytical purposes only · Always gamble responsibly
</div>
""", unsafe_allow_html=True)
