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

INITIAL_XP = 0
INITIAL_LEVEL = 1
INITIAL_STREAK = 0
INITIAL_BADGES = 0
INITIAL_MISSIONS = 0

RANK_NAME = "Pharma Initiate"

if "xp" not in st.session_state:
    st.session_state.xp = INITIAL_XP

if "level" not in st.session_state:
    st.session_state.level = INITIAL_LEVEL

if "streak" not in st.session_state:
    st.session_state.streak = INITIAL_STREAK

if "badges" not in st.session_state:
    st.session_state.badges = INITIAL_BADGES

if "missions_completed" not in st.session_state:
    st.session_state.missions_completed = INITIAL_MISSIONS


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
        )
        * 100
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

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(168,85,247,0.10),
                transparent 23%
            ),
            radial-gradient(
                circle at 95% 8%,
                rgba(16,185,129,0.10),
                transparent 22%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(249,115,22,0.07),
                transparent 28%
            ),
            #fafaf9;
    }

    .block-container {

        max-width: 1450px;

        padding-top: 1.5rem;

        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #fff7ed 0%,
                #faf5ff 48%,
                #ecfdf5 100%
            );

        border-right:
            1px solid #e5e7eb;
    }

    .sidebar-brand {

        padding:
            10px 5px 18px 5px;
    }

    .brand-row {

        display: flex;

        align-items: center;

        gap: 12px;
    }

    .sidebar-logo {

        width: 53px;
        height: 53px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 17px;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #db2777,
                #f97316
            );

        box-shadow:
            0 12px 25px
            rgba(124,58,237,0.24);

        font-size: 27px;
    }

    .sidebar-title {

        color: #18181b;

        font-size: 20px;

        font-weight: 950;

        letter-spacing: -0.6px;
    }

    .sidebar-subtitle {

        margin-top: 2px;

        color: #78716c;

        font-size: 8px;

        font-weight: 900;

        letter-spacing: 1.3px;
    }

    .sidebar-section {

        margin-top: 18px;

        margin-bottom: 7px;

        color: #a16207;

        font-size: 9px;

        font-weight: 950;

        letter-spacing: 1.5px;
    }

    .sidebar-section.play {

        color: #7c3aed;
    }

    .sidebar-section.learn {

        color: #059669;
    }

    .sidebar-section.account {

        color: #db2777;
    }

    .sidebar-footer-card {

        margin-top: 18px;

        padding: 15px;

        border-radius: 18px;

        background: rgba(255,255,255,0.85);

        border: 1px solid #e7e5e4;

        box-shadow:
            0 10px 25px
            rgba(28,25,23,0.05);
    }

    .footer-label {

        color: #a8a29e;

        font-size: 8px;

        font-weight: 900;

        letter-spacing: 1px;
    }

    .footer-rank {

        margin-top: 4px;

        color: #7c3aed;

        font-size: 15px;

        font-weight: 950;
    }


    /* ======================================================
       TOP BAR
       ====================================================== */

    .topbar {

        display: flex;

        justify-content: space-between;

        align-items: center;

        margin-bottom: 20px;
    }

    .eyebrow {

        color: #7c3aed;

        font-size: 9px;

        font-weight: 950;

        letter-spacing: 1.8px;
    }

    .top-title {

        margin-top: 4px;

        color: #18181b;

        font-size: 30px;

        font-weight: 950;

        letter-spacing: -1.2px;
    }

    .top-subtitle {

        margin-top: 3px;

        color: #78716c;

        font-size: 12px;
    }


    /* ======================================================
       WELCOME CARD
       ====================================================== */

    .welcome-card {

        position: relative;

        overflow: hidden;

        padding: 34px;

        border-radius: 30px;

        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(251,191,36,0.28),
                transparent 20%
            ),
            radial-gradient(
                circle at 15% 90%,
                rgba(236,72,153,0.20),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #4c1d95,
                #7c3aed 48%,
                #db2777
            );

        box-shadow:
            0 25px 60px
            rgba(91,33,182,0.20);
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

        color: #fef3c7;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1.5px;
    }

    .welcome-title {

        margin-top: 15px;

        color: white;

        font-size: 37px;

        line-height: 1.1;

        font-weight: 950;

        letter-spacing: -1.5px;
    }

    .welcome-text {

        max-width: 650px;

        margin-top: 10px;

        color: #f5f3ff;

        font-size: 13px;

        line-height: 1.6;
    }

    .welcome-pill {

        display: inline-block;

        margin-top: 19px;

        padding: 9px 14px;

        border-radius: 12px;

        background:
            rgba(255,255,255,0.12);

        color: white;

        font-size: 10px;

        font-weight: 850;
    }


    /* ======================================================
       QUICK STATS
       ====================================================== */

    .stats-area {

        margin-top: 20px;
    }

    .mini-card {

        min-height: 125px;

        padding: 20px;

        border-radius: 21px;

        background: white;

        border: 1px solid #e7e5e4;

        box-shadow:
            0 10px 25px
            rgba(28,25,23,0.05);

        transition: 0.25s ease;
    }

    .mini-card:hover {

        transform: translateY(-4px);

        box-shadow:
            0 18px 35px
            rgba(28,25,23,0.09);
    }

    .mini-icon {

        font-size: 25px;
    }

    .mini-number {

        margin-top: 5px;

        color: #18181b;

        font-size: 25px;

        font-weight: 950;
    }

    .mini-label {

        color: #78716c;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1px;
    }

    .mini-description {

        margin-top: 4px;

        color: #a8a29e;

        font-size: 9px;
    }


    /* ======================================================
       LEVEL CARD
       ====================================================== */

    .level-card {

        margin-top: 20px;

        padding: 23px;

        border-radius: 23px;

        background: white;

        border: 1px solid #e7e5e4;

        box-shadow:
            0 10px 25px
            rgba(28,25,23,0.05);
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

        width: 55px;
        height: 55px;

        border-radius: 17px;

        background:
            linear-gradient(
                135deg,
                #f59e0b,
                #f97316
            );

        color: white;

        font-size: 16px;

        font-weight: 950;

        box-shadow:
            0 10px 22px
            rgba(249,115,22,0.20);
    }

    .level-title {

        flex: 1;

        margin-left: 15px;
    }

    .level-small {

        color: #a8a29e;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1px;
    }

    .level-name {

        margin-top: 3px;

        color: #18181b;

        font-size: 18px;

        font-weight: 950;
    }

    .level-xp {

        color: #7c3aed;

        font-size: 11px;

        font-weight: 950;
    }

    .level-track {

        margin-top: 17px;

        width: 100%;

        height: 10px;

        overflow: hidden;

        border-radius: 999px;

        background: #f1f5f9;
    }

    .level-fill {

        height: 100%;

        width: 0%;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #ec4899,
                #f59e0b
            );
    }

    .level-bottom {

        display: flex;

        justify-content: space-between;

        margin-top: 7px;

        color: #a8a29e;

        font-size: 9px;
    }


    /* ======================================================
       SECTION
       ====================================================== */

    .section-heading {

        margin-top: 31px;

        margin-bottom: 5px;

        color: #18181b;

        font-size: 23px;

        font-weight: 950;

        letter-spacing: -0.6px;
    }

    .section-caption {

        margin-bottom: 16px;

        color: #78716c;

        font-size: 11px;
    }


    /* ======================================================
       MISSION CARDS
       ====================================================== */

    .mission-card {

        min-height: 235px;

        padding: 21px;

        margin-bottom: 17px;

        border-radius: 23px;

        background: white;

        border: 1px solid #e7e5e4;

        box-shadow:
            0 10px 25px
            rgba(28,25,23,0.05);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }

    .mission-card:hover {

        transform: translateY(-6px);

        box-shadow:
            0 22px 40px
            rgba(28,25,23,0.10);
    }

    .mission-top {

        display: flex;

        justify-content: space-between;

        align-items: center;
    }

    .mission-icon {

        width: 54px;
        height: 54px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 17px;

        font-size: 27px;
    }

    .icon-purple {

        background: #f3e8ff;
    }

    .icon-green {

        background: #d1fae5;
    }

    .icon-orange {

        background: #ffedd5;
    }

    .icon-pink {

        background: #fce7f3;
    }

    .icon-yellow {

        background: #fef3c7;
    }

    .icon-teal {

        background: #ccfbf1;
    }

    .mission-tag {

        padding: 6px 9px;

        border-radius: 999px;

        background: #fafaf9;

        color: #78716c;

        font-size: 7px;

        font-weight: 950;

        letter-spacing: 1px;
    }

    .mission-name {

        margin-top: 16px;

        color: #18181b;

        font-size: 17px;

        font-weight: 950;
    }

    .mission-description {

        min-height: 55px;

        margin-top: 7px;

        color: #78716c;

        font-size: 10px;

        line-height: 1.55;
    }

    .mission-reward {

        margin-top: 12px;

        color: #f59e0b;

        font-size: 9px;

        font-weight: 950;
    }


    /* ======================================================
       OTHER PAGES
       ====================================================== */

    .page-card {

        padding: 30px;

        border-radius: 25px;

        background: white;

        border: 1px solid #e7e5e4;

        box-shadow:
            0 12px 30px
            rgba(28,25,23,0.06);
    }

    .page-badge {

        display: inline-block;

        padding: 7px 11px;

        border-radius: 999px;

        background: #f3e8ff;

        color: #7c3aed;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: 1px;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        min-height: 44px;

        border-radius: 13px;

        border: none;

        font-weight: 850;

        transition: 0.2s ease;
    }

    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 8px 20px
            rgba(124,58,237,0.15);
    }


    /* ======================================================
       MOBILE
       ====================================================== */

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
        label_visibility="collapsed"
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
        label_visibility="collapsed"
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
        label_visibility="collapsed"
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
        label_visibility="collapsed"
    )


