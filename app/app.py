import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import pickle
import re
import os
from datetime import datetime
import time

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SentiFlow AI · Social Media Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS  — Cyberpunk / Glassmorphism SaaS Theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── CSS Variables ── */
:root {
  --bg-void:      #03040a;
  --bg-deep:      #060912;
  --bg-card:      rgba(8, 12, 28, 0.82);
  --bg-glass:     rgba(12, 18, 40, 0.70);
  --border-dim:   rgba(0, 212, 255, 0.10);
  --border-glow:  rgba(0, 212, 255, 0.30);
  --cyan:         #00d4ff;
  --cyan-dim:     rgba(0, 212, 255, 0.15);
  --magenta:      #ff006e;
  --magenta-dim:  rgba(255, 0, 110, 0.15);
  --green:        #00ff9f;
  --green-dim:    rgba(0, 255, 159, 0.12);
  --amber:        #ffb300;
  --amber-dim:    rgba(255, 179, 0, 0.12);
  --purple:       #9d4edd;
  --text-primary: #e8f4ff;
  --text-muted:   #4a6080;
  --text-dim:     #1e3050;
  --font-display: 'Orbitron', monospace;
  --font-body:    'Rajdhani', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg-void) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}

/* ── Animated background ── */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 90% 60% at 5% 0%,   rgba(0,212,255,.09) 0%, transparent 55%),
    radial-gradient(ellipse 70% 50% at 95% 100%, rgba(157,78,221,.09) 0%, transparent 55%),
    radial-gradient(ellipse 50% 40% at 50% 50%,  rgba(0,255,159,.04) 0%, transparent 60%),
    var(--bg-void);
  pointer-events: none;
}

/* Scanline overlay */
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed; inset: 0; z-index: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,212,255,.012) 2px,
    rgba(0,212,255,.012) 4px
  );
  pointer-events: none;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.main .block-container {
  padding: 0 2rem 5rem !important;
  max-width: 1520px;
  position: relative; z-index: 1;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: rgba(4, 7, 18, 0.96) !important;
  border-right: 1px solid var(--border-dim) !important;
  backdrop-filter: blur(30px);
}
[data-testid="stSidebar"] * { font-family: var(--font-body) !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: #3a5070 !important; font-size: .82rem !important; letter-spacing: .04em; }

/* ── Inputs ── */
[data-testid="stTextArea"] textarea {
  background: rgba(4, 10, 26, 0.90) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-size: .95rem !important;
  letter-spacing: .03em !important;
  padding: 1rem !important;
  transition: border-color .25s, box-shadow .25s !important;
  resize: none !important;
}
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 2px rgba(0,212,255,.12), 0 0 20px rgba(0,212,255,.08) !important;
  outline: none !important;
}
[data-testid="stTextArea"] label { color: var(--text-muted) !important; font-size: .78rem !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
  background: transparent !important;
  border: 1px solid var(--cyan) !important;
  border-radius: 6px !important;
  color: var(--cyan) !important;
  font-family: var(--font-display) !important;
  font-size: .72rem !important;
  font-weight: 700 !important;
  letter-spacing: .15em !important;
  padding: .75rem 1.5rem !important;
  text-transform: uppercase !important;
  width: 100% !important;
  position: relative !important;
  overflow: hidden !important;
  transition: color .2s, box-shadow .2s, background .2s !important;
}
[data-testid="stButton"] > button::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(0,212,255,.15), rgba(157,78,221,.1));
  opacity: 0; transition: opacity .2s;
}
[data-testid="stButton"] > button:hover {
  color: #fff !important;
  box-shadow: 0 0 24px rgba(0,212,255,.35), 0 0 60px rgba(0,212,255,.12) !important;
}
[data-testid="stButton"] > button:hover::before { opacity: 1; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
  background: rgba(4,10,26,.9) !important;
  border: 1px solid var(--border-dim) !important;
  border-radius: 6px !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}
[data-testid="stSlider"] .stSlider { accent-color: var(--cyan); }
[data-testid="stMarkdownContainer"] p { color: #4a6080 !important; line-height: 1.7 !important; font-family: var(--font-body) !important; }

/* ══════════════════════════════════════
   HERO
══════════════════════════════════════ */
.hero {
  position: relative;
  padding: 3rem 3rem 2.5rem;
  margin: 0 -2rem 2.5rem;
  border-bottom: 1px solid var(--border-dim);
  overflow: hidden;
}
.hero-bg {
  position: absolute; inset: 0;
  background:
    linear-gradient(135deg, rgba(0,212,255,.07) 0%, rgba(157,78,221,.05) 50%, rgba(0,255,159,.04) 100%);
}
.hero-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(var(--border-dim) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-dim) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: linear-gradient(to bottom, transparent 0%, black 20%, black 80%, transparent 100%);
}
.hero-corner {
  position: absolute; top: 1.5rem; right: 2rem;
  width: 80px; height: 80px;
  border-top: 2px solid var(--cyan);
  border-right: 2px solid var(--cyan);
  opacity: .35;
}
.hero-corner-bl {
  position: absolute; bottom: 1.5rem; left: 2rem;
  width: 50px; height: 50px;
  border-bottom: 2px solid var(--cyan);
  border-left: 2px solid var(--cyan);
  opacity: .2;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: .5rem;
  background: rgba(0,212,255,.08);
  border: 1px solid rgba(0,212,255,.25);
  border-radius: 3px;
  padding: .3rem 1rem;
  font-family: var(--font-mono);
  font-size: .65rem; font-weight: 400; letter-spacing: .15em;
  color: var(--cyan); text-transform: uppercase;
  margin-bottom: 1.2rem;
  animation: fadeIn .6s ease both;
}
.status-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  animation: blink 1.8s ease-in-out infinite;
}
.hero h1 {
  font-family: var(--font-display) !important;
  font-size: clamp(1.8rem, 3.5vw, 3rem) !important;
  font-weight: 900 !important;
  line-height: 1.05 !important;
  color: var(--text-primary) !important;
  letter-spacing: .04em !important;
  text-transform: uppercase !important;
  animation: fadeIn .7s .1s ease both;
}
.hero h1 .c1 { color: var(--cyan); }
.hero h1 .c2 {
  background: linear-gradient(90deg, var(--cyan), var(--purple));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
  margin-top: .7rem;
  font-family: var(--font-body);
  font-size: .95rem; font-weight: 300; letter-spacing: .06em;
  color: var(--text-muted); max-width: 600px; line-height: 1.6;
  animation: fadeIn .7s .2s ease both;
}
.hero-pills {
  display: flex; gap: 1.5rem; margin-top: 1.8rem; flex-wrap: wrap;
  animation: fadeIn .7s .3s ease both;
}
.hero-pill {
  display: flex; align-items: center; gap: .55rem;
  font-family: var(--font-mono); font-size: .65rem;
  color: var(--text-muted); letter-spacing: .08em;
}
.hero-pill .val {
  font-family: var(--font-display); font-size: .9rem; font-weight: 700;
  color: var(--text-primary);
}
.hero-pill .bar {
  width: 1px; height: 28px; background: var(--border-dim);
  margin: 0 .3rem;
}

