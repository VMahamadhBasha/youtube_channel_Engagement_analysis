# app.py
# YouTube Insight Hub — Professional Dashboard
# Infosys Springboard 6.0 | Dark Purple Theme (inspired by sample)
# Modular: add new sections without touching existing code

import streamlit as st
from datetime import date
import plotly.graph_objects as go
import pandas as pd

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Insight Hub",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Utility ──────────────────────────────────────────────────────────────────
def fmt(n):
    try:
        n = int(n)
        if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
        if n >= 1_000:     return f"{n/1_000:.1f}K"
        return str(n)
    except: return "0"

# ── Global CSS — Purple/Dark theme matching reference ────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d1a !important;
    color: #e2e2f0;
    font-family: 'Outfit', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #1a0a2e 0%, #0d0d1a 50%, #080814 100%) !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Top Nav ── */
.yt-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 2.5rem;
    background: rgba(13,13,26,0.92);
    border-bottom: 1px solid rgba(138,43,226,0.3);
    backdrop-filter: blur(12px);
}
.yt-nav-logo { font-size: 1.1rem; font-weight: 700; color: #fff; letter-spacing: -0.3px; }
.yt-nav-logo span { color: #8b5cf6; }
.yt-nav-right { display: flex; gap: 1rem; align-items: center; }
.nav-btn { padding: 0.35rem 1.1rem; border-radius: 6px; font-size: 0.8rem; font-weight: 500; border: 1px solid rgba(138,43,226,0.4); background: transparent; color: #ccc; font-family: 'Outfit', sans-serif; cursor: pointer; }
.nav-btn-primary { background: linear-gradient(135deg,#7c3aed,#5b21b6); border: none; color: white; border-radius: 20px; }

/* ── Page wrapper ── */
.page-wrap { padding: 2rem 2.5rem; }
.hero-title { font-size: 1.45rem; font-weight: 700; color: #fff; margin-bottom: 1.6rem; letter-spacing: -0.3px; }

/* ── Main dashboard card ── */
.dashboard-card {
    background: rgba(18,12,38,0.75);
    border: 1.5px solid rgba(138,43,226,0.4);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    box-shadow: 0 0 60px rgba(138,43,226,0.07), inset 0 1px 0 rgba(255,255,255,0.03);
    margin-bottom: 1.5rem;
}

/* ── Input area ── */
.input-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #7070a0; margin-bottom: 0.4rem; }
.channel-info-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(138,43,226,0.2);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    font-size: 0.85rem;
    color: #9090b0;
    line-height: 1.75;
    min-height: 90px;
}

/* ── Section label ── */
.sec-title {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 1.8px;
    text-transform: uppercase; color: #5050a0;
    margin: 1.8rem 0 0.8rem 0.2rem;
    padding-left: 0.7rem;
    border-left: 2px solid #7c3aed;
}

/* ── Mini metric cards ── */
.mini-card {
    background: rgba(12,10,28,0.95);
    border: 1px solid rgba(138,43,226,0.18);
    border-radius: 13px;
    padding: 1.1rem 1.2rem;
    position: relative; overflow: hidden;
    transition: border-color 0.25s, transform 0.2s;
    margin-bottom: 0.2rem;
}
.mini-card:hover { border-color: rgba(138,43,226,0.45); transform: translateY(-2px); }
.mini-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #7c3aed 40%, #a855f7 60%, transparent);
}
.mini-card-label { font-size: 0.68rem; font-weight: 600; letter-spacing: 1.4px; text-transform: uppercase; color: #6060a0; margin-bottom: 0.45rem; }
.mini-card-value { font-size: 1.55rem; font-weight: 700; color: #fff; font-family: 'IBM Plex Mono', monospace; line-height: 1; }
.mini-card-sub { font-size: 0.7rem; color: #484878; margin-top: 0.3rem; }

/* ── Gauge ring ── */
.gauge-wrap { margin-top: 0.6rem; }
.gauge-ring {
    width: 52px; height: 52px; border-radius: 50%;
    border: 3.5px solid rgba(138,43,226,0.15);
    border-top: 3.5px solid #8b5cf6;
    border-right: 3.5px solid #8b5cf6;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 600; color: #a78bfa;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── Chart cards ── */
.chart-card {
    background: rgba(12,10,28,0.95);
    border: 1px solid rgba(138,43,226,0.18);
    border-radius: 13px;
    padding: 1.2rem 1.3rem;
}
.chart-card-title { font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; color: #5050a0; text-transform: uppercase; margin-bottom: 0.6rem; }

/* ── Pills ── */
.pill-green  { background: rgba(74,222,128,0.1);  color: #4ade80; border: 1px solid rgba(74,222,128,0.2);  padding: 0.15rem 0.65rem; border-radius: 20px; font-size: 0.68rem; font-weight: 600; }
.pill-yellow { background: rgba(251,191,36,0.1);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2);  padding: 0.15rem 0.65rem; border-radius: 20px; font-size: 0.68rem; font-weight: 600; }
.pill-red    { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.2); padding: 0.15rem 0.65rem; border-radius: 20px; font-size: 0.68rem; font-weight: 600; }

/* ── Streamlit overrides ── */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(138,43,226,0.35) !important;
    border-radius: 8px !important; color: #e2e2f0 !important; font-family: 'Outfit',sans-serif !important; font-size: 0.88rem !important;
}
div[data-testid="stTextInput"] input:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 2px rgba(124,58,237,0.18) !important; }
div[data-testid="stDateInput"] input { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(138,43,226,0.25) !important; border-radius: 8px !important; color: #e2e2f0 !important; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#7c3aed 0%,#5b21b6 100%) !important; border: none !important; border-radius: 8px !important; color: white !important; font-family: 'Outfit',sans-serif !important; font-weight: 600 !important; font-size: 0.85rem !important; width: 100%; }
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
label[data-testid="stWidgetLabel"] p { color: #6060a0 !important; font-size: 0.72rem !important; letter-spacing: 0.8px !important; font-weight: 600 !important; text-transform: uppercase !important; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
div[data-testid="stMetric"] { background: rgba(12,10,28,0.95); border: 1px solid rgba(138,43,226,0.18); border-radius: 12px; padding: 1rem 1.2rem; }
div[data-testid="stMetricValue"] { color: #fff !important; font-family: 'IBM Plex Mono',monospace !important; }
div[data-testid="stMetricLabel"] { color: #6060a0 !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 1.2px !important; }
</style>
""", unsafe_allow_html=True)

# ── Nav Bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="yt-nav">
    <div class="yt-nav-logo">YouTube <span>Insight Hub</span></div>
    <div class="yt-nav-right">
        <button class="nav-btn">Log In</button>
        <button class="nav-btn nav-btn-primary">Sign Up</button>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">YouTube Insight Hub: Analyze Your Channel</div>', unsafe_allow_html=True)

# ── Import DB modules ─────────────────────────────────────────────────────────
# Catching ImportError with a clear message so the user knows exactly what is missing.
try:
    from database  import create_database, DB_PATH
    from api       import build_youtube_channel_data
    from storage   import save_to_local, load_from_local
    from db_insert import push_to_database
    from db_queries import (
        get_channel_summary, get_top_videos,
        get_videos_by_month, get_filtered_videos
    )
    DB_AVAILABLE = True
except ImportError as import_err:
    DB_AVAILABLE = False
    st.error(
        f"⚠️ A required module could not be imported: {import_err}\n\n"
        "Make sure all files are in the same folder as app.py:\n"
        "database.py · api.py · storage.py · db_insert.py · db_queries.py · config.py\n\n"
        "Then run:  pip install -r requirements.txt"
    )
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — INPUT CARD (Channel ID + Channel Info)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)

col_in, col_info = st.columns([1.2, 2], gap="large")

with col_in:
    st.markdown('<p class="input-label">Channel ID</p>', unsafe_allow_html=True)
    channel_id_input = st.text_input("cid", placeholder="e.g. UC4a-Gbdw7vOaccHmFo40b9g", label_visibility="collapsed")
    fetch_btn = st.button("⚡  Analyse Channel")

active_channel = st.session_state.get("active_channel_id", None)

# Wrap get_channel_summary so a stale/missing channel_id doesn't crash the whole page
summary = {}
if active_channel:
    try:
        summary = get_channel_summary(active_channel) or {}
    except Exception as e:
        st.warning(f"⚠️ Could not load channel summary: {e}")

with col_info:
    st.markdown('<p class="input-label">About Channel</p>', unsafe_allow_html=True)
    if summary:
        title = summary.get("title", "—")
        subs  = fmt(summary.get("subscriber_count", 0))
        vids  = fmt(summary.get("video_count", 0))
        views = fmt(summary.get("view_count", 0))
        st.markdown(f"""
        <div class="channel-info-box">
            <strong style="color:#c4b5fd;font-size:1rem;">{title}</strong><br>
            <span style="color:#7070a0;">Channel ID:</span> <span style="color:#9090c0;font-family:'IBM Plex Mono',monospace;font-size:0.8rem;">{active_channel}</span><br>
            📺 <strong style="color:#e2e2f0;">{vids}</strong> videos &nbsp;·&nbsp;
            👥 <strong style="color:#e2e2f0;">{subs}</strong> subscribers &nbsp;·&nbsp;
            👁️ <strong style="color:#e2e2f0;">{views}</strong> total views
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="channel-info-box" style="color:#3a3a60;">
            Enter a Channel ID on the left and click <strong style="color:#7c3aed;">Analyse Channel</strong>.<br>
            Data is fetched from YouTube API, saved locally as JSON,
            then stored in your SQLite database for instant reloads.
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Fetch logic ───────────────────────────────────────────────────────────────
if fetch_btn:
    if channel_id_input.strip():
        cid = channel_id_input.strip()
        with st.spinner("Fetching from YouTube API → saving locally → pushing to SQLite..."):
            try:
                create_database()
                data   = build_youtube_channel_data(cid)
                save_to_local(cid, data)
                loaded = load_from_local(cid)
                push_to_database(cid, loaded)
                st.session_state["active_channel_id"] = cid
                # Flag so success message survives the rerun
                st.session_state["just_loaded"] = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️  Please enter a Channel ID first.")

# Show success toast after rerun (st.success before st.rerun is wiped immediately)
if st.session_state.pop("just_loaded", False):
    st.success(f"✅ Data loaded for `{active_channel}`")

# ══════════════════════════════════════════════════════════════════════════════
# SECTIONS BELOW — only show when a channel is loaded
# ══════════════════════════════════════════════════════════════════════════════
if active_channel:

    # DATE FILTER
    st.markdown('<p class="sec-title">Date Range Filter</p>', unsafe_allow_html=True)
    dc1, dc2, _ = st.columns([1, 1, 3])
    with dc1:
        date_from = st.date_input("From", value=date(2020, 1, 1))
    with dc2:
        date_to = st.date_input("To", value=date.today())

    # Fetch data
    filtered_videos = get_filtered_videos(active_channel, str(date_from), str(date_to))
    monthly_data    = get_videos_by_month(active_channel, str(date_from), str(date_to))
    top_videos      = get_top_videos(active_channel, str(date_from), str(date_to), limit=10)

    # Index constants — match db_queries.py tuple layout exactly
    # [0]=video_id  [1]=title  [2]=views  [3]=likes  [4]=comments  [5]=duration_seconds
    VIEWS_IDX, LIKES_IDX, COMMENTS_IDX = 2, 3, 4

    total_views    = sum(v[VIEWS_IDX]    for v in filtered_videos)
    total_likes    = sum(v[LIKES_IDX]    for v in filtered_videos)
    total_comments = sum(v[COMMENTS_IDX] for v in filtered_videos)
    total_vids     = len(filtered_videos)
    engagement     = round((total_likes / total_views * 100), 1) if total_views else 0
    avg_views      = total_views // total_vids if total_vids else 0
    eng_pill       = "pill-green" if engagement > 5 else ("pill-yellow" if engagement > 2 else "pill-red")

    # ═════════════════════════════════════════════════════════════════════════
    # SECTION 2 — 4 METRIC CARDS
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sec-title">Channel Metrics</p>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4, gap="medium")

    # Card 1 — Total Views + engagement gauge
    with m1:
        st.markdown(f"""
        <div class="mini-card">
            <div class="mini-card-label">Total Views</div>
            <div class="mini-card-value">{fmt(total_views)}</div>
            <div class="mini-card-sub">in selected range</div>
            <div class="gauge-wrap">
                <div class="gauge-ring">{engagement}%</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Card 2 — Upload Trend sparkline
    with m2:
        if monthly_data:
            vals   = [r[1] for r in monthly_data]
            labels = [r[0] for r in monthly_data]
            fig_sp = go.Figure(go.Scatter(
                x=labels, y=vals, fill='tozeroy',
                line=dict(color='#8b5cf6', width=2),
                fillcolor='rgba(139,92,246,0.12)',
                hovertemplate="%{x}<br>%{y} videos<extra></extra>"
            ))
            fig_sp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=4, b=4, l=4, r=4), height=80,
                xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False
            )
            st.markdown('<div class="mini-card"><div class="mini-card-label">Upload Trend</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_sp, use_container_width=True, config={"displayModeBar": False})
            st.markdown(f'<div class="mini-card-sub">{total_vids} videos · {len(monthly_data)} months</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mini-card"><div class="mini-card-label">Videos in Range</div><div class="mini-card-value">{total_vids}</div><div class="mini-card-sub">videos uploaded</div></div>', unsafe_allow_html=True)

    # Card 3 — Top 2 videos bar
    with m3:
        top2 = top_videos[:2] if top_videos else []
        if len(top2) >= 1:
            v1_views = top2[0][VIEWS_IDX]
            v2_views = top2[1][VIEWS_IDX] if len(top2) > 1 else 0
            fig_b = go.Figure(go.Bar(
                x=["#1 Video", "#2 Video"],
                y=[v1_views, v2_views],
                marker_color=['#7c3aed', '#a78bfa'],
                hovertemplate="%{x}: %{y:,}<extra></extra>"
            ))
            fig_b.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=4, b=4, l=4, r=4), height=80,
                xaxis=dict(tickfont=dict(color='#5050a0', size=8), showgrid=False),
                yaxis=dict(visible=False), showlegend=False, bargap=0.3
            )
            v1_label = fmt(v1_views)
            v2_label = fmt(v2_views) if len(top2) > 1 else "—"
            st.markdown('<div class="mini-card"><div class="mini-card-label">Top Videos</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
            st.markdown(f'<div style="display:flex;gap:1.2rem;"><span style="font-size:0.68rem;color:#7070a0;">· #2: {v2_label}</span><span style="font-size:0.68rem;color:#9b7fff;">· #1: {v1_label}</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mini-card"><div class="mini-card-label">Avg Views</div><div class="mini-card-value">{fmt(avg_views)}</div><div class="mini-card-sub">per video</div></div>', unsafe_allow_html=True)

    # Card 4 — Engagement bar chart
    with m4:
        subs_val = summary.get("subscriber_count", 0)
        fig_e = go.Figure(go.Bar(
            x=["Subs", "Likes", "Comments"],
            y=[min(subs_val//1000, 9999), min(total_likes//100, 9999), min(total_comments//10, 9999)],
            marker_color=['#6d28d9', '#8b5cf6', '#c084fc'],
            hovertemplate="%{x}<extra></extra>"
        ))
        fig_e.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=4, b=4, l=4, r=4), height=80,
            xaxis=dict(tickfont=dict(color='#5050a0', size=8), showgrid=False),
            yaxis=dict(visible=False), showlegend=False, bargap=0.25
        )
        st.markdown('<div class="mini-card"><div class="mini-card-label">Engagement</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_e, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f'<div class="mini-card-sub"><span class="{eng_pill}">{engagement}% engagement rate</span></div></div>', unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # SECTION 3 — LINE CHART (left big) + PIE CHART (right)
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sec-title">Analytics Deep Dive</p>', unsafe_allow_html=True)

    left_chart, right_chart = st.columns([2, 1], gap="medium")

    with left_chart:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-card-title">Upload Insights — Videos per Month</div>', unsafe_allow_html=True)

        if monthly_data:
            months = [r[0] for r in monthly_data]
            counts = [r[1] for r in monthly_data]
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=months, y=counts, mode='lines',
                line=dict(color='#a855f7', width=2.5, shape='spline'),
                fill='tozeroy', fillcolor='rgba(168,85,247,0.07)',
                hovertemplate="<b>%{x}</b><br>%{y} videos<extra></extra>"
            ))
            fig_line.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#6060a0', family='Outfit', size=10),
                height=260, margin=dict(t=10, b=30, l=35, r=15),
                xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#4a4a80', size=9), tickangle=-30),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', zeroline=False, tickfont=dict(color='#4a4a80', size=9)),
                showlegend=False, hovermode='x unified'
            )
            st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="height:260px;display:flex;align-items:center;justify-content:center;color:#3a3a60;">No data for selected range</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with right_chart:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-card-title">Videos by Month (%)</div>', unsafe_allow_html=True)

        if monthly_data:
            PURPLES = ["#7c3aed","#8b5cf6","#a78bfa","#6d28d9","#5b21b6","#9333ea","#c084fc","#d8b4fe","#4c1d95","#7e22ce","#581c87","#ede9fe"]
            fig_pie = go.Figure(data=[go.Pie(
                labels=[r[0] for r in monthly_data],
                values=[r[1] for r in monthly_data],
                hole=0.5, textinfo='percent',
                textfont=dict(size=9, color='#fff'),
                hovertemplate="<b>%{label}</b><br>%{value} videos · %{percent}<extra></extra>",
                marker=dict(colors=PURPLES[:len(monthly_data)], line=dict(color='#0d0d1a', width=2))
            )])
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#7070a0', family='Outfit'),
                height=260, margin=dict(t=10, b=10, l=10, r=80),
                legend=dict(font=dict(size=8, color='#6060a0'), bgcolor='rgba(0,0,0,0)', orientation='v', x=1.0, y=0.5),
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="height:260px;display:flex;align-items:center;justify-content:center;color:#3a3a60;">No data</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # SECTION 4 — PERFORMANCE METRICS ROW
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sec-title">Performance Metrics</p>', unsafe_allow_html=True)

    pm1, pm2, pm3, pm4 = st.columns(4, gap="medium")
    with pm1: st.metric("📽️ Videos in Range", f"{total_vids:,}")
    with pm2: st.metric("👁️ Avg Views / Video", fmt(avg_views), delta="per video")
    with pm3: st.metric("👍 Total Likes", fmt(total_likes), delta="in range")
    with pm4:
        color = "🟢" if engagement > 5 else ("🟡" if engagement > 2 else "🔴")
        st.metric(f"{color} Engagement Rate", f"{engagement}%", delta="likes ÷ views")

    # ═════════════════════════════════════════════════════════════════════════
    # SECTION 5 — TOP 10 VIDEOS TABLE
    # ═════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sec-title">Top 10 Most Viewed Videos</p>', unsafe_allow_html=True)

    if top_videos:
        df = pd.DataFrame(top_videos, columns=["Video ID","Title","Views","Likes","Comments","Duration (s)"])
        df.index = df.index + 1
        df["Views"]    = df["Views"].apply(lambda x: f"{x:,}")
        df["Likes"]    = df["Likes"].apply(lambda x: f"{x:,}")
        df["Comments"] = df["Comments"].apply(lambda x: f"{x:,}")
        df["Duration"] = df["Duration (s)"].apply(lambda x: f"{int(x)//60}m {int(x)%60}s")
        st.dataframe(df[["Title","Views","Likes","Comments","Duration"]], use_container_width=True, height=360)
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#3a3a60;">No videos found for this date range.</div>', unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style='text-align:center;padding:5rem 2rem;'>
        <div style='font-size:3rem;'>▶️</div>
        <div style='font-size:1.2rem;font-weight:600;color:#4a3a6a;margin-top:1rem;'>
            Enter a Channel ID above and click Analyse Channel
        </div>
        <div style='font-size:0.85rem;color:#35305a;margin-top:0.5rem;'>
            Your full dashboard will appear once data is loaded
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)