# ============================================================
# DETERMINE PAGE
# ============================================================

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
                color:#78716c;
                font-weight:700;
            ">
                ⭐ {st.session_state.xp} XP
            </div>

            <div style="
                margin-top:8px;
                height:6px;
                border-radius:10px;
                background:#e7e5e4;
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
# HOME
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
                    style="width:{progress_percent}%;">
                </div>

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
            Mission Hub
        </div>

        <div class="section-caption">
            Choose how you want to train today.
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
            "icon-purple"
        ),

        (
            "🩺",
            "Patient Case",
            "Think like a clinical pharmacist and solve a fictional case.",
            "CLINICAL",
            "+75 XP",
            "icon-green"
        ),

        (
            "🗣️",
            "AI Patient",
            "Practice counselling with realistic patient personalities.",
            "COUNSELLING",
            "+60 XP",
            "icon-pink"
        ),

        (
            "⚔️",
            "Pharma Battle",
            "Answer rapid-fire pharmacy questions.",
            "BATTLE",
            "+50 XP",
            "icon-orange"
        ),

        (
            "🔐",
            "Escape Room",
            "Solve a pharmacy mystery before time runs out.",
            "MYSTERY",
            "+100 XP",
            "icon-purple"
        ),

        (
            "🧬",
            "Build the Patient",
            "Explore treatment decisions in a fictional patient.",
            "SIMULATION",
            "+100 XP",
            "icon-teal"
        ),

        (
            "❓",
            "AI Quiz",
            "Create a personalized pharmacy quiz with AI.",
            "KNOWLEDGE",
            "+50 XP",
            "icon-yellow"
        ),

        (
            "🔥",
            "Daily Challenge",
            "Complete today's challenge and earn bonus XP.",
            "DAILY",
            "+75 XP",
            "icon-orange"
        )

    ]


    columns = st.columns(4)


    for i, mission in enumerate(missions):

        icon, title, description, category, reward, icon_class = mission

        with columns[i % 4]:

            st.html(
                f"""
                <div class="mission-card">

                    <div class="mission-top">

                        <div class="
                            mission-icon
                            {icon_class}
                        ">
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
                    Your pharmacy learning journey starts here.
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
                    style="width:{progress_percent}%;">
                </div>

            </div>

            <p style="
                color:#78716c;
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
                color:#78716c;
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

            <p style="
                color:#78716c;
            ">
                Your PharmaQuest journey is just beginning.
            </p>

            <div style="
                margin-top:25px;
                padding:18px;
                border-radius:18px;
                background:#fafaf9;
                border:1px solid #e7e5e4;
            ">

                <strong>
                    ⭐ {st.session_state.xp} XP
                </strong>

                <br>

                <span style="
                    color:#78716c;
                    font-size:11px;
                ">
                    Experience earned
                </span>

            </div>

        </div>
        """
    )