/* ══════════════════════════════════════
   KPI CARDS
══════════════════════════════════════ */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: .9rem; margin-bottom: 1.8rem; }
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border-dim);
  border-radius: 8px;
  padding: 1.2rem 1.4rem;
  backdrop-filter: blur(20px);
  position: relative; overflow: hidden;
  animation: fadeUp .5s ease both;
  transition: border-color .25s, box-shadow .25s, transform .2s;
  cursor: default;
}
.kpi-card::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, var(--accent-color, rgba(0,212,255,.05)), transparent 60%);
}
.kpi-card::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: var(--accent-line, linear-gradient(90deg, var(--cyan), transparent));
  box-shadow: var(--accent-shadow, 0 0 12px rgba(0,212,255,.4));
}
.kpi-card:hover {
  border-color: var(--border-glow);
  box-shadow: 0 0 30px rgba(0,212,255,.08);
  transform: translateY(-2px);
}
.kpi-top { display: flex; justify-content: space-between; align-items: flex-start; }
.kpi-icon { font-size: 1.1rem; opacity: .7; }
.kpi-tag {
  font-family: var(--font-mono); font-size: .55rem; letter-spacing: .1em;
  color: var(--text-dim); text-transform: uppercase;
  background: rgba(0,212,255,.06); border: 1px solid var(--border-dim);
  border-radius: 3px; padding: .15rem .4rem;
}
.kpi-val {
  font-family: var(--font-display);
  font-size: 2rem; font-weight: 900; color: var(--text-primary);
  line-height: 1; margin: .7rem 0 .2rem;
}
.kpi-lbl {
  font-family: var(--font-body); font-size: .72rem; letter-spacing: .08em;
  text-transform: uppercase; color: var(--text-muted); font-weight: 500;
}
.kpi-delta { font-size: .72rem; margin-top: .5rem; font-family: var(--font-mono); }
.kpi-delta.up { color: var(--green); }
.kpi-delta.dn { color: var(--magenta); }
.kpi-delta.nu { color: var(--amber); }

/* ══════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════ */
.sec-header {
  display: flex; align-items: center; gap: .8rem; margin-bottom: 1.1rem;
}
.sec-header .ico {
  width: 28px; height: 28px; border-radius: 4px;
  background: var(--cyan-dim); border: 1px solid rgba(0,212,255,.2);
  display: flex; align-items: center; justify-content: center;
  font-size: .85rem;
}
.sec-header h3 {
  font-family: var(--font-display) !important;
  font-size: .68rem !important; font-weight: 700 !important;
  letter-spacing: .2em !important; text-transform: uppercase !important;
  color: var(--cyan) !important;
}
.sec-header .line {
  flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(0,212,255,.2), transparent);
}

/* ══════════════════════════════════════
   GLASS CARD
══════════════════════════════════════ */
.g-card {
  background: var(--bg-glass);
  border: 1px solid var(--border-dim);
  border-radius: 10px;
  backdrop-filter: blur(20px);
  padding: 1.4rem 1.6rem;
  position: relative; overflow: hidden;
  animation: fadeUp .5s ease both;
  transition: border-color .25s, box-shadow .25s;
}
.g-card:hover { border-color: rgba(0,212,255,.18); }
.g-card-label {
  font-family: var(--font-mono); font-size: .6rem; letter-spacing: .15em;
  text-transform: uppercase; color: var(--text-dim); margin-bottom: .6rem;
}
.g-card-title {
  font-family: var(--font-display); font-size: .9rem; font-weight: 700;
  color: var(--text-primary); letter-spacing: .05em;
}

