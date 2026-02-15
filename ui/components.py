"""
EquiVision — Reusable Streamlit UI Components
Glass cards, navbar, hero titles, confetti, skeletons, and more.
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import json

from .theme import get_theme_css


def _load_animations_js():
    """Read the animations.js file and return as string."""
    js_path = os.path.join(os.path.dirname(__file__), "animations.js")
    with open(js_path, "r", encoding="utf-8") as f:
        return f.read()


def _run_parent_js(js_code: str, height: int = 0):
    """Execute JavaScript in the parent Streamlit document via a hidden iframe.
    
    st.markdown strips <script> tags, so we use components.html() which runs
    in an iframe. From there we inject a <script> into the parent document so
    the code runs with full access to the main page DOM.
    """
    # json.dumps safely escapes all quotes, backticks, newlines etc.
    escaped = json.dumps(js_code)
    components.html(
        f"""<script>
        (function() {{
            var pd = window.parent.document;
            var s = pd.createElement('script');
            s.textContent = {escaped};
            pd.head.appendChild(s);
            // Clean up: remove after execution so it doesn't pile up
            setTimeout(function() {{ s.remove(); }}, 100);
        }})();
        </script>""",
        height=height,
    )


def inject_theme():
    """Inject the full CSS theme + JS animations into the page. Call once at the top."""
    # Inject CSS (st.markdown handles <style> tags fine)
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Inject JS via hidden iframe → parent document script injection
    js_code = _load_animations_js()
    full_js = "window.__equivisionInitialized = false;\n" + js_code
    _run_parent_js(full_js)


def hero_title(title: str, subtitle: str = ""):
    """Render a premium hero title with optional typewriter subtitle."""
    st.markdown(
        f'<div class="ev-login-title">{title}</div>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<div class="ev-login-subtitle ev-typewriter" data-text="{subtitle}">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def glass_card(icon: str, label: str, key_suffix: str = ""):
    """
    Render a premium glassmorphism action card.
    Returns the HTML; pair with st.button separately for click handling.
    """
    st.markdown(
        f"""<div class="ev-action-card">
            <div class="ev-card-icon">{icon}</div>
            <div class="ev-card-label">{label}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def menu_card(icon: str, label: str):
    """Render a smaller event-menu card."""
    st.markdown(
        f"""<div class="ev-menu-card">
            <div class="ev-menu-icon">{icon}</div>
            <div class="ev-menu-label">{label}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def glass_navbar():
    """Render a sticky glassmorphism navigation bar with Home and Back buttons."""
    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
        st.markdown(
            '<span style="font-family:Inter,sans-serif; font-weight:700; '
            'font-size:1rem; background:linear-gradient(90deg,#7F5AF0,#2CB67D); '
            '-webkit-background-clip:text; -webkit-text-fill-color:transparent;">'
            '⚡ EquiVision</span>',
            unsafe_allow_html=True,
        )
    with col2:
        home_clicked = st.button("🏠", use_container_width=True, help="Home")
    with col3:
        back_clicked = st.button("⬅️", use_container_width=True, help="Back")

    return home_clicked, back_clicked


def welcome_animation(username: str):
    """Trigger the full-screen welcome animation."""
    safe_name = username.replace("'", "\\'").replace('"', '\\"')
    _run_parent_js(f'if(window.evWelcome) window.evWelcome("{safe_name}");')


def success_confetti():
    """Trigger a confetti burst animation."""
    _run_parent_js('if(window.evConfetti) window.evConfetti();')


def loading_skeleton(rows: int = 3):
    """Render a skeleton loading placeholder."""
    lines = ""
    for i in range(rows):
        width = 90 - (i * 15) if i < 4 else 60
        lines += f'<div class="ev-skeleton ev-skeleton-line" style="width:{width}%"></div>'
    st.markdown(
        f'<div style="padding:1rem;">{lines}</div>',
        unsafe_allow_html=True,
    )


def greeting_banner(username: str, now):
    """Render the home-page greeting with time and date."""
    hour = now.hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    emoji = "🌅" if hour < 12 else "☀️" if hour < 18 else "🌙"

    st.markdown(
        f"""<div style="animation: ev-slide-up 0.6s ease-out;">
            <h1 style="margin-bottom:0.2rem !important;">{emoji} {greeting}, {username}!</h1>
            <p style="color: var(--text-secondary); font-size: 1rem; margin-top:0;">
                🕒 <strong>{now.strftime('%I:%M %p')}</strong> &nbsp;|&nbsp; 📅 {now.strftime('%d %B %Y')}
            </p>
        </div>""",
        unsafe_allow_html=True,
    )


def section_heading(text: str, subtitle: str = ""):
    """Render an animated section heading."""
    html = f'<div style="animation: ev-fade-in 0.5s ease-out;">'
    html += f'<h2 style="margin-bottom:0.3rem !important;">{text}</h2>'
    if subtitle:
        html += f'<p style="color:var(--text-secondary); font-size:0.9rem; margin-top:0;">{subtitle}</p>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def event_list_card(name: str, date: str, count: int):
    """Render a styled event list item card."""
    st.markdown(
        f"""<div class="glass-card" style="padding:1.2rem 1.5rem; margin-bottom:0.8rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0 !important; font-size:1.2rem !important;">{name}</h3>
                    <span style="color:var(--text-secondary); font-size:0.85rem;">
                        📅 {date} &nbsp;·&nbsp; 👥 {count} Participants
                    </span>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )
