import os
import streamlit as st


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="PharmaQuest",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# INITIAL STUDENT STATE
# ============================================================

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "badges" not in st.session_state:
    st.session_state.badges = 0

if "missions_completed" not in st.session_state:
    st.session_state.missions_completed = 0

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "🏠 Home"


# ============================================================
# GEMINI CONNECTION
# ============================================================

def get_gemini_client():

    try:

        api_key = st.secrets.get("GEMINI_API_KEY")

        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            return None

        from google import genai

        return genai.Client(api_key=api_key)

    except Exception:

        return None


# ============================================================
# XP / LEVEL SYSTEM
# ============================================================

def get_level_info(xp):

    levels = [
        (1, "Pharma Initiate", 0, 100),
        (2, "Drug Seeker", 100, 250),
        (3, "Pharma Strategist", 250, 500),
        (4, "Clinical Specialist", 500, 850),
        (5, "Therapeutics Master", 850, 1300),
        (6, "PharmaQuest Elite", 1300, 2000),
    ]

    current = levels[0]

    for level in levels:

        if xp >= level[2]:
            current = level

    return current


level_number, level_name, level_start, level_end = get_level_info(
    st.session_state.xp
)

if level_end > level_start:

    progress_percent = int(
        (
            (st.session_state.xp - level_start)
            / (level_end - level_start)
        ) * 100
    )

else:

    progress_percent = 0

progress_percent = max(
    0,
    min(100, progress_percent)
)