/* ══════════════════════════════════════
   PREDICTION RESULT
══════════════════════════════════════ */
.pred-card {
  border-radius: 10px; padding: 1.8rem 2rem;
  position: relative; overflow: hidden;
  animation: glowReveal .6s cubic-bezier(.22,1,.36,1) both;
  margin-top: 1rem;
}
.pred-card.positive {
  background: linear-gradient(135deg, rgba(0,255,159,.08), rgba(0,212,255,.05));
  border: 1px solid rgba(0,255,159,.3);
}
.pred-card.negative {
  background: linear-gradient(135deg, rgba(255,0,110,.1), rgba(157,78,221,.05));
  border: 1px solid rgba(255,0,110,.3);
}
.pred-card.neutral {
  background: linear-gradient(135deg, rgba(255,179,0,.08), rgba(255,255,255,.03));
  border: 1px solid rgba(255,179,0,.3);
}
.pred-glow {
  position: absolute; top: -60px; right: -60px;
  width: 200px; height: 200px; border-radius: 50%;
  opacity: .12; filter: blur(50px);
}
.pred-glow.positive { background: var(--green); }
.pred-glow.negative { background: var(--magenta); }
.pred-glow.neutral  { background: var(--amber); }
.pred-top { display: flex; align-items: center; gap: 1.2rem; }
.pred-emoji { font-size: 2.8rem; line-height: 1; }
.pred-info { flex: 1; }
.pred-label {
  font-family: var(--font-display);
  font-size: 1.8rem; font-weight: 900; letter-spacing: .06em;
}
.pred-label.positive { color: var(--green); }
.pred-label.negative { color: var(--magenta); }
.pred-label.neutral  { color: var(--amber); }
.pred-meta {
  font-family: var(--font-mono); font-size: .65rem; letter-spacing: .1em;
  color: var(--text-muted); margin-top: .3rem;
}
.pred-conf-bar {
  margin-top: 1rem; background: rgba(255,255,255,.06);
  border-radius: 999px; height: 4px; overflow: hidden;
}
.pred-conf-fill {
  height: 100%; border-radius: 999px;
  transition: width 1s cubic-bezier(.22,1,.36,1);
}
.pred-conf-fill.positive { background: linear-gradient(90deg, var(--green), var(--cyan)); }
.pred-conf-fill.negative { background: linear-gradient(90deg, var(--magenta), var(--purple)); }
.pred-conf-fill.neutral  { background: linear-gradient(90deg, var(--amber), #ff6b35); }

/* ══════════════════════════════════════
   BUSINESS INSIGHT CARD
══════════════════════════════════════ */
.insight-card {
  background: rgba(0, 212, 255, 0.04);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-left: 3px solid var(--cyan);
  border-radius: 8px; padding: 1.2rem 1.4rem;
  margin-top: 1rem; animation: fadeUp .5s .1s ease both;
}
.insight-title {
  font-family: var(--font-display); font-size: .65rem; font-weight: 700;
  letter-spacing: .18em; text-transform: uppercase; color: var(--cyan);
  margin-bottom: .6rem; display: flex; align-items: center; gap: .5rem;
}
.insight-body {
  font-family: var(--font-body); font-size: .92rem; font-weight: 400;
  line-height: 1.7; color: #8aaccc; letter-spacing: .03em;
}
.insight-rec {
  margin-top: .8rem; padding-top: .8rem;
  border-top: 1px solid rgba(0,212,255,.08);
  font-family: var(--font-mono); font-size: .68rem;
  color: var(--text-dim); letter-spacing: .06em;
}
.insight-rec span { color: var(--cyan); }

/* ══════════════════════════════════════
   XAI — KEYWORDS
══════════════════════════════════════ */
.xai-card {
  background: var(--bg-glass);
  border: 1px solid var(--border-dim);
  border-radius: 10px; padding: 1.2rem 1.4rem;
  margin-top: 1rem; animation: fadeUp .5s .15s ease both;
}
.xai-title {
  font-family: var(--font-display); font-size: .65rem; letter-spacing: .18em;
  text-transform: uppercase; color: var(--purple); margin-bottom: .9rem;
}
.kw-row { display: flex; flex-wrap: wrap; gap: .45rem; }
.kw-chip {
  font-family: var(--font-mono); font-size: .68rem; letter-spacing: .06em;
  border-radius: 4px; padding: .3rem .7rem;
  display: flex; align-items: center; gap: .35rem;
}
.kw-chip.pos {
  background: rgba(0,255,159,.1); border: 1px solid rgba(0,255,159,.2);
  color: var(--green);
}
.kw-chip.neg {
  background: rgba(255,0,110,.1); border: 1px solid rgba(255,0,110,.2);
  color: var(--magenta);
}
.kw-chip .kw-score {
  opacity: .6; font-size: .6rem;
}

/* ══════════════════════════════════════
   HISTORY ITEMS
══════════════════════════════════════ */
.hist-item {
  display: flex; align-items: center; gap: .9rem;
  padding: .8rem 1.1rem;
  background: rgba(5, 10, 24, 0.6);
  border: 1px solid var(--border-dim);
  border-radius: 7px; margin-bottom: .5rem;
  transition: background .2s, border-color .2s;
  animation: fadeUp .4s ease both;
}
.hist-item:hover {
  background: rgba(0,212,255,.04);
  border-color: rgba(0,212,255,.15);
}
.hist-badge {
  flex-shrink: 0; border-radius: 4px;
  padding: .25rem .6rem;
  font-family: var(--font-mono); font-size: .6rem; letter-spacing: .08em;
  text-transform: uppercase; font-weight: 600;
}
.hist-badge.positive { background: rgba(0,255,159,.12); color: var(--green); border: 1px solid rgba(0,255,159,.2); }
.hist-badge.negative { background: rgba(255,0,110,.12);  color: var(--magenta); border: 1px solid rgba(255,0,110,.2); }
.hist-badge.neutral  { background: rgba(255,179,0,.12);  color: var(--amber); border: 1px solid rgba(255,179,0,.2); }
.hist-text  { flex: 1; font-size: .82rem; color: var(--text-muted); line-height: 1.4; font-family: var(--font-body); }
.hist-score { font-family: var(--font-display); font-size: .8rem; font-weight: 700; color: var(--text-primary); }
.hist-time  { font-family: var(--font-mono); font-size: .6rem; color: var(--text-dim); }
.hist-idx   { font-family: var(--font-mono); font-size: .6rem; color: var(--text-dim); opacity: .5; }

/* ══════════════════════════════════════
   EXEC SUMMARY
══════════════════════════════════════ */
.exec-card {
  background: linear-gradient(135deg, rgba(157,78,221,.07), rgba(0,212,255,.04));
  border: 1px solid rgba(157,78,221,.2);
  border-radius: 10px; padding: 1.4rem 1.6rem;
  margin-top: 1rem; animation: fadeUp .5s .2s ease both;
}
.exec-title {
  font-family: var(--font-display); font-size: .65rem; letter-spacing: .18em;
  text-transform: uppercase; color: var(--purple); margin-bottom: .8rem;
  display: flex; align-items: center; gap: .5rem;
}
.exec-line {
  font-family: var(--font-body); font-size: .88rem; line-height: 1.75;
  color: #7090b0; letter-spacing: .03em;
}
.exec-metric-row {
  display: flex; gap: 1.5rem; margin-top: 1rem;
  padding-top: 1rem; border-top: 1px solid rgba(157,78,221,.1);
}
.exec-metric { text-align: center; }
.exec-m-val {
  font-family: var(--font-display); font-size: 1.2rem; font-weight: 900;
  color: var(--text-primary);
}
.exec-m-lbl {
  font-family: var(--font-mono); font-size: .58rem; letter-spacing: .1em;
  color: var(--text-dim); text-transform: uppercase;
}

/* ══════════════════════════════════════
   SIDEBAR STYLING
══════════════════════════════════════ */
.sb-header {
  padding: .5rem 0 1.5rem;
  border-bottom: 1px solid var(--border-dim);
  margin-bottom: 1.2rem;
}
.sb-logo-row { display: flex; align-items: center; gap: .7rem; margin-bottom: .3rem; }
.sb-logo-box {
  width: 34px; height: 34px; border-radius: 6px;
  background: linear-gradient(135deg, var(--cyan), var(--purple));
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 20px rgba(0,212,255,.3);
}
.sb-logo-letter {
  font-family: var(--font-display); font-size: .9rem; font-weight: 900;
  color: #fff; letter-spacing: 0;
}
.sb-name {
  font-family: var(--font-display); font-size: .82rem; font-weight: 700;
  color: var(--text-primary); letter-spacing: .1em;
}
.sb-tagline {
  font-family: var(--font-mono); font-size: .58rem; letter-spacing: .1em;
  color: var(--text-dim); text-transform: uppercase; margin-left: .1rem;
}
.sb-section {
  font-family: var(--font-mono); font-size: .58rem; letter-spacing: .15em;
  text-transform: uppercase; color: var(--text-dim); margin: 1.2rem 0 .5rem;
}
.sb-divider { height: 1px; background: var(--border-dim); margin: .8rem 0; }
.sb-metric {
  display: flex; justify-content: space-between; align-items: center;
  padding: .5rem 0; border-bottom: 1px solid rgba(255,255,255,.03);
}
.sb-m-lbl { font-family: var(--font-body); font-size: .78rem; color: #2a4060; letter-spacing: .05em; }
.sb-m-val { font-family: var(--font-display); font-size: .82rem; font-weight: 700; color: var(--text-primary); }
.sb-status {
  display: flex; align-items: center; gap: .5rem; margin-top: 1rem;
  background: rgba(0,255,159,.05); border: 1px solid rgba(0,255,159,.15);
  border-radius: 5px; padding: .5rem .8rem;
}
.sb-status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); animation: blink 1.8s infinite; }
.sb-status-txt { font-family: var(--font-mono); font-size: .62rem; letter-spacing: .08em; color: var(--green); }

/* ══════════════════════════════════════
   EXAMPLE PILLS
══════════════════════════════════════ */
.pill-row { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .8rem; }
.e-pill {
  background: rgba(0,212,255,.05);
  border: 1px solid rgba(0,212,255,.12);
  border-radius: 4px; padding: .3rem .75rem;
  font-family: var(--font-mono); font-size: .65rem; letter-spacing: .05em;
  color: #3a6080; cursor: default; transition: background .2s, border-color .2s, color .2s;
}
.e-pill:hover { background: rgba(0,212,255,.1); border-color: rgba(0,212,255,.25); color: var(--cyan); }

/* ══════════════════════════════════════
   ANIMATIONS
══════════════════════════════════════ */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes glowReveal {
  from { opacity: 0; transform: scale(.96) translateY(8px); filter: blur(4px); }
  to   { opacity: 1; transform: scale(1)   translateY(0);   filter: blur(0); }
}
@keyframes blink {
  0%,100% { opacity: 1; }
  50%      { opacity: .35; }
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

/* ── Footer ── */
.footer {
  margin-top: 4rem; padding-top: 1.5rem;
  border-top: 1px solid var(--border-dim);
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: .5rem;
}
.footer-brand { font-family: var(--font-display); font-size: .7rem; font-weight: 700; color: var(--text-dim); letter-spacing: .1em; }
.footer-copy  { font-family: var(--font-mono); font-size: .62rem; color: var(--text-dim); opacity: .5; letter-spacing: .06em; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODEL LOADING
# ══════════════════════════════════════════════════════════════════════════════
def _load_file(path: str):
    """Try joblib first (scikit-learn default), then fall back to pickle."""
    try:
        import joblib
        return joblib.load(path)
    except Exception:
        pass
    import pickle as _pickle
    with open(path, "rb") as f:
        return _pickle.load(f)

@st.cache_resource(show_spinner=False)
def load_model():
    model_path = os.path.join("models", "sentiment_model.pkl")
    vec_path   = os.path.join("models", "tfidf_vectorizer.pkl")
    try:
        model      = _load_file(model_path)
        vectorizer = _load_file(vec_path)
        return model, vectorizer, True
    except FileNotFoundError:
        return None, None, False
    except Exception as e:
        return None, None, False

model, vectorizer, model_loaded = load_model()

# ══════════════════════════════════════════════════════════════════════════════
#  INFERENCE
# ══════════════════════════════════════════════════════════════════════════════
def clean_text(text: str) -> str:
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def predict_sentiment(text: str) -> dict:
    """
    Real inference via loaded scikit-learn model + TF-IDF vectorizer.
    Returns dict with label, confidence, and per-class probabilities.
    """
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])

    label_raw = model.predict(vec)[0]

    # Normalise label to standard form
    label_map = {
        "positive": "Positive", "pos": "Positive", "1": "Positive", 1: "Positive", 2: "Positive",
        "negative": "Negative", "neg": "Negative", "0": "Negative", 0: "Negative",
        "neutral":  "Neutral",  "neu": "Neutral",   "2": "Neutral",
    }
    label = label_map.get(str(label_raw).lower(), str(label_raw).capitalize())
    if label not in ("Positive", "Negative", "Neutral"):
        label = "Neutral"

    # Probabilities
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(vec)[0]
        classes = [label_map.get(str(c).lower(), str(c)) for c in model.classes_]
        prob_dict = {}
        for cls, p in zip(classes, proba):
            norm_cls = label_map.get(str(cls).lower(), str(cls).capitalize())
            prob_dict[norm_cls] = prob_dict.get(norm_cls, 0) + float(p)
        pos_p = prob_dict.get("Positive", 0.0)
        neg_p = prob_dict.get("Negative", 0.0)
        neu_p = prob_dict.get("Neutral",  0.0)
        # Normalise to 1
        total = pos_p + neg_p + neu_p or 1.0
        pos_p /= total; neg_p /= total; neu_p /= total
    else:
        # Decision function fallback
        if hasattr(model, "decision_function"):
            df = model.decision_function(vec)[0]
            df = np.atleast_1d(df)
            proba = np.exp(df) / np.sum(np.exp(df))
            if len(proba) == 3:
                neg_p, neu_p, pos_p = proba
            elif len(proba) == 2:
                neg_p, pos_p = proba; neu_p = 0.0
            else:
                pos_p = 0.8 if label == "Positive" else 0.1
                neg_p = 0.8 if label == "Negative" else 0.1
                neu_p = 1 - pos_p - neg_p
        else:
            pos_p = 0.80 if label == "Positive" else 0.08
            neg_p = 0.80 if label == "Negative" else 0.08
            neu_p = max(0, 1 - pos_p - neg_p)

    confidence = {"Positive": pos_p, "Negative": neg_p, "Neutral": neu_p}[label]
    return {
        "label": label, "confidence": float(confidence),
        "positive": float(pos_p), "negative": float(neg_p), "neutral": float(neu_p),
        "cleaned": cleaned,
    }

# ══════════════════════════════════════════════════════════════════════════════
#  EXPLAINABLE AI  (TF-IDF keyword importance)
# ══════════════════════════════════════════════════════════════════════════════
def get_keywords(text: str, result: dict) -> tuple[list, list]:
    """Extract top positive / negative influencing tokens via TF-IDF weights."""
    cleaned = result["cleaned"]
    vec_matrix = vectorizer.transform([cleaned])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = vec_matrix.toarray()[0]

    # Get words actually in the text
    tokens_in_text = [(feature_names[i], tfidf_scores[i])
                      for i in tfidf_scores.nonzero()[0]]
    tokens_in_text.sort(key=lambda x: x[1], reverse=True)

    # Split by sentiment heuristics
    POS_WORDS = {"love","great","amazing","awesome","excellent","good","best","happy",
                 "wonderful","fantastic","incredible","outstanding","perfect","brilliant",
                 "superb","nice","glad","joy","enjoy","helpful","recommend","fast","easy"}
    NEG_WORDS = {"hate","terrible","awful","bad","worst","horrible","disgusting",
                 "disappointing","poor","useless","fail","broken","wrong","sad","angry",
                 "slow","never","not","can't","worst","trash","waste","scam","rude","awful"}

    pos_kw, neg_kw = [], []
    for word, score in tokens_in_text[:20]:
        if word in POS_WORDS:
            pos_kw.append((word, score))
        elif word in NEG_WORDS:
            neg_kw.append((word, score))
        elif result["label"] == "Positive" and len(pos_kw) < 5:
            pos_kw.append((word, score))
        elif result["label"] == "Negative" and len(neg_kw) < 5:
            neg_kw.append((word, score))

    return pos_kw[:5], neg_kw[:5]

# ══════════════════════════════════════════════════════════════════════════════
#  BUSINESS INSIGHT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
INSIGHTS = {
    "Positive": {
        "high":   ("🟢 Customers are expressing strong satisfaction and brand loyalty. This content signals positive word-of-mouth potential and a high likelihood of organic advocacy.",
                   "→ AMPLIFY: Engage with this user. Feature as a testimonial candidate."),
        "medium": ("🟡 Moderately positive sentiment detected. Users show general approval with moderate enthusiasm. Engagement opportunity exists.",
                   "→ NURTURE: Respond with appreciation and deepen the relationship."),
        "low":    ("⚪ Mild positivity with uncertainty. The signal is favourable but weak — further context may refine the picture.",
                   "→ MONITOR: Track follow-up engagement for sentiment drift."),
    },
    "Negative": {
        "high":   ("🔴 High-risk negative signal detected. Customer is expressing strong dissatisfaction — potential churn, escalation, or viral complaint risk.",
                   "→ ESCALATE: Prioritise immediate response. Route to senior support."),
        "medium": ("🟠 Negative sentiment with moderate intensity. Customer experience friction identified. Service recovery is feasible at this stage.",
                   "→ RESPOND: Acknowledge and offer a resolution within 2 hours."),
        "low":    ("🟡 Mild negative tone. Minor friction point identified. Low churn risk but worth addressing proactively.",
                   "→ ENGAGE: Proactive response can convert this to a positive outcome."),
    },
    "Neutral": {
        "high":   ("⚪ Neutral sentiment with high confidence. Informational or observational content — neither brand advocacy nor detraction.",
                   "→ TRACK: Monitor for sentiment shift in replies or follow-up posts."),
        "medium": ("⚪ Balanced sentiment. User is describing an experience without strong emotional colouring.",
                   "→ ANALYSE: Identify latent needs or unanswered questions in the content."),
        "low":    ("⚪ Ambiguous content — borderline neutral. Human review recommended for nuanced contexts.",
                   "→ REVIEW: Flag for manual inspection in brand monitoring workflow."),
    },
}

def get_business_insight(label: str, confidence: float) -> tuple[str, str]:
    tier = "high" if confidence >= .70 else ("medium" if confidence >= .45 else "low")
    body, rec = INSIGHTS[label][tier]
    return body, rec

# ══════════════════════════════════════════════════════════════════════════════
#  EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
def get_exec_summary(history: list) -> str:
    if not history:
        return "No data available yet. Analyse tweets to generate an executive summary."
    total = len(history)
    pos_r = sum(1 for r in history if r["label"] == "Positive") / total
    neg_r = sum(1 for r in history if r["label"] == "Negative") / total
    neu_r = sum(1 for r in history if r["label"] == "Neutral")  / total
    avg_c = np.mean([r["confidence"] for r in history])
    dominant = max([("Positive", pos_r), ("Negative", neg_r), ("Neutral", neu_r)], key=lambda x: x[1])[0]
    risk = "HIGH" if neg_r > .40 else ("MODERATE" if neg_r > .20 else "LOW")

    risk_color  = "#ff006e" if risk == "HIGH" else ("#ffb300" if risk == "MODERATE" else "#00ff9f")
    risk_icon   = "⚠ " if risk != "LOW" else ""
    conf_word   = "reliable" if avg_c > .7 else "moderate"
    plural_s    = "s" if total > 1 else ""

    lines = [
        f"Analysis of {total} social media record{plural_s} yields a <b>{dominant.upper()}</b>-dominant sentiment profile "
        f"({pos_r:.0%} positive · {neg_r:.0%} negative · {neu_r:.0%} neutral).",
        f"Average model confidence stands at <b>{avg_c:.1%}</b>, indicating {conf_word} signal quality.",
        f"Brand risk level assessed as <b style='color: {risk_color}'>{risk_icon}{risk}</b>.",
    ]
    return " ".join(lines)

# ══════════════════════════════════════════════════════════════════════════════
#  PLOTLY CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font_family="Rajdhani", font_color="#4a6080",
    margin=dict(t=10, b=30, l=10, r=10),
)

def make_gauge(value: float, color: str, title: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(value * 100, 1),
        number={"suffix": "%", "font": {"size": 26, "color": "#e8f4ff", "family": "Orbitron"}},
        title={"text": title.upper(), "font": {"size": 10, "color": "#2a4060", "family": "Orbitron"}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"color": "#1e3050", "size": 8},
                     "tickcolor": "#0d1a30", "gridcolor": "#0d1a30"},
            "bar": {"color": color, "thickness": .18},
            "bgcolor": "rgba(0,0,0,0)", "bordercolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0,  33], "color": "rgba(10,18,40,.6)"},
                {"range": [33, 66], "color": "rgba(10,18,40,.4)"},
                {"range": [66,100], "color": "rgba(10,18,40,.2)"},
            ],
            "threshold": {"line": {"color": color, "width": 2},
                          "thickness": .65, "value": value * 100},
        },
    ))
    fig.update_layout(height=180, **CHART_LAYOUT, margin=dict(t=28, b=8, l=16, r=16))
    return fig

def make_donut(pos, neg, neu) -> go.Figure:
    total = pos + neg + neu or 1
    fig = go.Figure(go.Pie(
        labels=["Positive", "Negative", "Neutral"],
        values=[pos/total, neg/total, neu/total],
        hole=.72,
        marker=dict(colors=["#00ff9f", "#ff006e", "#ffb300"],
                    line=dict(color="#03040a", width=4)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text=f"{round(pos/total*100)}%", x=.5, y=.56, showarrow=False,
                       font=dict(size=20, color="#e8f4ff", family="Orbitron"), font_weight=900)
    fig.add_annotation(text="POSITIVE", x=.5, y=.41, showarrow=False,
                       font=dict(size=8, color="#2a4060", family="Orbitron"))
    fig.update_layout(height=200, showlegend=True,
                      legend=dict(font=dict(size=9, color="#4a6080", family="Rajdhani"),
                                  bgcolor="rgba(0,0,0,0)", orientation="h", x=.5, xanchor="center", y=-.05),
                      **CHART_LAYOUT, margin=dict(t=8, b=20, l=8, r=8))
    return fig

def make_confidence_trend(history) -> go.Figure:
    if len(history) < 2:
        return go.Figure()
    df = pd.DataFrame(history[-25:])
    idx = list(range(len(df)))
    colors_map = {"Positive": "#00ff9f", "Negative": "#ff006e", "Neutral": "#ffb300"}
    bar_colors  = [colors_map.get(l, "#00d4ff") for l in df["label"]]

    fig = go.Figure(go.Bar(
        x=idx, y=df["confidence"],
        marker=dict(color=bar_colors, line=dict(width=0), cornerradius=4),
        hovertemplate="<b>#%{x}</b> · %{customdata}<br>Confidence: %{y:.1%}<extra></extra>",
        customdata=df["label"],
    ))
    fig.update_layout(
        height=190, bargap=.3,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#1e3050", size=8)),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,212,255,.06)", zeroline=False,
                   tickformat=".0%", tickfont=dict(color="#1e3050", size=8), range=[0, 1]),
        **CHART_LAYOUT,
    )
    return fig

def make_trend_lines(history) -> go.Figure:
    if len(history) < 2:
        return go.Figure()
    df = pd.DataFrame(history[-30:])
    fig = go.Figure()
    for col, name, color, fill_color in [
        ("positive", "Positive", "#00ff9f", "rgba(0,255,159,.06)"),
        ("negative", "Negative", "#ff006e", "rgba(255,0,110,.06)"),
        ("neutral",  "Neutral",  "#ffb300", "rgba(255,179,0,.05)"),
    ]:
        fig.add_trace(go.Scatter(
            y=df[col], name=name,
            line=dict(color=color, width=2),
            fill="tozeroy", fillcolor=fill_color,
            mode="lines",
            hovertemplate=f"<b>{name}</b>: %{{y:.1%}}<extra></extra>",
        ))
    fig.update_layout(
        height=200,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#1e3050", size=8)),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,212,255,.05)", zeroline=False,
                   tickformat=".0%", tickfont=dict(color="#1e3050", size=8), range=[0, 1]),
        legend=dict(font=dict(size=8, color="#4a6080", family="Rajdhani"),
                    bgcolor="rgba(0,0,0,0)", orientation="h", x=.5, xanchor="center", y=1.1),
        hovermode="x unified",
        **CHART_LAYOUT,
    )
    return fig

def make_heatmap(history) -> go.Figure:
    if len(history) < 3:
        return None
    df = pd.DataFrame(history[-30:])
    hours = [datetime.strptime(r["time"], "%H:%M:%S").hour for r in history[-30:]]
    df["hour"] = hours
    df["idx"]  = range(len(df))
    z_pos = [df[df["hour"] == h]["positive"].mean() if len(df[df["hour"] == h]) else 0
             for h in range(24)]
    fig = go.Figure(go.Heatmap(
        z=[z_pos],
        x=list(range(24)),
        colorscale=[[0, "#03040a"], [0.5, "#00336a"], [1, "#00ff9f"]],
        showscale=False,
        hovertemplate="Hour %{x}:00 · Avg Positive: %{z:.1%}<extra></extra>",
    ))
    fig.update_layout(
        height=80, margin=dict(t=5, b=5, l=5, r=5),
        xaxis=dict(showgrid=False, tickfont=dict(color="#1e3050", size=7), tickmode="array",
                   tickvals=list(range(0,24,4)), ticktext=[f"{h:02d}h" for h in range(0,24,4)]),
        yaxis=dict(showgrid=False, showticklabels=False),
        **{k: v for k, v in CHART_LAYOUT.items() if k not in ("margin",)},
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for key, default in [
    ("history", []), ("total", 0),
    ("pos_n", 0), ("neg_n", 0), ("neu_n", 0),
    ("last_result", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class='sb-header'>
        <div class='sb-logo-row'>
            <div class='sb-logo-box'><span class='sb-logo-letter'>SF</span></div>
            <div>
                <div class='sb-name'>SENTIFLOW</div>
                <div class='sb-tagline'>Social Media Intelligence</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Model status
    if model_loaded:
        st.markdown("""
        <div class='sb-status'>
            <div class='sb-status-dot'></div>
            <span class='sb-status-txt'>MODEL ONLINE · INFERENCE READY</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.error("⚠ Model files not found in /models/")

    st.markdown("<div class='sb-section'>Model Configuration</div>", unsafe_allow_html=True)
    model_name = st.selectbox("Engine", ["Logistic Regression · TF-IDF", "SVM · TF-IDF", "Naive Bayes · TF-IDF"],
                              label_visibility="collapsed")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.50, 0.05)
    max_features   = st.slider("Max TF-IDF Features", 1000, 20000, 5000, 1000)

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-section'>Session Analytics</div>", unsafe_allow_html=True)

    total = st.session_state.total
    pos_pct = st.session_state.pos_n / total * 100 if total else 0
    neg_pct = st.session_state.neg_n / total * 100 if total else 0
    neu_pct = st.session_state.neu_n / total * 100 if total else 0
    avg_conf = np.mean([r["confidence"] for r in st.session_state.history]) if st.session_state.history else 0

    for lbl, val in [
        ("Total Analysed", str(total)),
        ("Avg. Confidence", f"{avg_conf:.1%}"),
        ("Positive Rate",  f"{pos_pct:.1f}%"),
        ("Negative Rate",  f"{neg_pct:.1f}%"),
        ("Neutral Rate",   f"{neu_pct:.1f}%"),
    ]:
        st.markdown(f"""
        <div class='sb-metric'>
            <span class='sb-m-lbl'>{lbl}</span>
            <span class='sb-m-val'>{val}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:var(--font-mono);font-size:.6rem;color:var(--text-dim);
                letter-spacing:.08em;line-height:1.8'>
        ENGINE · scikit-learn<br>
        VECTORISER · TF-IDF<br>
        CLASSES · 3 (pos/neg/neu)<br>
        VERSION · 2.0.0
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='hero'>
    <div class='hero-bg'></div>
    <div class='hero-grid'></div>
    <div class='hero-corner'></div>
    <div class='hero-corner-bl'></div>
    <div class='hero-badge'>
        <span class='status-dot'></span>
        SYSTEM · ONLINE &nbsp;/&nbsp; NLP INFERENCE ENGINE ACTIVE
    </div>
    <h1>SENTIFLOW <span class='c2'>AI</span><br><span style='font-size:.55em;letter-spacing:.08em;color:#2a4060'>SOCIAL MEDIA INTELLIGENCE PLATFORM</span></h1>
    <p class='hero-sub'>
        Enterprise-grade transformer sentiment analysis for brand monitoring,
        crisis detection, and audience intelligence — powered by your trained ML model.
    </p>
    <div class='hero-pills'>
        <div class='hero-pill'>
            <span class='val'>3</span>
            <span class='bar'></span>
            <span>Sentiment Classes</span>
        </div>
        <div class='hero-pill'>
            <span class='val'>&lt;50ms</span>
            <span class='bar'></span>
            <span>Inference Latency</span>
        </div>
        <div class='hero-pill'>
            <span class='val'>TF-IDF</span>
            <span class='bar'></span>
            <span>Vectoriser</span>
        </div>
        <div class='hero-pill'>
            <span class='val'>XAI</span>
            <span class='bar'></span>
            <span>Explainable AI</span>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  KPI ROW
# ══════════════════════════════════════════════════════════════════════════════
total = st.session_state.total
pos_n = st.session_state.pos_n
neg_n = st.session_state.neg_n
neu_n = st.session_state.neu_n

k1, k2, k3, k4 = st.columns(4)
kpi_data = [
    (k1, "acc",  "🧠", str(total),           "TWEETS ANALYSED",  f"↑ {total} this session" if total else "— awaiting data", "up"),
    (k2, "pos",  "✦",  str(pos_n),           "POSITIVE SIGNALS", f"{pos_n/total*100:.1f}% rate" if total else "— awaiting data", "up"),
    (k3, "neg",  "⚠",  str(neg_n),           "NEGATIVE SIGNALS", f"{neg_n/total*100:.1f}% rate" if total else "— awaiting data", "dn"),
    (k4, "neu",  "◈",  f"{avg_conf:.0%}" if st.session_state.history else "—%",
                                             "AVG CONFIDENCE",   f"{neu_n} neutral samples" if total else "— awaiting data", "nu"),
]
for col, cls, icon, val, lbl, delta, delta_cls in kpi_data:
    with col:
        accent_cfg = {
            "acc": ("rgba(0,212,255,.07)",  "linear-gradient(90deg,#00d4ff,transparent)", "0 0 14px rgba(0,212,255,.5)"),
            "pos": ("rgba(0,255,159,.06)",  "linear-gradient(90deg,#00ff9f,transparent)", "0 0 14px rgba(0,255,159,.5)"),
            "neg": ("rgba(255,0,110,.07)",  "linear-gradient(90deg,#ff006e,transparent)", "0 0 14px rgba(255,0,110,.5)"),
            "neu": ("rgba(255,179,0,.06)",  "linear-gradient(90deg,#ffb300,transparent)", "0 0 14px rgba(255,179,0,.5)"),
        }[cls]
        st.markdown(f"""
        <div class='kpi-card' style='--accent-color:{accent_cfg[0]};--accent-line:{accent_cfg[1]};--accent-shadow:{accent_cfg[2]}'>
            <div class='kpi-top'>
                <span class='kpi-icon'>{icon}</span>
                <span class='kpi-tag'>{cls.upper()}</span>
            </div>
            <div class='kpi-val'>{val}</div>
            <div class='kpi-lbl'>{lbl}</div>
            <div class='kpi-delta {delta_cls}'>{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1.1, 1], gap="large")

# ─────────────────────────────────────
#  LEFT — Input + Result + XAI
# ─────────────────────────────────────
with col_left:
    st.markdown("""
    <div class='sec-header'>
        <div class='ico'>⚡</div>
        <h3>Sentiment Inference Engine</h3>
        <div class='line'></div>
    </div>""", unsafe_allow_html=True)

    EXAMPLES = [
        "Absolutely love this product! Best purchase ever 🔥",
        "This service is broken and completely useless 😤",
        "Just arrived at the airport. Flight is on time.",
        "Incredible customer support — resolved in minutes!",
        "Worst experience I've had with any brand. Never again.",
    ]
    pills_html = "".join(f"<span class='e-pill'>{e[:36]}…</span>" for e in EXAMPLES)
    st.markdown(f"""
    <p style='font-family:var(--font-mono);font-size:.6rem;letter-spacing:.1em;
              color:var(--text-dim);text-transform:uppercase;margin-bottom:.4rem'>
        Quick Load Examples
    </p>
    <div class='pill-row'>{pills_html}</div>""", unsafe_allow_html=True)

    tweet_input = st.text_area(
        "Tweet",
        placeholder="Paste a tweet or social media post to analyse…",
        height=110,
        label_visibility="collapsed",
        key="tweet_input",
    )

    char_n = len(tweet_input) if tweet_input else 0
    char_color = "#ff006e" if char_n > 280 else "var(--text-dim)"
    st.markdown(f"""
    <p style='font-family:var(--font-mono);font-size:.6rem;text-align:right;
              color:{char_color};letter-spacing:.05em;margin-top:.25rem'>
        {char_n} / 280 CHARS
    </p>""", unsafe_allow_html=True)

    run_btn = st.button("▶  RUN SENTIMENT ANALYSIS", use_container_width=True)

    # ── Inference & Results ──────────────────────────────────────────────────
    if run_btn and tweet_input.strip():
        if not model_loaded:
            st.error("❌ Model files not found. Place `sentiment_model.pkl` and `tfidf_vectorizer.pkl` in a `/models/` directory.")
        else:
            with st.spinner(""):
                time.sleep(0.35)
                result = predict_sentiment(tweet_input)

            # Update state
            st.session_state.total += 1
            if result["label"] == "Positive":   st.session_state.pos_n += 1
            elif result["label"] == "Negative": st.session_state.neg_n += 1
            else:                               st.session_state.neu_n += 1
            st.session_state.history.append({
                **result,
                "text": tweet_input[:90],
                "time": datetime.now().strftime("%H:%M:%S"),
            })
            st.session_state.last_result = result

    elif run_btn:
        st.warning("⚠ Enter some text before running analysis.")

    # ── Show last result ─────────────────────────────────────────────────────
    if st.session_state.last_result:
        r   = st.session_state.last_result
        lbl = r["label"]
        cls = lbl.lower()
        cfg = {"Positive": ("😊", var_c := "#00ff9f"),
               "Negative": ("😠", var_c := "#ff006e"),
               "Neutral":  ("😐", var_c := "#ffb300")}
        emoji = cfg[lbl][0]; _color = cfg[lbl][1]
        conf  = r["confidence"]

        st.markdown(f"""
        <div class='pred-card {cls}'>
            <div class='pred-glow {cls}'></div>
            <div class='pred-top'>
                <div class='pred-emoji'>{emoji}</div>
                <div class='pred-info'>
                    <div class='pred-label {cls}'>{lbl.upper()}</div>
                    <div class='pred-meta'>
                        CONFIDENCE {conf:.1%} &nbsp;·&nbsp;
                        THRESHOLD {conf_threshold:.2f} &nbsp;·&nbsp;
                        ENGINE {model_name.split(" · ")[0].upper()}
                    </div>
                </div>
            </div>
            <div class='pred-conf-bar'>
                <div class='pred-conf-fill {cls}' style='width:{conf*100:.1f}%'></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Class Probability Gauges ─────────────────────────────────────────
        st.markdown("""
        <div class='sec-header' style='margin-top:1.2rem'>
            <div class='ico'>🎯</div><h3>Class Probabilities</h3><div class='line'></div>
        </div>""", unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1: st.plotly_chart(make_gauge(r["positive"], "#00ff9f", "Positive"), use_container_width=True, config={"displayModeBar": False})
        with g2: st.plotly_chart(make_gauge(r["negative"], "#ff006e", "Negative"), use_container_width=True, config={"displayModeBar": False})
        with g3: st.plotly_chart(make_gauge(r["neutral"],  "#ffb300", "Neutral"),  use_container_width=True, config={"displayModeBar": False})

        # ── Business Insight ─────────────────────────────────────────────────
        insight_body, insight_rec = get_business_insight(lbl, conf)
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-title'>🤖 AI Business Insight</div>
            <div class='insight-body'>{insight_body}</div>
            <div class='insight-rec'><span>{insight_rec}</span></div>
        </div>""", unsafe_allow_html=True)

        # ── Explainable AI — Keywords ─────────────────────────────────────────
        pos_kw, neg_kw = get_keywords(tweet_input, r)
        st.markdown("""
        <div class='xai-card'>
            <div class='xai-title'>🧬 Explainable AI · Token Influence Analysis</div>""",
        unsafe_allow_html=True)

        if pos_kw:
            kw_html = "".join(
                f"<span class='kw-chip pos'>{w} <span class='kw-score'>+{s:.3f}</span></span>"
                for w, s in pos_kw
            )
            st.markdown(f"""
            <p style='font-family:var(--font-mono);font-size:.6rem;letter-spacing:.1em;
                      color:var(--text-dim);margin-bottom:.4rem;text-transform:uppercase'>
                ↑ Positive Influence Tokens
            </p>
            <div class='kw-row'>{kw_html}</div>""", unsafe_allow_html=True)

        if neg_kw:
            kw_html = "".join(
                f"<span class='kw-chip neg'>{w} <span class='kw-score'>-{s:.3f}</span></span>"
                for w, s in neg_kw
            )
            st.markdown(f"""
            <p style='font-family:var(--font-mono);font-size:.6rem;letter-spacing:.1em;
                      color:var(--text-dim);margin:.6rem 0 .4rem;text-transform:uppercase'>
                ↓ Negative Influence Tokens
            </p>
            <div class='kw-row'>{kw_html}</div>""", unsafe_allow_html=True)

        if not pos_kw and not neg_kw:
            st.markdown("""
            <p style='font-family:var(--font-mono);font-size:.65rem;color:var(--text-dim)'>
                No strongly-polarised tokens detected in this input.
            </p>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────
#  RIGHT — Analytics Dashboard
# ─────────────────────────────────────
with col_right:
    st.markdown("""
    <div class='sec-header'>
        <div class='ico'>📊</div>
        <h3>Analytics Dashboard</h3>
        <div class='line'></div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.history:
        pos_avg = np.mean([r["positive"] for r in st.session_state.history])
        neg_avg = np.mean([r["negative"] for r in st.session_state.history])
        neu_avg = np.mean([r["neutral"]  for r in st.session_state.history])

        # Donut
        st.markdown("<div class='g-card'>", unsafe_allow_html=True)
        st.markdown("<div class='g-card-label'>Sentiment Distribution · Session Average</div>", unsafe_allow_html=True)
        st.plotly_chart(make_donut(pos_avg, neg_avg, neu_avg), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

        if len(st.session_state.history) > 1:
            # Confidence bar chart
            st.markdown("<div class='g-card'>", unsafe_allow_html=True)
            st.markdown("<div class='g-card-label'>Confidence Scores · Last 25 Analyses</div>", unsafe_allow_html=True)
            st.plotly_chart(make_confidence_trend(st.session_state.history), use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

            # Trend lines
            st.markdown("<div class='g-card'>", unsafe_allow_html=True)
            st.markdown("<div class='g-card-label'>Score Trends · All Classes</div>", unsafe_allow_html=True)
            st.plotly_chart(make_trend_lines(st.session_state.history), use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

            # Hourly heatmap
            hm = make_heatmap(st.session_state.history)
            if hm:
                st.markdown("<div class='g-card'>", unsafe_allow_html=True)
                st.markdown("<div class='g-card-label'>Positive Sentiment Heatmap · By Hour</div>", unsafe_allow_html=True)
                st.plotly_chart(hm, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

        # ── Executive Summary ─────────────────────────────────────────────────
        exec_html = get_exec_summary(st.session_state.history)
        avg_conf  = np.mean([r["confidence"] for r in st.session_state.history])
        risk_lbl  = "HIGH" if st.session_state.neg_n / max(total,1) > .40 else (
                    "MODERATE" if st.session_state.neg_n / max(total,1) > .20 else "LOW")
        risk_color = "#ff006e" if risk_lbl == "HIGH" else ("#ffb300" if risk_lbl == "MODERATE" else "#00ff9f")

        st.markdown(f"""
        <div class='exec-card' style='margin-top:.7rem'>
            <div class='exec-title'>📋 Executive Summary Panel</div>
            <div class='exec-line'>{exec_html}</div>
            <div class='exec-metric-row'>
                <div class='exec-metric'>
                    <div class='exec-m-val'>{total}</div>
                    <div class='exec-m-lbl'>Records</div>
                </div>
                <div class='exec-metric'>
                    <div class='exec-m-val'>{avg_conf:.0%}</div>
                    <div class='exec-m-lbl'>Avg Conf.</div>
                </div>
                <div class='exec-metric'>
                    <div class='exec-m-val' style='color:{risk_color}'>{risk_lbl}</div>
                    <div class='exec-m-lbl'>Brand Risk</div>
                </div>
                <div class='exec-metric'>
                    <div class='exec-m-val'>{st.session_state.pos_n}</div>
                    <div class='exec-m-lbl'>Positive</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class='g-card' style='text-align:center;padding:3.5rem 2rem'>
            <div style='font-size:2.5rem;margin-bottom:1rem;opacity:.3'>◈</div>
            <div class='g-card-title' style='letter-spacing:.1em'>NO DATA STREAM</div>
            <p style='color:var(--text-dim);font-family:var(--font-mono);font-size:.7rem;
                      margin-top:.6rem;letter-spacing:.08em'>
                ANALYSE A TWEET TO INITIALISE DASHBOARD
            </p>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SENTIMENT HISTORY
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-header'>
        <div class='ico'>🕒</div>
        <h3>Social Monitoring Feed · Analysis History</h3>
        <div class='line'></div>
    </div>""", unsafe_allow_html=True)

    for i, item in enumerate(reversed(st.session_state.history[-12:])):
        lbl  = item["label"]
        cls  = lbl.lower()
        conf = item.get("confidence", item.get(lbl.lower(), 0))
        text = item["text"]
        ts   = item.get("time", "—")
        idx  = st.session_state.total - i

        st.markdown(f"""
        <div class='hist-item'>
            <span class='hist-idx'>#{idx:03d}</span>
            <span class='hist-badge {cls}'>{lbl}</span>
            <span class='hist-text'>{text}</span>
            <span class='hist-score'>{conf:.1%}</span>
            <span class='hist-time'>{ts}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    if st.button("🗑  CLEAR ALL HISTORY", key="clear_all"):
        for k, v in [("history", []), ("total", 0), ("pos_n", 0),
                     ("neg_n", 0), ("neu_n", 0), ("last_result", None)]:
            st.session_state[k] = v
        st.rerun()

# ═══════════════════════════════════════════════════