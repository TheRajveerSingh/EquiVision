"""
EquiVision — Premium CSS Theme System
All CSS variables, animations, glassmorphism, and premium styling.
"""

def get_theme_css():
    """Return the complete CSS theme string."""
    return """
    <style>
        /* ═══════════════════════ FONT IMPORTS ═══════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@300;400;500;700&display=swap');

        /* ═══════════════════════ CSS VARIABLES ═══════════════════════ */
        :root {
            --primary: #7F5AF0;
            --primary-glow: rgba(127, 90, 240, 0.4);
            --secondary: #2CB67D;
            --secondary-glow: rgba(44, 182, 125, 0.4);
            --accent: #FF8906;
            --accent-glow: rgba(255, 137, 6, 0.3);
            --danger: #E53170;
            --bg-dark: #0D0D11;
            --bg-surface: #16161A;
            --bg-card: rgba(255, 255, 255, 0.04);
            --bg-card-hover: rgba(255, 255, 255, 0.08);
            --text-primary: #FFFFFE;
            --text-secondary: #94A1B2;
            --text-muted: rgba(255, 255, 255, 0.4);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-border-hover: rgba(127, 90, 240, 0.3);
            --radius-sm: 10px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.4);
            --shadow-card-hover: 0 16px 48px rgba(127, 90, 240, 0.15);
            --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-smooth: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-bounce: 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        /* ═══════════════════════ GLOBAL RESET ═══════════════════════ */
        .stApp {
            background: var(--bg-dark) !important;
            background-image:
                radial-gradient(ellipse at 10% 10%, rgba(127, 90, 240, 0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 20%, rgba(44, 182, 125, 0.10) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 80%, rgba(255, 137, 6, 0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 90%, rgba(229, 49, 112, 0.05) 0%, transparent 40%) !important;
            background-attachment: fixed !important;
        }

        body, .stApp, [data-testid="stAppViewContainer"] {
            color: var(--text-primary) !important;
            font-family: 'Outfit', -apple-system, sans-serif !important;
        }

        /* Ensure Streamlit content sits ABOVE the starfield canvas */
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stSidebar"],
        section.main,
        header {
            position: relative;
            z-index: 2;
        }

        /* Noise texture overlay */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            opacity: 0.015;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 1;
        }

        /* ═══════════════════════ CUSTOM SCROLLBAR ═══════════════════════ */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary), var(--secondary));
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #9B7BFF, #3FD99B); }

        /* ═══════════════════════ TYPOGRAPHY ═══════════════════════ */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(135deg, #FFFFFE 0%, #94A1B2 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 0.8rem !important;
        }

        h1 {
            font-size: 2.5rem !important;
            background: linear-gradient(135deg, #FFFFFE 30%, #7F5AF0 70%, #2CB67D 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        p, span, label, div {
            font-family: 'Outfit', sans-serif;
        }

        /* ═══════════════════════ GLASSMORPHISM PANELS ═══════════════════════ */
        .glass-card,
        [data-testid="stMetric"],
        [data-testid="stExpander"],
        div.stDataFrame,
        div[data-testid="stForm"],
        div[data-testid="stSidebar"] {
            background: var(--bg-card) !important;
            backdrop-filter: blur(20px) saturate(1.3) !important;
            -webkit-backdrop-filter: blur(20px) saturate(1.3) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow-card) !important;
            transition: transform var(--transition-smooth),
                        box-shadow var(--transition-smooth),
                        border-color var(--transition-smooth) !important;
        }

        .glass-card:hover,
        [data-testid="stMetric"]:hover {
            background: var(--bg-card-hover) !important;
            box-shadow: var(--shadow-card-hover) !important;
            border-color: var(--glass-border-hover) !important;
        }

        /* ═══════════════════════ METRIC CARDS ═══════════════════════ */
        [data-testid="stMetric"] {
            padding: 1.5rem !important;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        /* Gradient animated border */
        [data-testid="stMetric"]::before {
            content: '';
            position: absolute;
            top: -1px; left: -1px; right: -1px; bottom: -1px;
            border-radius: var(--radius-lg);
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent), var(--primary));
            background-size: 300% 300%;
            animation: ev-gradient-spin 6s ease infinite;
            z-index: -1;
            opacity: 0;
            transition: opacity var(--transition-smooth);
        }

        [data-testid="stMetric"]:hover::before { opacity: 1; }

        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
            color: var(--text-secondary) !important;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 500;
        }

        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            text-shadow: 0 0 30px var(--primary-glow);
        }

        /* ═══════════════════════ BUTTONS ═══════════════════════ */
        div.stButton > button {
            background: linear-gradient(135deg, rgba(127, 90, 240, 0.85), rgba(44, 182, 125, 0.85)) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.7rem 1.5rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            letter-spacing: 0.02em !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25),
                        inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transition: all var(--transition-smooth) !important;
            position: relative;
            overflow: hidden;
            width: 100%;
        }

        /* Shimmer sweep on hover */
        div.stButton > button::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
            transition: 0.6s;
        }

        div.stButton > button:hover {
            box-shadow: 0 8px 30px var(--primary-glow),
                        0 0 60px rgba(127, 90, 240, 0.15),
                        inset 0 1px 0 rgba(255,255,255,0.3) !important;
            border-color: rgba(255,255,255,0.4) !important;
        }

        div.stButton > button:hover::before { left: 100%; }

        div.stButton > button:active {
            transform: scale(0.97) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        }

        /* Primary button variant */
        div.stButton > button[kind="primary"],
        div.stFormSubmitButton > button {
            background: linear-gradient(135deg, #7F5AF0, #6C4ED9) !important;
            box-shadow: 0 4px 25px rgba(127, 90, 240, 0.3),
                        inset 0 1px 0 rgba(255,255,255,0.25) !important;
        }

        /* ═══════════════════════ INPUT FIELDS ═══════════════════════ */
        .stTextInput > div > div > input,
        .stDateInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div,
        .stMultiSelect > div > div > div,
        .stTextArea > div > div > textarea {
            background: rgba(0,0,0,0.25) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.6rem 1rem !important;
            font-family: 'Outfit', sans-serif !important;
            transition: border-color var(--transition-fast),
                        box-shadow var(--transition-fast) !important;
        }

        .stTextInput > div > div > input:focus,
        .stDateInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(127, 90, 240, 0.15),
                        0 0 20px rgba(127, 90, 240, 0.08) !important;
        }

        /* ═══════════════════════ TABS ═══════════════════════ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: rgba(0,0,0,0.2);
            border-radius: var(--radius-md);
            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-sm) !important;
            color: var(--text-secondary) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            transition: all var(--transition-fast) !important;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(127, 90, 240, 0.2) !important;
            color: var(--text-primary) !important;
        }

        /* ═══════════════════════ CAMERA INPUT ═══════════════════════ */
        div[data-testid="stCameraInput"] {
            border: 2px solid var(--glass-border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }

        /* ═══════════════════════ EXPANDER ═══════════════════════ */
        [data-testid="stExpander"] {
            border-radius: var(--radius-md) !important;
        }

        [data-testid="stExpander"] summary {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }

        /* ═══════════════════════ DATAFRAME ═══════════════════════ */
        div.stDataFrame {
            border-radius: var(--radius-md) !important;
            overflow: hidden;
        }

        /* ═══════════════════════ RADIO / TOGGLE ═══════════════════════ */
        .stRadio > div {
            gap: 0.5rem;
        }

        .stRadio label {
            background: rgba(0,0,0,0.15) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.4rem 0.8rem !important;
            transition: all var(--transition-fast) !important;
        }

        .stRadio label:hover {
            border-color: var(--primary) !important;
            background: rgba(127, 90, 240, 0.1) !important;
        }

        /* ═══════════════════════ DIVIDER ═══════════════════════ */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--glass-border), transparent) !important;
            margin: 1.5rem 0 !important;
        }

        /* ═══════════════════════ ALERTS / INFO / SUCCESS ═══════════════════════ */
        .stAlert, [data-testid="stNotification"] {
            border-radius: var(--radius-md) !important;
            backdrop-filter: blur(10px) !important;
        }

        /* ═══════════════════════ LOGIN PAGE ═══════════════════════ */
        .ev-login-title {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: 3.8rem;
            text-align: center;
            margin-bottom: 0.3rem;
            letter-spacing: -0.05em;
            background: linear-gradient(135deg, #FFFFFE 0%, #7F5AF0 50%, #2CB67D 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: ev-title-glow 3s ease-in-out infinite alternate;
        }

        .ev-login-subtitle {
            font-family: 'Outfit', sans-serif;
            font-weight: 300;
            font-size: 1.05rem;
            color: var(--text-muted);
            text-align: center;
            font-style: italic;
            margin-bottom: 2.5rem;
            letter-spacing: 0.04em;
            min-height: 1.5em;
        }

        /* ═══════════════════════ NAVBAR ═══════════════════════ */
        .ev-navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(13, 13, 17, 0.7);
            backdrop-filter: blur(20px) saturate(1.2);
            -webkit-backdrop-filter: blur(20px) saturate(1.2);
            border-bottom: 1px solid var(--glass-border);
            padding: 0.6rem 1rem;
            margin: -1rem -1rem 1.5rem -1rem;
            border-radius: 0 0 var(--radius-md) var(--radius-md);
        }

        /* ═══════════════════════ ACTION CARDS (Home Page) ═══════════════════════ */
        .ev-action-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 2rem 1.5rem;
            text-align: center;
            transition: all var(--transition-smooth);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            min-height: 140px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .ev-action-card::before {
            content: '';
            position: absolute;
            top: -1px; left: -1px; right: -1px; bottom: -1px;
            border-radius: var(--radius-lg);
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent), var(--danger));
            background-size: 300% 300%;
            animation: ev-gradient-spin 8s ease infinite;
            z-index: -1;
            opacity: 0;
            transition: opacity var(--transition-smooth);
        }

        .ev-action-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-card-hover);
        }

        .ev-action-card:hover::before { opacity: 1; }

        .ev-action-card .ev-card-icon {
            font-size: 2.5rem;
            margin-bottom: 0.3rem;
            filter: drop-shadow(0 0 8px var(--primary-glow));
        }

        .ev-action-card .ev-card-label {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-primary);
        }

        /* ═══════════════════════ EVENT MENU CARDS ═══════════════════════ */
        .ev-menu-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-md);
            padding: 1.2rem;
            text-align: center;
            transition: all var(--transition-smooth);
            position: relative;
            overflow: hidden;
        }

        .ev-menu-card:hover {
            transform: translateY(-4px);
            border-color: var(--glass-border-hover);
            box-shadow: 0 12px 32px rgba(127, 90, 240, 0.12);
        }

        .ev-menu-card .ev-menu-icon {
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
        }

        .ev-menu-card .ev-menu-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* ═══════════════════════ SKELETON LOADING ═══════════════════════ */
        .ev-skeleton {
            position: relative;
            overflow: hidden;
            background: rgba(255,255,255,0.04);
            border-radius: var(--radius-sm);
        }

        .ev-skeleton::after {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            animation: ev-skeleton-sweep 1.5s infinite;
        }

        .ev-skeleton-line {
            height: 14px;
            margin: 10px 0;
            border-radius: 4px;
        }

        .ev-skeleton-block {
            height: 80px;
            border-radius: var(--radius-sm);
        }

        /* ═══════════════════════ ANIMATIONS / KEYFRAMES ═══════════════════════ */
        @keyframes ev-gradient-spin {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes ev-title-glow {
            0% { filter: drop-shadow(0 0 15px rgba(127, 90, 240, 0.3)); }
            100% { filter: drop-shadow(0 0 30px rgba(44, 182, 125, 0.4)); }
        }

        @keyframes ev-skeleton-sweep {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        @keyframes ev-ripple {
            0% { transform: scale(0); opacity: 0.35; }
            100% { transform: scale(3); opacity: 0; }
        }

        @keyframes ev-welcome-scale {
            0% { opacity: 0; transform: scale(0.5); }
            100% { opacity: 1; transform: scale(1); }
        }

        @keyframes ev-welcome-fade {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes ev-fade-in {
            0% { opacity: 0; transform: translateY(15px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes ev-slide-up {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Page entrance animation */
        section.main > div {
            animation: ev-fade-in 0.5s ease-out;
        }

        /* Smooth icon hover animations */
        .ev-action-card:hover .ev-card-icon,
        .ev-menu-card:hover .ev-menu-icon {
            animation: ev-icon-bounce 0.4s ease;
        }

        @keyframes ev-icon-bounce {
            0% { transform: scale(1); }
            40% { transform: scale(1.25); }
            70% { transform: scale(0.95); }
            100% { transform: scale(1); }
        }

        /* ═══════════════════════ RESPONSIVE ═══════════════════════ */
        @media (max-width: 768px) {
            .ev-login-title { font-size: 2.5rem; }
            .ev-action-card { padding: 1.2rem 1rem; min-height: 100px; }
            .ev-action-card .ev-card-icon { font-size: 2rem; }
        }
    </style>
    """