xp_to_next = max(
    0,
    level_end - st.session_state.xp
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(124,58,237,0.16),
                transparent 25%
            ),
            radial-gradient(
                circle at 92% 12%,
                rgba(6,182,212,0.12),
                transparent 24%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(236,72,153,0.10),
                transparent 28%
            ),
            #0b1020;

        color: #f8fafc;
    }

    .block-container {

        max-width: 1500px;

        padding-top: 1.5rem;

        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #11152a 0%,
                #15102a 50%,
                #0d1c27 100%
            );

        border-right:
            1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-brand {

        padding:
            8px 5px 18px 5px;
    }

    .brand-row {

        display: flex;

        align-items: center;

        gap: 13px;
    }

    .sidebar-logo {

        width: 54px;
        height: 54px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 17px;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #ec4899,
                #f97316
            );

        box-shadow:
            0 12px 30px
            rgba(236,72,153,0.30);

        font-size: 27px;
    }

    .sidebar-title {

        color: #ffffff;

        font-size: 20px;

        font-weight: 950;

        letter-spacing: -0.5px;
    }

    .sidebar-subtitle {

        margin-top: 3px;

        color: #94a3b8;

        font-size: 8px;

        font-weight: 900;

        letter-spacing: 1.3px;
    }

    .sidebar-section {

        margin-top: 17px;

        margin-bottom: 7px;

        color: #fbbf24;

        font-size: 9px;

        font-weight: 950;

        letter-spacing: 1.5px;
    }

    .sidebar-section.play {
        color: #c084fc;
    }

    .sidebar-section.learn {
        color: #34d399;
    }

    .sidebar-section.account {
        color: #f472b6;
    }

    section[data-testid="stSidebar"] .stRadio label {

        color: #cbd5e1 !important;

        font-size: 11px !important;

        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {

        color: white !important;
    }

    .sidebar-footer-card {

        margin-top: 18px;

        padding: 17px;

        border-radius: 20px;

        background:
            linear-gradient(
                135deg,
                rgba(124,58,237,0.20),
                rgba(236,72,153,0.12)
            );

        border:
            1px solid
            rgba(255,255,255,0.10);

        box-shadow:
            0 15px 35px
            rgba(0,0,0,0.20);
    }

    .footer-label {

        color: #94a3b8;

        font-size: 8px;

        font-weight: 900;

        letter-spacing: 1px;
    }

    .footer-rank {

        margin-top: 5px;

        color: #c084fc;

        font-size: 15px;

        font-weight: 950;
    }


    /* ========================================================
       TOP BAR
       ======================================================== */

    .topbar {

        margin-bottom: 20px;
    }

    .eyebrow {

        color: #a78bfa;

        font-size: 9px;

        font-weight: 950;

        letter-spacing: 1.8px;
    }

    .top-title {

        margin-top: 5px;

        color: #ffffff;

        font-size: 31px;

        font-weight: 950;

        letter-spacing: -1.2px;
    }

    .top-subtitle {

        margin-top: 4px;

        color: #94a3b8;

        font-size: 12px;
    }


    /* ========================================================
       WELCOME HERO
       ======================================================== */

    .welcome-card {

        position: relative;

        overflow: hidden;

        padding: 36px;

        border-radius: 30px;

        background:
            radial-gradient(
                circle at 88% 15%,
                rgba(251,191,36,0.35),
                transparent 20%
            ),
            radial-gradient(
                circle at 15% 100%,
                rgba(6,182,212,0.30),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #312e81,
                #7c3aed 45%,
                #db2777 78%,
                #f97316
            );

        border:
            1px solid
            rgba(255,255,255,0.14);

        box-shadow:
            0 30px 70px
            rgba(124,58,237,0.30);
    }

    .welcome-card::after {

        content: "";

        position: absolute;

        width: 220px;
        height: 220px;

        right: -70px;
        bottom: -90px;

        border-radius: 50%;

        background:
            rgba(255,255,255,0.08);
    }

    .welcome-label {

        display: inline-block;

        padding: 7px 12px;

        border-radius: 999px;

        background:
            rgba(255,255,255,0.14);

        border:
            1px solid
            rgba(255,255,255,0.20);

        color: #fde68a;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1.5px;
    }

    .welcome-title {

        margin-top: 15px;

        color: white;

        font-size: 38px;

        line-height: 1.1;

        font-weight: 950;

        letter-spacing: -1.5px;
    }

    .welcome-text {

        max-width: 700px;

        margin-top: 10px;

        color: #f5f3ff;

        font-size: 13px;

        line-height: 1.65;
    }

    .welcome-pill {

        display: inline-block;

        margin-top: 20px;

        padding: 10px 15px;

        border-radius: 13px;

        background:
            rgba(0,0,0,0.16);

        border:
            1px solid
            rgba(255,255,255,0.13);

        color: white;

        font-size: 10px;

        font-weight: 850;
    }


    /* ========================================================
       STAT CARDS
       ======================================================== */

    .stats-area {

        margin-top: 20px;
    }

    .mini-card {

        min-height: 125px;

        padding: 20px;

        border-radius: 21px;

        background:
            linear-gradient(
                145deg,
                #151b32,
                #101628
            );

        border:
            1px solid
            rgba(255,255,255,0.08);

        box-shadow:
            0 15px 35px
            rgba(0,0,0,0.18);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }

    .mini-card:hover {

        transform: translateY(-5px);

        box-shadow:
            0 22px 45px
            rgba(0,0,0,0.28);
    }

    .mini-icon {

        font-size: 25px;
    }

    .mini-number {

        margin-top: 5px;

        color: #ffffff;

        font-size: 26px;

        font-weight: 950;
    }

    .mini-label {

        color: #cbd5e1;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1px;
    }

    .mini-description {

        margin-top: 4px;

        color: #64748b;

        font-size: 9px;
    }


    /* ========================================================
       LEVEL CARD
       ======================================================== */

    .level-card {

        margin-top: 20px;

        padding: 23px;

        border-radius: 23px;

        background:
            linear-gradient(
                145deg,
                #161d36,
                #11172a
            );

        border:
            1px solid
            rgba(255,255,255,0.08);

        box-shadow:
            0 15px 35px
            rgba(0,0,0,0.18);
    }

    .level-top {

        display: flex;

        justify-content: space-between;

        align-items: center;
    }

    .level-badge {

        display: flex;

        align-items: center;
        justify-content: center;

        width: 57px;
        height: 57px;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                #f59e0b,
                #ef4444
            );

        color: white;

        font-size: 16px;

        font-weight: 950;

        box-shadow:
            0 12px 25px
            rgba(249,115,22,0.25);
    }

    .level-title {

        flex: 1;

        margin-left: 15px;
    }

    .level-small {

        color: #64748b;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1px;
    }

    .level-name {

        margin-top: 3px;

        color: #ffffff;

        font-size: 18px;

        font-weight: 950;
    }

    .level-xp {

        color: #c084fc;

        font-size: 11px;

        font-weight: 950;
    }

    .level-track {

        margin-top: 17px;

        width: 100%;

        height: 10px;

        overflow: hidden;

        border-radius: 999px;

        background: #1e293b;
    }

    .level-fill {

        height: 100%;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #ec4899,
                #f59e0b
            );

        box-shadow:
            0 0 14px
            rgba(236,72,153,0.45);
    }

    .level-bottom {

        display: flex;

        justify-content: space-between;

        margin-top: 7px;

        color: #64748b;

        font-size: 9px;
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    .section-heading {

        margin-top: 35px;

        margin-bottom: 5px;

        color: #ffffff;

        font-size: 25px;

        font-weight: 950;

        letter-spacing: -0.6px;
    }

    .section-caption {

        margin-bottom: 17px;

        color: #94a3b8;

        font-size: 11px;
    }


    /* ========================================================
       MISSION CARDS
       ======================================================== */

    .mission-card {

        position: relative;

        min-height: 215px;

        padding: 22px;

        margin-bottom: 4px;

        border-radius: 24px;

        overflow: hidden;

        color: white;

        border:
            1px solid
            rgba(255,255,255,0.12);

        box-shadow:
            0 18px 38px
            rgba(0,0,0,0.22);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }

    .mission-card::after {

        content: "";

        position: absolute;

        width: 130px;
        height: 130px;

        right: -45px;
        bottom: -55px;

        border-radius: 50%;

        background:
            rgba(255,255,255,0.10);
    }

    .mission-card:hover {

        transform: translateY(-7px) scale(1.01);

        box-shadow:
            0 25px 55px
            rgba(0,0,0,0.35);
    }

    .mission-purple {

        background:
            linear-gradient(
                145deg,
                #6d28d9,
                #9333ea,
                #c026d3
            );
    }

    .mission-blue {

        background:
            linear-gradient(
                145deg,
                #1d4ed8,
                #2563eb,
                #0891b2
            );
    }

    .mission-pink {

        background:
            linear-gradient(
                145deg,
                #be185d,
                #db2777,
                #9333ea
            );
    }

    .mission-orange {

        background:
            linear-gradient(
                145deg,
                #c2410c,
                #ea580c,
                #dc2626
            );
    }

    .mission-indigo {

        background:
            linear-gradient(
                145deg,
                #3730a3,
                #4f46e5,
                #2563eb
            );
    }

    .mission-green {

        background:
            linear-gradient(
                145deg,
                #047857,
                #059669,
                #0d9488
            );
    }

    .mission-yellow {

        background:
            linear-gradient(
                145deg,
                #b45309,
                #d97706,
                #ea580c
            );
    }

    .mission-red {

        background:
            linear-gradient(
                145deg,
                #b91c1c,
                #dc2626,
                #db2777
            );
    }

    .mission-top {

        display: flex;

        justify-content: space-between;

        align-items: center;

        position: relative;

        z-index: 2;
    }

    .mission-icon {

        width: 58px;
        height: 58px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 18px;

        background:
            rgba(255,255,255,0.16);

        border:
            1px solid
            rgba(255,255,255,0.20);

        font-size: 29px;

        box-shadow:
            0 10px 20px
            rgba(0,0,0,0.12);
    }

    .mission-tag {

        padding: 6px 9px;

        border-radius: 999px;

        background:
            rgba(0,0,0,0.18);

        color: #ffffff;

        font-size: 7px;

        font-weight: 950;

        letter-spacing: 1px;
    }

    .mission-name {

        position: relative;

        z-index: 2;

        margin-top: 17px;

        color: white;

        font-size: 18px;

        font-weight: 950;
    }

    .mission-description {

        position: relative;

        z-index: 2;

        min-height: 49px;

        margin-top: 7px;

        color: rgba(255,255,255,0.83);

        font-size: 10px;

        line-height: 1.55;
    }

    .mission-reward {

        position: relative;

        z-index: 2;

        margin-top: 11px;

        color: #ffffff;

        font-size: 9px;

        font-weight: 950;
    }


    /* ========================================================
       CLICKABLE GAME BUTTON
       ======================================================== */

    .game-button {

        margin-top: 13px;
    }

    .game-button button {

        width: 100% !important;

        min-height: 42px !important;

        border-radius: 12px !important;

        border:
            1px solid
            rgba(255,255,255,0.20) !important;

        background:
            rgba(255,255,255,0.13) !important;

        color: white !important;

        font-size: 10px !important;

        font-weight: 900 !important;

        transition: 0.2s ease !important;
    }

    .game-button button:hover {

        background:
            rgba(255,255,255,0.24) !important;

        border-color:
            rgba(255,255,255,0.40) !important;

        transform:
            translateY(-2px) !important;

        box-shadow:
            0 8px 20px
            rgba(0,0,0,0.18) !important;
    }


    /* ========================================================
       OTHER PAGES
       ======================================================== */

    .page-card {

        padding: 30px;

        border-radius: 25px;

        background:
            linear-gradient(
                145deg,
                #151b32,
                #101628
            );

        border:
            1px solid
            rgba(255,255,255,0.08);

        box-shadow:
            0 18px 40px
            rgba(0,0,0,0.20);
    }

    .page-card h2 {

        color: #ffffff;
    }

    .page-card p {

        color: #94a3b8;
    }

    .page-badge {

        display: inline-block;

        padding: 7px 11px;

        border-radius: 999px;

        background:
            rgba(124,58,237,0.18);

        border:
            1px solid
            rgba(167,139,250,0.20);

        color: #c4b5fd;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1px;
    }


    /* ========================================================
       STREAMLIT INPUTS
       ======================================================== */

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] {

        background: #151b32 !important;
    }

    input,
    textarea {

        color: #ffffff !important;
    }

    label {

        color: #cbd5e1 !important;
    }

    .stSelectbox div,
    .stTextInput div {

        border-radius: 12px;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        min-height: 44px;

        border-radius: 13px;

        border:
            1px solid
            rgba(124,58,237,0.35);

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #db2777
            );

        color: white;

        font-weight: 900;

        transition: 0.2s ease;
    }

    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 10px 25px
            rgba(124,58,237,0.30);
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                #151b32,
                #101628
            );

        border:
            1px solid
            rgba(255,255,255,0.08);

        border-radius: 18px;

        padding: 18px;
    }

    [data-testid="stMetricLabel"] {

        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {

        color: #ffffff !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    .stAlert {

        border-radius: 15px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .welcome-title {
            font-size: 30px;
        }

        .welcome-card {
            padding: 27px;
        }

        .top-title {
            font-size: 25px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">

            <div class="brand-row">

                <div class="sidebar-logo">
                    💊
                </div>

                <div>

                    <div class="sidebar-title">
                        PHARMAQUEST
                    </div>

                    <div class="sidebar-subtitle">
                        PHARMACY LEARNING LAB
                    </div>

                </div>

            </div>

        </div>
        """
    )

    st.markdown("---")

    st.html(
        """
        <div class="sidebar-section">
            MAIN
        </div>
        """
    )

    main_page = st.radio(
        "MAIN",
        [
            "🏠 Home",
            "📊 My Progress"
        ],
        label_visibility="collapsed",
        key="main_navigation"
    )

    st.html(
        """
        <div class="sidebar-section play">
            🎮 PLAY & PRACTICE
        </div>
        """
    )

    play_page = st.radio(
        "PLAY",
        [
            "🕵️ Drug Detective",
            "🩺 Patient Case",
            "🗣️ AI Patient",
            "⚔️ Pharma Battle",
            "🔐 Escape Room",
            "🧬 Build the Patient"
        ],
        label_visibility="collapsed",
        key="play_navigation"
    )

    st.html(
        """
        <div class="sidebar-section learn">
            🧠 LEARN
        </div>
        """
    )

    learn_page = st.radio(
        "LEARN",
        [
            "❓ AI Quiz",
            "🔥 Daily Challenge"
        ],
        label_visibility="collapsed",
        key="learn_navigation"
    )

    st.html(
        """
        <div class="sidebar-section account">
            👤 ACCOUNT
        </div>
        """
    )

    account_page = st.radio(
        "ACCOUNT",
        [
            "🏆 My Profile"
        ],
        label_visibility="collapsed",
        key="account_navigation"
    )


# ============================================================
# DETERMINE PAGE
# ============================================================

if st.session_state.selected_page != "🏠 Home":

    page = st.session_state.selected_page

else:

    if main_page != "🏠 Home":
        page = main_page

    elif play_page in [
        "🕵️ Drug Detective",
        "🩺 Patient Case",
        "🗣️ AI Patient",
        "⚔️ Pharma Battle",
        "🔐 Escape Room",
        "🧬 Build the Patient"
    ]:

        page = play_page

    elif learn_page in [
        "❓ AI Quiz",
        "🔥 Daily Challenge"
    ]:

        page = learn_page

    else:

        page = account_page


# ============================================================
# SIDEBAR STATUS
# ============================================================

with st.sidebar:

    st.html(
        f"""
        <div class="sidebar-footer-card">

            <div class="footer-label">
                CURRENT JOURNEY
            </div>

            <div class="footer-rank">
                🧬 {level_name}
            </div>

            <div style="
                margin-top:10px;
                font-size:10px;
                color:#cbd5e1;
                font-weight:700;
            ">
                ⭐ {st.session_state.xp} XP
            </div>

            <div style="
                margin-top:8px;
                height:6px;
                border-radius:10px;
                background:#1e293b;
                overflow:hidden;
            ">

                <div style="
                    width:{progress_percent}%;
                    height:100%;
                    border-radius:10px;
                    background:
                        linear-gradient(
                            90deg,
                            #7c3aed,
                            #ec4899,
                            #f59e0b
                        );
                "></div>

            </div>

        </div>
        """
    )


# ============================================================
# HOME DASHBOARD
# ============================================================

if page == "🏠 Home":

    st.html(
        f"""
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    PHARMAQUEST • STUDENT COMMAND
                </div>

                <div class="top-title">
                    Your Pharmacy Journey
                </div>

                <div class="top-subtitle">
                    Learn. Practice. Challenge yourself.
                </div>

            </div>

        </div>


        <div class="welcome-card">

            <div class="welcome-label">
                🧬 LEVEL {level_number} • {level_name.upper()}
            </div>

            <div class="welcome-title">
                Ready for your next
                pharmacy challenge?
            </div>

            <div class="welcome-text">
                Build clinical thinking, medication knowledge
                and counselling skills through interactive
                pharmacy missions powered by AI.
            </div>

            <div class="welcome-pill">
                ⭐ {st.session_state.xp} XP
                &nbsp;&nbsp;•&nbsp;&nbsp;
                🔥 {st.session_state.streak} day streak
            </div>

        </div>
        """
    )


    # ========================================================
    # QUICK STATS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    stats = [

        (
            "⭐",
            str(st.session_state.xp),
            "TOTAL XP",
            "Start earning experience"
        ),

        (
            "🔥",
            str(st.session_state.streak),
            "DAY STREAK",
            "Your learning streak"
        ),

        (
            "🏆",
            str(st.session_state.badges),
            "BADGES",
            "Achievements unlocked"
        ),

        (
            "🧠",
            str(st.session_state.missions_completed),
            "MISSIONS",
            "Completed missions"
        )

    ]

    for col, data in zip(
        [c1, c2, c3, c4],
        stats
    ):

        icon, number, name, description = data

        with col:

            st.html(
                f"""
                <div class="mini-card">

                    <div class="mini-icon">
                        {icon}
                    </div>

                    <div class="mini-number">
                        {number}
                    </div>

                    <div class="mini-label">
                        {name}
                    </div>

                    <div class="mini-description">
                        {description}
                    </div>

                </div>
                """
            )


    # ========================================================
    # LEVEL
    # ========================================================

    st.html(
        f"""
        <div class="level-card">

            <div class="level-top">

                <div class="level-badge">
                    LV {level_number}
                </div>

                <div class="level-title">

                    <div class="level-small">
                        CURRENT PHARMA RANK
                    </div>

                    <div class="level-name">
                        🧬 {level_name}
                    </div>

                </div>

                <div class="level-xp">
                    {st.session_state.xp} / {level_end} XP
                </div>

            </div>

            <div class="level-track">

                <div
                    class="level-fill"
                    style="width:{progress_percent}%;"
                ></div>

            </div>

            <div class="level-bottom">

                <span>
                    🚀 {xp_to_next} XP until next level
                </span>

                <span>
                    {progress_percent}%
                </span>

            </div>

        </div>
        """
    )


    # ========================================================
    # MISSION HUB
    # ========================================================

    st.html(
        """
        <div class="section-heading">
            🎮 Mission Hub
        </div>

        <div class="section-caption">
            Choose your next challenge. Every mission trains a different pharmacy skill.
        </div>
        """
    )


    missions = [

        (
            "🕵️",
            "Drug Detective",
            "Investigate clues and identify the mystery medicine.",
            "DEDUCTION",
            "+50 XP",
            "mission-purple"
        ),

        (
            "🩺",
            "Patient Case",
            "Think like a clinical pharmacist and solve a fictional case.",
            "CLINICAL",
            "+75 XP",
            "mission-blue"
        ),

        (
            "🗣️",
            "AI Patient",
            "Practice counselling with realistic patient personalities.",
            "COUNSELLING",
            "+60 XP",
            "mission-pink"
        ),

        (
            "⚔️",
            "Pharma Battle",
            "Answer rapid-fire pharmacy questions.",
            "BATTLE",
            "+50 XP",
            "mission-orange"
        ),

        (
            "🔐",
            "Escape Room",
            "Solve a pharmacy mystery before time runs out.",
            "MYSTERY",
            "+100 XP",
            "mission-indigo"
        ),

        (
            "🧬",
            "Build the Patient",
            "Explore treatment decisions in a fictional patient.",
            "SIMULATION",
            "+100 XP",
            "mission-green"
        ),

        (
            "❓",
            "AI Quiz",
            "Create a personalized pharmacy quiz with AI.",
            "KNOWLEDGE",
            "+50 XP",
            "mission-yellow"
        ),

        (
            "🔥",
            "Daily Challenge",
            "Complete today's challenge and earn bonus XP.",
            "DAILY",
            "+75 XP",
            "mission-red"
        )

    ]


    columns = st.columns(4)


    for i, mission in enumerate(missions):

        icon, title, description, category, reward, card_class = mission

        with columns[i % 4]:

            st.html(
                f"""
                <div class="mission-card {card_class}">

                    <div class="mission-top">

                        <div class="mission-icon">
                            {icon}
                        </div>

                        <div class="mission-tag">
                            {category}
                        </div>

                    </div>

                    <div class="mission-name">
                        {title}
                    </div>

                    <div class="mission-description">
                        {description}
                    </div>

                    <div class="mission-reward">
                        ⚡ {reward}
                    </div>

                </div>
                """
            )

            # ------------------------------------------------
            # CLICKABLE BUTTON
            # ------------------------------------------------

            if st.button(
                f"▶ OPEN {title.upper()}",
                key=f"mission_{i}",
                use_container_width=True
            ):

                st.session_state.selected_page = (
                    f"{icon} {title}"
                )

                st.rerun()


# ============================================================
# MY PROGRESS
# ============================================================

elif page == "📊 My Progress":

    st.html(
        """
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    PROGRESSION CENTER
                </div>

                <div class="top-title">
                    My Progress
                </div>

                <div class="top-subtitle">
                    Track your pharmacy learning journey.
                </div>

            </div>

        </div>
        """
    )

    st.html(
        f"""
        <div class="page-card">

            <div class="page-badge">
                LEVEL {level_number}
            </div>

            <h2>
                🧬 {level_name}
            </h2>

            <p>
                You currently have
                <strong>{st.session_state.xp} XP</strong>.
            </p>

            <div class="level-track">

                <div
                    class="level-fill"
                    style="width:{progress_percent}%;"
                ></div>

            </div>

            <p style="
                color:#64748b;
                font-size:11px;
                margin-top:8px;
            ">
                {xp_to_next} XP remaining until your next level.
            </p>

        </div>
        """
    )

    st.write("")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "⭐ Total XP",
            st.session_state.xp
        )

    with p2:
        st.metric(
            "🏆 Badges",
            st.session_state.badges
        )

    with p3:
        st.metric(
            "🧠 Missions",
            st.session_state.missions_completed
        )


# ============================================================
# DRUG DETECTIVE
# ============================================================

elif page == "🕵️ Drug Detective":

    st.html(
        """
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    🎮 PLAY & PRACTICE
                </div>

                <div class="top-title">
                    🕵️ Drug Detective
                </div>

                <div class="top-subtitle">
                    Investigate clues. Think clinically. Identify the medicine.
                </div>

            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="page-card">

            <div class="page-badge">
                +50 XP • DEDUCTION
            </div>

            <h2>
                🔎 Open a new case
            </h2>

            <p>
                Choose a pharmacy topic and let AI create
                a mystery case for you.
            </p>

        </div>
        """
    )

    topic = st.text_input(
        "Pharmacy topic",
        placeholder="Example: antibiotics, diabetes, cardiovascular drugs"
    )

    if st.button("🔎 START INVESTIGATION"):

        client = get_gemini_client()

        if client is None:

            st.error(
                "Gemini API key is not connected. "
                "Add GEMINI_API_KEY to Streamlit Secrets."
            )

        else:

            prompt = f"""
You are an educational pharmacy game master.

Create a Drug Detective mystery for a Pharm-D student.

Topic:
{topic if topic else "General Pharmacology"}

Give:

1. A short fictional patient situation
2. Three clinical clues
3. Four possible medicines

Do NOT reveal the correct answer.

Make it challenging but educational.

This is an educational simulation only.
Do not provide personalized medical advice.
"""

            try:

                with st.spinner(
                    "🧠 Building your mystery..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                st.markdown("### 🔍 CASE FILE")

                st.write(response.text)

            except Exception as e:

                st.error(
                    "Gemini could not generate the case."
                )

                st.code(str(e))


# ============================================================
# PATIENT CASE
# ============================================================

elif page == "🩺 Patient Case":

    st.html(
        """
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    🎮 PLAY & PRACTICE
                </div>

                <div class="top-title">
                    🩺 Patient Case
                </div>

                <div class="top-subtitle">
                    Think like a clinical pharmacist.
                </div>

            </div>

        </div>
        """
    )

    st.info(
        "This is a fictional educational clinical pharmacy simulation."
    )

    condition = st.text_input(
        "Choose a condition",
        placeholder="Example: hypertension, asthma, diabetes"
    )

    if st.button("🩺 GENERATE CASE"):

        client = get_gemini_client()

        if client is None:

            st.error(
                "Gemini API key is not connected. "
                "Add GEMINI_API_KEY to Streamlit Secrets."
            )

        else:

            prompt = f"""
Create a fictional educational clinical pharmacy case.

Condition:
{condition if condition else "Hypertension"}

Include:

- Fictional patient background
- Presenting complaint
- Medication history
- Relevant laboratory information
- Important clues
- Clinical reasoning questions

This is an educational simulation only.
Do not provide personalized medical advice.
"""

            try:

                with st.spinner(
                    "🩺 Preparing the patient..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                st.markdown("### 🧑‍⚕️ PATIENT FILE")

                st.write(response.text)

            except Exception as e:

                st.error("Gemini error")

                st.code(str(e))


# ============================================================
# AI PATIENT
# ============================================================

elif page == "🗣️ AI Patient":

    st.html(
        """
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    🧠 COUNSELLING LAB
                </div>

                <div class="top-title">
                    🗣️ AI Patient
                </div>

                <div class="top-subtitle">
                    Practice your communication with realistic patient personalities.
                </div>

            </div>

        </div>
        """
    )

    personality = st.selectbox(
        "Patient personality",
        [
            "Anxious",
            "Angry",
            "Confused",
            "Non-adherent",
            "Friendly"
        ]
    )

    message = st.text_area(
        "What would you say to the patient?",
        height=130
    )

    if st.button("💬 TALK TO PATIENT"):

        client = get_gemini_client()

        if client is None:

            st.error(
                "Gemini API key is not connected. "
                "Add GEMINI_API_KEY to Streamlit Secrets."
            )

        elif not message:

            st.warning(
                "Enter something to say to the patient."
            )

        else:

            prompt = f"""
You are a fictional patient in a pharmacy counselling simulation.

Patient personality:
{personality}

Pharmacy student's message:
{message}

Respond naturally as the patient.

Keep the conversation realistic.

This is communication practice only.
Do not provide medical advice.
"""

            try:

                with st.spinner(
                    "🗣️ Patient is responding..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                st.markdown("### 🧑 PATIENT")

                st.write(response.text)

            except Exception as e:

                st.error("Gemini error")

                st.code(str(e))


# ============================================================
# AI QUIZ
# ============================================================

elif page == "❓ AI Quiz":

    st.html(
        """
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    🧠 LEARNING LAB
                </div>

                <div class="top-title">
                    ❓ AI Pharmacy Quiz
                </div>

                <div class="top-subtitle">
                    Generate a pharmacy challenge around the topic you choose.
                </div>

            </div>

        </div>
        """
    )

    topic = st.text_input(
        "Quiz topic",
        placeholder="Example: autonomic nervous system pharmacology"
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    number = st.slider(
        "Number of questions",
        1,
        10,
        5
    )

    if st.button("🧠 CREATE QUIZ"):

        client = get_gemini_client()

        if client is None:

            st.error(
                "Gemini API key is not connected. "
                "Add GEMINI_API_KEY to Streamlit Secrets."
            )

        else:

            prompt = f"""
You are a pharmacy education game master.

Create {number} MCQs for a Pharm-D student.

Topic:
{topic if topic else "General Pharmacy"}

Difficulty:
{difficulty}

Each question must have:

A
B
C
D

At the end give an ANSWER KEY.

Do not give explanations unless requested.

This is an educational quiz.
"""

            try:

                with st.spinner(
                    "🧠 Building your quiz..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                st.markdown("### 📚 YOUR CHALLENGE")

                st.write(response.text)

            except Exception as e:

                st.error("Gemini error")

                st.code(str(e))


# ============================================================
# COMING SOON MISSIONS
# ============================================================

elif page in [
    "⚔️ Pharma Battle",
    "🔐 Escape Room",
    "🧬 Build the Patient",
    "🔥 Daily Challenge"
]:

    st.html(
        f"""
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    🚀 PHARMAQUEST ROADMAP
                </div>

                <div class="top-title">
                    {page}
                </div>

                <div class="top-subtitle">
                    An interactive pharmacy experience is being prepared.
                </div>

            </div>

        </div>

        <div class="page-card" style="text-align:center;">

            <div style="
                font-size:58px;
            ">
                🚀
            </div>

            <h2>
                Mission Loading
            </h2>

            <p style="
                color:#94a3b8;
                font-size:13px;
            ">
                This feature is part of the PharmaQuest roadmap.
                The mission mechanics will be added next.
            </p>

        </div>
        """
    )


# ============================================================
# PROFILE
# ============================================================

elif page == "🏆 My Profile":

    st.html(
        f"""
        <div class="topbar">

            <div>

                <div class="eyebrow">
                    👤 STUDENT PROFILE
                </div>

                <div class="top-title">
                    My Pharmacy Profile
                </div>

                <div class="top-subtitle">
                    Your achievements and learning identity.
                </div>

            </div>

        </div>

        <div class="page-card">

            <div class="page-badge">
                LEVEL {level_number}
            </div>

            <h2>
                🧬 {level_name}
            </h2>

            <p>
                Your PharmaQuest journey is just beginning.
            </p>

            <div style="
                margin-top:25px;
                padding:18px;
                border-radius:18px;
                background:#101628;
                border:1px solid rgba(255,255,255,0.08);
            ">

                <strong style="color:#ffffff;">
                    ⭐ {st.session_state.xp} XP
                </strong>

                <br>

                <span style="
                    color:#64748b;
                    font-size:11px;
                ">
                    Experience earned
                </span>

            </div>

        </div>
        """
    )
