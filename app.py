import streamlit as st
from google import genai
from supabase import create_client


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PharmaQuest",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "user": None,
    "profile": None,
    "page": "Home",
    "login_mode": "login",
    "drug_case": None,
    "patient_case": None,
    "quiz": None,
    "patient_reply": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SUPABASE
# =========================================================

def get_supabase():
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")

        if not url or not key:
            return None

        return create_client(url, key)

    except Exception:
        return None


supabase = get_supabase()


# =========================================================
# GEMINI
# =========================================================

def get_gemini():

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# =========================================================
# LEVEL SYSTEM
# =========================================================

def get_level_info(xp):

    if xp < 500:
        return 1, "🧬 Pharma Initiate", 500

    if xp < 1200:
        return 2, "🔎 Drug Seeker", 1200

    if xp < 2500:
        return 3, "⚗️ Pharma Strategist", 2500

    if xp < 4500:
        return 4, "🩺 Clinical Specialist", 4500

    if xp < 7000:
        return 5, "🧠 Therapeutics Master", 7000

    return 6, "🏆 PharmaQuest Elite", 10000


# =========================================================
# LOAD PROFILE
# =========================================================

def load_profile():

    if not supabase or not st.session_state.user:
        return None

    try:

        result = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", st.session_state.user.id)
            .execute()
        )

        if result.data:
            return result.data[0]

    except Exception:
        return None

    return None


# =========================================================
# CREATE PROFILE
# =========================================================

def create_profile(user, username):

    if not supabase:
        return None

    data = {
        "id": user.id,
        "username": username,
        "xp": 0,
        "level": 1,
        "streak": 0,
        "badges": 0,
        "missions_completed": 0,
    }

    try:

        result = (
            supabase
            .table("profiles")
            .insert(data)
            .execute()
        )

        if result.data:
            return result.data[0]

    except Exception:
        return None

    return None


# =========================================================
# SAVE PROGRESS
# =========================================================

def save_progress(xp_add=0, mission_complete=False):

    if not supabase:
        return

    if not st.session_state.user:
        return

    profile = st.session_state.profile

    if not profile:
        return

    old_xp = profile.get("xp", 0)
    new_xp = old_xp + xp_add

    missions = profile.get(
        "missions_completed",
        0
    )

    if mission_complete:
        missions += 1

    level, title, next_xp = get_level_info(new_xp)

    update_data = {
        "xp": new_xp,
        "level": level,
        "missions_completed": missions,
    }

    try:

        result = (
            supabase
            .table("profiles")
            .update(update_data)
            .eq(
                "id",
                st.session_state.user.id
            )
            .execute()
        )

        if result.data:
            st.session_state.profile = result.data[0]
        else:
            st.session_state.profile.update(update_data)

    except Exception as e:

        st.error(
            f"Could not save progress: {str(e)}"
        )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    if supabase:

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

    st.session_state.user = None
    st.session_state.profile = None
    st.session_state.page = "Home"
    st.session_state.login_mode = "login"

    st.rerun()


# =========================================================
# GLOBAL DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(236,72,153,0.08),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(20,184,166,0.08),
                transparent 25%
            ),
            #fffafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    footer {
        visibility: hidden;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #fff7fb 0%,
                #faf5ff 50%,
                #f0fdfa 100%
            );

        border-right: 1px solid #eee5f4;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    section[data-testid="stSidebar"] .stButton button {

        width: 100%;

        border: 1px solid transparent;

        border-radius: 13px;

        padding: 0.62rem 0.8rem;

        background: transparent;

        color: #40384f;

        text-align: left;

        font-weight: 650;

        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"]
    .stButton button:hover {

        background: #f3e8ff;

        border-color: #e9d5ff;

        transform: translateX(3px);
    }


    /* =====================================================
       LOGIN PAGE
    ===================================================== */

    .login-shell {

        max-width: 1000px;

        margin: 2rem auto 1rem auto;

        text-align: center;
    }

    .login-logo {

        width: 90px;
        height: 90px;

        margin: auto;

        border-radius: 28px;

        display: flex;

        align-items: center;
        justify-content: center;

        font-size: 3.5rem;

        background:
            linear-gradient(
                135deg,
                #ec4899,
                #8b5cf6
            );

        box-shadow:
            0 15px 35px
            rgba(236,72,153,0.25);
    }

    .login-title {

        margin-top: 1rem;

        font-size: 3rem;

        font-weight: 950;

        color: #31243f;
    }

    .login-subtitle {

        color: #81758d;

        font-size: 1.05rem;

        margin-bottom: 1.8rem;
    }

    .login-panel {

        background: rgba(255,255,255,0.96);

        border: 1px solid #eee5f4;

        border-radius: 28px;

        padding: 2rem;

        box-shadow:
            0 20px 60px
            rgba(70,40,90,0.10);
    }


    /* =====================================================
       HERO
    ===================================================== */

    .home-hero {

        position: relative;

        overflow: hidden;

        border-radius: 30px;

        padding: 2.4rem;

        background:
            linear-gradient(
                120deg,
                #8b5cf6 0%,
                #ec4899 52%,
                #f97316 100%
            );

        color: white;

        box-shadow:
            0 18px 45px
            rgba(139,92,246,0.20);
    }

    .home-hero:after {

        content: "";

        position: absolute;

        width: 220px;
        height: 220px;

        border-radius: 50%;

        background: rgba(255,255,255,0.10);

        right: -70px;
        top: -80px;
    }

    .home-hero h1 {

        font-size: 2.55rem;

        font-weight: 950;

        margin: 0;
    }

    .home-hero p {

        font-size: 1.05rem;

        margin-top: 0.6rem;

        opacity: 0.94;
    }


    /* =====================================================
       STAT CARDS
    ===================================================== */

    .stat-card {

        min-height: 125px;

        padding: 1.2rem;

        border-radius: 21px;

        background: white;

        border: 1px solid #eee5f4;

        box-shadow:
            0 10px 28px
            rgba(80,50,100,0.07);
    }

    .stat-icon {

        font-size: 1.6rem;
    }

    .stat-number {

        font-size: 1.65rem;

        font-weight: 900;

        color: #33263d;

        margin-top: 4px;
    }

    .stat-label {

        color: #8b8193;

        font-size: 0.85rem;
    }


    /* =====================================================
       SECTION
    ===================================================== */

    .section-title {

        font-size: 1.9rem;

        font-weight: 900;

        color: #33263d;

        margin-top: 2rem;
    }

    .section-subtitle {

        color: #8b8193;

        margin-bottom: 1.2rem;
    }


    /* =====================================================
       GAME CARDS
    ===================================================== */

    div.st-key-card_drug button,
    div.st-key-card_case button,
    div.st-key-card_patient button,
    div.st-key-card_battle button,
    div.st-key-card_escape button,
    div.st-key-card_build button,
    div.st-key-card_quiz button,
    div.st-key-card_daily button {

        min-height: 235px;

        width: 100%;

        border: none !important;

        border-radius: 25px !important;

        color: white !important;

        text-align: left !important;

        white-space: pre-wrap !important;

        padding: 1.5rem !important;

        font-size: 1rem !important;

        font-weight: 700 !important;

        box-shadow:
            0 15px 35px
            rgba(50,40,80,0.14);

        transition:
            transform 0.22s ease,
            box-shadow 0.22s ease;
    }


    div.st-key-card_drug button {

        background:
            linear-gradient(
                135deg,
                #ec4899,
                #8b5cf6
            ) !important;
    }

    div.st-key-card_case button {

        background:
            linear-gradient(
                135deg,
                #14b8a6,
                #0891b2
            ) !important;
    }

    div.st-key-card_patient button {

        background:
            linear-gradient(
                135deg,
                #f472b6,
                #a855f7
            ) !important;
    }

    div.st-key-card_battle button {

        background:
            linear-gradient(
                135deg,
                #fb923c,
                #ef4444
            ) !important;
    }

    div.st-key-card_escape button {

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            ) !important;
    }

    div.st-key-card_build button {

        background:
            linear-gradient(
                135deg,
                #10b981,
                #14b8a6
            ) !important;
    }

    div.st-key-card_quiz button {

        background:
            linear-gradient(
                135deg,
                #f59e0b,
                #f97316
            ) !important;
    }

    div.st-key-card_daily button {

        background:
            linear-gradient(
                135deg,
                #f43f5e,
                #ec4899
            ) !important;
    }


    div.st-key-card_drug button:hover,
    div.st-key-card_case button:hover,
    div.st-key-card_patient button:hover,
    div.st-key-card_battle button:hover,
    div.st-key-card_escape button:hover,
    div.st-key-card_build button:hover,
    div.st-key-card_quiz button:hover,
    div.st-key-card_daily button:hover {

        transform:
            translateY(-7px)
            scale(1.015);

        box-shadow:
            0 24px 45px
            rgba(50,40,80,0.22);
    }


    /* =====================================================
       GAME HEADER
    ===================================================== */

    .game-header {

        padding: 2rem;

        border-radius: 26px;

        background: white;

        border: 1px solid #eee5f4;

        box-shadow:
            0 12px 35px
            rgba(70,40,90,0.07);

        margin-bottom: 1.5rem;
    }

    .game-header h1 {

        font-weight: 950;

        color: #33263d;
    }

    .game-header p {

        color: #81758d;
    }


    /* =====================================================
       PROGRESS
    ===================================================== */

    .progress-panel {

        margin-top: 1.5rem;

        padding: 1.5rem;

        background: white;

        border-radius: 22px;

        border: 1px solid #eee5f4;

        box-shadow:
            0 10px 30px
            rgba(60,40,90,0.06);
    }

    .progress-bar {

        height: 13px;

        border-radius: 20px;

        background: #f0eaf5;

        overflow: hidden;

        margin-top: 0.7rem;
    }

    .progress-fill {

        height: 100%;

        border-radius: 20px;

        background:
            linear-gradient(
                90deg,
                #8b5cf6,
                #ec4899,
                #f97316
            );
    }


    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton button[kind="primary"] {

        border: none;

        border-radius: 13px;

        font-weight: 800;

        padding: 0.7rem 1.4rem;

        background:
            linear-gradient(
                90deg,
                #8b5cf6,
                #ec4899
            );
    }


    /* =====================================================
       INPUTS
    ===================================================== */

    .stTextInput input,
    .stTextArea textarea {

        border-radius: 13px !important;

        border: 1px solid #ddd4e5 !important;

        background: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN / SIGNUP
# =========================================================

def login_page():

    st.markdown(
        """
        <div class="login-shell">

            <div class="login-logo">
                💊
            </div>

            <div class="login-title">
                PharmaQuest
            </div>

            <div class="login-subtitle">
                Learn Pharmacy • Solve Cases • Build Clinical Confidence
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 1.35, 1]
    )

    with center:

        st.markdown(
            '<div class="login-panel">',
            unsafe_allow_html=True
        )

        if st.session_state.login_mode == "login":

            st.markdown("### 👋 Welcome back")
            st.write(
                "Log in to continue your pharmacy learning journey."
            )

            email = st.text_input(
                "Email",
                placeholder="student@example.com",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "🚀 LOGIN TO PHARMAQUEST",
                type="primary",
                use_container_width=True
            ):

                if not email or not password:

                    st.error(
                        "Please enter your email and password."
                    )

                elif not supabase:

                    st.error(
                        "Supabase is not connected."
                    )

                else:

                    try:

                        result = (
                            supabase.auth
                            .sign_in_with_password(
                                {
                                    "email": email,
                                    "password": password
                                }
                            )
                        )

                        if result.user:

                            st.session_state.user = result.user

                            profile = load_profile()

                            if not profile:

                                username = (
                                    result.user.user_metadata.get(
                                        "username"
                                    )
                                    or email.split("@")[0]
                                )

                                profile = create_profile(
                                    result.user,
                                    username
                                )

                            st.session_state.profile = profile
                            st.session_state.page = "Home"

                            st.rerun()

                        else:

                            st.error(
                                "Login was not successful."
                            )

                    except Exception as e:

                        st.error(
                            f"Login failed: {str(e)}"
                        )

            st.markdown("---")

            st.write(
                "Don't have a PharmaQuest account?"
            )

            if st.button(
                "✨ CREATE NEW ACCOUNT",
                use_container_width=True
            ):

                st.session_state.login_mode = "signup"
                st.rerun()

        else:

            st.markdown("### ✨ Create your account")

            st.write(
                "Your own account will keep your XP and progress."
            )

            username = st.text_input(
                "Username",
                placeholder="e.g. Aiman",
                key="signup_username"
            )

            email = st.text_input(
                "Email",
                placeholder="student@example.com",
                key="signup_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                key="signup_confirm"
            )

            if st.button(
                "🎓 CREATE MY ACCOUNT",
                type="primary",
                use_container_width=True
            ):

                if not username or not email or not password:

                    st.error(
                        "Please complete all fields."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(password) < 6:

                    st.error(
                        "Password must contain at least 6 characters."
                    )

                elif not supabase:

                    st.error(
                        "Supabase is not connected."
                    )

                else:

                    try:

                        result = supabase.auth.sign_up(
                            {
                                "email": email,
                                "password": password,
                                "options": {
                                    "data": {
                                        "username": username
                                    }
                                }
                            }
                        )

                        if result.user:

                            if result.session:

                                profile = create_profile(
                                    result.user,
                                    username
                                )

                                st.session_state.user = result.user
                                st.session_state.profile = profile
                                st.session_state.page = "Home"

                                st.rerun()

                            else:

                                st.success(
                                    "Account created successfully. "
                                    "Please confirm your email, "
                                    "then return here and log in."
                                )

                        else:

                            st.error(
                                "Could not create the account."
                            )

                    except Exception as e:

                        st.error(
                            f"Signup failed: {str(e)}"
                        )

            st.markdown("---")

            if st.button(
                "← BACK TO LOGIN",
                use_container_width=True
            ):

                st.session_state.login_mode = "login"
                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# SIDEBAR
# =========================================================

def sidebar():

    profile = st.session_state.profile

    username = profile.get(
        "username",
        "Student"
    )

    xp = profile.get(
        "xp",
        0
    )

    level, title, next_xp = get_level_info(xp)

    with st.sidebar:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:8px 0 18px 0;
            ">

                <div style="
                    font-size:3rem;
                ">
                    💊
                </div>

                <div style="
                    font-size:1.45rem;
                    font-weight:900;
                    color:#3b2947;
                ">
                    PharmaQuest
                </div>

                <div style="
                    color:#8a7c91;
                    font-size:0.78rem;
                ">
                    Pharmacy Learning Arena
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:19px;
                background:
                    linear-gradient(
                        135deg,
                        #8b5cf6,
                        #ec4899
                    );
                color:white;
                margin-bottom:18px;
                box-shadow:
                    0 10px 25px
                    rgba(139,92,246,0.18);
            ">

                <div style="
                    font-size:0.72rem;
                    opacity:0.85;
                    font-weight:700;
                ">
                    CURRENT JOURNEY
                </div>

                <div style="
                    font-size:1.02rem;
                    font-weight:850;
                    margin-top:5px;
                ">
                    {title}
                </div>

                <div style="
                    margin-top:6px;
                    font-size:0.8rem;
                ">
                    Level {level} • {xp} XP
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 🧭 MAIN")

        if st.button(
            "🏠  Home Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "Home"
            st.rerun()

        if st.button(
            "📊  My Progress",
            use_container_width=True
        ):

            st.session_state.page = "Progress"
            st.rerun()

        st.markdown("### 🎮 PLAY & PRACTICE")

        menu_items = [
            ("🕵️  Drug Detective", "Drug Detective"),
            ("🩺  Patient Case", "Patient Case"),
            ("🗣️  AI Patient", "AI Patient"),
            ("⚔️  Pharma Battle", "Pharma Battle"),
            ("🔐  Escape Room", "Escape Room"),
            ("🧬  Build the Patient", "Build the Patient"),
        ]

        for label, page in menu_items:

            if st.button(
                label,
                use_container_width=True
            ):

                st.session_state.page = page
                st.rerun()

        st.markdown("### 🧠 LEARN")

        if st.button(
            "❓  AI Quiz",
            use_container_width=True
        ):

            st.session_state.page = "AI Quiz"
            st.rerun()

        if st.button(
            "🔥  Daily Challenge",
            use_container_width=True
        ):

            st.session_state.page = "Daily Challenge"
            st.rerun()

        st.markdown("### 👤 ACCOUNT")

        if st.button(
            "🏆  My Profile",
            use_container_width=True
        ):

            st.session_state.page = "Profile"
            st.rerun()

        st.markdown("---")

        if st.button(
            "🚪  Logout",
            use_container_width=True
        ):

            logout()


# =========================================================
# HOME DASHBOARD
# =========================================================

def home_page():

    profile = st.session_state.profile

    username = profile.get(
        "username",
        "Future Pharmacist"
    )

    xp = profile.get(
        "xp",
        0
    )

    missions = profile.get(
        "missions_completed",
        0
    )

    level, title, next_xp = get_level_info(xp)

    st.markdown(
        f"""
        <div class="home-hero">

            <h1>
                Hey, {username}! 👋
            </h1>

            <p>
                Welcome to your pharmacy learning arena.
                Choose a mission, practice your skills,
                and earn XP.
            </p>

            <div style="
                margin-top:15px;
                font-weight:800;
                font-size:1.05rem;
            ">
                {title} • Level {level}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    stats = [
        ("⚡", xp, "Total XP"),
        ("🎯", missions, "Missions Completed"),
        ("🔥", profile.get("streak", 0), "Day Streak"),
        ("🏆", profile.get("badges", 0), "Badges"),
    ]

    for column, stat in zip(
        [c1, c2, c3, c4],
        stats
    ):

        icon, number, label = stat

        with column:

            st.markdown(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        {icon}
                    </div>

                    <div class="stat-number">
                        {number}
                    </div>

                    <div class="stat-label">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="section-title">
            🎮 Choose Your Mission
        </div>

        <div class="section-subtitle">
            Practice, investigate, solve and earn XP.
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # ROW 1
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (
            c1,
            "🕵️\n\nDRUG DETECTIVE\n\n"
            "Investigate clues and identify mysterious medicines.\n\n"
            "+50 XP",
            "card_drug",
            "Drug Detective"
        ),
        (
            c2,
            "🩺\n\nPATIENT CASE\n\n"
            "Solve fictional clinical cases and choose the best therapy.\n\n"
            "+75 XP",
            "card_case",
            "Patient Case"
        ),
        (
            c3,
            "🗣️\n\nAI PATIENT\n\n"
            "Interview an AI patient and discover the clinical story.\n\n"
            "+60 XP",
            "card_patient",
            "AI Patient"
        ),
        (
            c4,
            "⚔️\n\nPHARMA BATTLE\n\n"
            "Test your pharmacy knowledge in competitive challenges.\n\n"
            "+100 XP",
            "card_battle",
            "Pharma Battle"
        ),
    ]

    for column, text, key, page in cards:

        with column:

            if st.button(
                text,
                key=key,
                use_container_width=True
            ):

                st.session_state.page = page
                st.rerun()

    # =====================================================
    # ROW 2
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (
            c1,
            "🔐\n\nESCAPE ROOM\n\n"
            "Solve pharmacy puzzles before time runs out.\n\n"
            "+100 XP",
            "card_escape",
            "Escape Room"
        ),
        (
            c2,
            "🧬\n\nBUILD THE PATIENT\n\n"
            "Construct the patient profile and treatment plan.\n\n"
            "+80 XP",
            "card_build",
            "Build the Patient"
        ),
        (
            c3,
            "❓\n\nAI QUIZ\n\n"
            "Challenge yourself with AI-generated pharmacy MCQs.\n\n"
            "+40 XP",
            "card_quiz",
            "AI Quiz"
        ),
        (
            c4,
            "🔥\n\nDAILY CHALLENGE\n\n"
            "Complete today's pharmacy challenge and keep your streak alive.\n\n"
            "+50 XP",
            "card_daily",
            "Daily Challenge"
        ),
    ]

    for column, text, key, page in cards:

        with column:

            if st.button(
                text,
                key=key,
                use_container_width=True
            ):

                st.session_state.page = page
                st.rerun()

    # =====================================================
    # LEVEL PROGRESS
    # =====================================================

    level_starts = {
        1: 0,
        2: 500,
        3: 1200,
        4: 2500,
        5: 4500,
        6: 7000,
    }

    current_start = level_starts.get(
        level,
        0
    )

    progress_range = max(
        next_xp - current_start,
        1
    )

    progress = min(
        max(
            (xp - current_start)
            / progress_range,
            0
        ),
        1
    )

    progress_percent = int(
        progress * 100
    )

    st.markdown(
        f"""
        <div class="progress-panel">

            <div style="
                display:flex;
                justify-content:space-between;
                font-weight:800;
                color:#3b3044;
            ">

                <span>
                    🧬 Level {level} • {title}
                </span>

                <span>
                    {xp} / {next_xp} XP
                </span>

            </div>

            <div class="progress-bar">

                <div
                    class="progress-fill"
                    style="width:{progress_percent}%"
                ></div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DRUG DETECTIVE
# =========================================================

def drug_detective():

    st.markdown(
        """
        <div class="game-header">

            <h1>🕵️ Drug Detective</h1>

            <p>
                Investigate clues. Think clinically.
                Identify the medicine.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Pharmacy topic",
        placeholder=(
            "Example: antibiotics, diabetes, "
            "cardiovascular drugs"
        )
    )

    if st.button(
        "🔎 START INVESTIGATION",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a pharmacy topic first."
            )

        else:

            client = get_gemini()

            if not client:

                st.error(
                    "Gemini API key is not configured."
                )

            else:

                prompt = f"""
You are creating a pharmacy education mystery game
for Pharm-D students.

Topic:
{topic}

Create a Drug Detective mystery.

Give:
1. Three clinical clues.
2. One mechanism clue.
3. One side-effect clue.
4. Ask the student to identify the drug.
5. Do NOT immediately reveal the answer.

Keep the case educational and fictional.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.session_state.drug_case = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.drug_case:

        st.markdown(
            "### 🔍 Mystery Case"
        )

        st.write(
            st.session_state.drug_case
        )

        if st.button(
            "✅ I solved the case!",
            type="primary",
            key="solve_drug"
        ):

            save_progress(
                xp_add=50,
                mission_complete=True
            )

            st.session_state.drug_case = None

            st.success(
                "Great work! +50 XP added."
            )


# =========================================================
# PATIENT CASE
# =========================================================

def patient_case():

    st.markdown(
        """
        <div class="game-header">

            <h1>🩺 Patient Case</h1>

            <p>
                Analyze the patient and make the best
                clinical decision.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Clinical topic",
        placeholder=(
            "Example: hypertension, diabetes, asthma"
        )
    )

    if st.button(
        "🩺 GENERATE CASE",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a clinical topic."
            )

        else:

            client = get_gemini()

            if not client:

                st.error(
                    "Gemini API key is missing."
                )

            else:

                prompt = f"""
Create a fictional pharmacy clinical case
for a Pharm-D student.

Topic:
{topic}

Include:
- patient age and sex
- chief complaint
- history
- relevant medicines
- vital/lab information
- three possible therapeutic decisions

Ask the student what they would recommend.

Do not give the answer immediately.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.session_state.patient_case = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.patient_case:

        st.markdown(
            "### 🩺 Clinical Case"
        )

        st.write(
            st.session_state.patient_case
        )

        if st.button(
            "🎯 Complete Case",
            type="primary",
            key="complete_patient_case"
        ):

            save_progress(
                xp_add=75,
                mission_complete=True
            )

            st.session_state.patient_case = None

            st.success(
                "Case completed! +75 XP."
            )


# =========================================================
# AI PATIENT
# =========================================================

def ai_patient():

    st.markdown(
        """
        <div class="game-header">

            <h1>🗣️ AI Patient</h1>

            <p>
                Practice patient interviewing and
                clinical questioning.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    condition = st.text_input(
        "Patient condition",
        placeholder="Example: diabetes"
    )

    question = st.text_input(
        "Ask your patient a question"
    )

    if st.button(
        "🗣️ TALK TO PATIENT",
        type="primary"
    ):

        client = get_gemini()

        if not client:

            st.error(
                "Gemini API key is missing."
            )

        elif not condition:

            st.warning(
                "Enter a patient condition."
            )

        elif not question:

            st.warning(
                "Ask the patient something."
            )

        else:

            prompt = f"""
Act as a fictional pharmacy patient.

Condition:
{condition}

Student question:
{question}

Respond naturally like a patient.
Do not act as a doctor.
Do not provide definitive medical diagnosis.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.session_state.patient_reply = response.text

            except Exception as e:

                st.error(
                    f"AI error: {str(e)}"
                )

    if st.session_state.patient_reply:

        st.markdown(
            "### 🗣️ Patient"
        )

        st.write(
            st.session_state.patient_reply
        )


# =========================================================
# AI QUIZ
# =========================================================

def ai_quiz():

    st.markdown(
        """
        <div class="game-header">

            <h1>❓ AI Quiz</h1>

            <p>
                Test your pharmacy knowledge with
                AI-generated MCQs.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Quiz topic",
        placeholder=(
            "Example: pharmacology, medicinal chemistry"
        )
    )

    if st.button(
        "🧠 GENERATE QUIZ",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a topic."
            )

        else:

            client = get_gemini()

            if not client:

                st.error(
                    "Gemini API key is missing."
                )

            else:

                prompt = f"""
Create 5 pharmacy MCQs for a Pharm-D student.

Topic:
{topic}

For every question provide:
A, B, C, D options.

Clearly identify the correct answer after
each question.

Keep the questions educational.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.session_state.quiz = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.quiz:

        st.markdown(
            "### 🧠 Your Quiz"
        )

        st.write(
            st.session_state.quiz
        )

        if st.button(
            "🏆 Complete Quiz",
            type="primary",
            key="complete_quiz"
        ):

            save_progress(
                xp_add=40,
                mission_complete=True
            )

            st.session_state.quiz = None

            st.success(
                "Quiz completed! +40 XP."
            )


# =========================================================
# PLACEHOLDER GAMES
# =========================================================

def placeholder_game(
    title,
    icon,
    description,
    xp
):

    st.markdown(
        f"""
        <div class="game-header">

            <h1>{icon} {title}</h1>

            <p>
                {description}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "🚧 This mission is ready for development."
    )

    st.write(
        "The mission is already connected "
        "to your PharmaQuest account and XP system."
    )

    if st.button(
        f"🎯 COMPLETE DEMO MISSION (+{xp} XP)",
        type="primary"
    ):

        save_progress(
            xp_add=xp,
            mission_complete=True
        )

        st.success(
            f"Mission completed! +{xp} XP."
        )


# =========================================================
# PROGRESS PAGE
# =========================================================

def progress_page():

    profile = st.session_state.profile

    xp = profile.get(
        "xp",
        0
    )

    level, title, next_xp = get_level_info(xp)

    st.markdown(
        """
        <div class="game-header">

            <h1>📊 My Progress</h1>

            <p>
                Track your journey toward becoming
                a pharmacy expert.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Level",
            level
        )

    with c2:

        st.metric(
            "XP",
            xp
        )

    with c3:

        st.metric(
            "Missions",
            profile.get(
                "missions_completed",
                0
            )
        )

    st.markdown(
        f"### {title}"
    )

    level_starts = {
        1: 0,
        2: 500,
        3: 1200,
        4: 2500,
        5: 4500,
        6: 7000,
    }

    start = level_starts.get(
        level,
        0
    )

    total = max(
        next_xp - start,
        1
    )

    progress = min(
        max(
            (xp - start) / total,
            0
        ),
        1
    )

    st.progress(progress)

    st.write(
        f"{xp} / {next_xp} XP"
    )


# =========================================================
# PROFILE PAGE
# =========================================================

def profile_page():

    profile = st.session_state.profile

    level, title, _ = get_level_info(
        profile.get("xp", 0)
    )

    st.markdown(
        """
        <div class="game-header">

            <h1>🏆 My Profile</h1>

            <p>
                Your personal PharmaQuest identity.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        ### 👤 {profile.get("username", "Student")}

        **Rank:** {title}

        **Level:** {level}

        **XP:** {profile.get("xp", 0)}

        **Missions completed:**
        {profile.get("missions_completed", 0)}

        **Badges:**
        {profile.get("badges", 0)}

        **Streak:**
        {profile.get("streak", 0)} days
        """
    )


# =========================================================
# MAIN APP
# =========================================================

if not st.session_state.user:

    login_page()

else:

    if not st.session_state.profile:

        st.session_state.profile = load_profile()

    if not st.session_state.profile:

        st.error(
            "Could not load your student profile."
        )

        st.stop()

    sidebar()

    page = st.session_state.page

    if page == "Home":

        home_page()

    elif page == "Progress":

        progress_page()

    elif page == "Profile":

        profile_page()

    elif page == "Drug Detective":

        drug_detective()

    elif page == "Patient Case":

        patient_case()

    elif page == "AI Patient":

        ai_patient()

    elif page == "AI Quiz":

        ai_quiz()

    elif page == "Pharma Battle":

        placeholder_game(
            "Pharma Battle",
            "⚔️",
            "Challenge your pharmacy knowledge.",
            100
        )

    elif page == "Escape Room":

        placeholder_game(
            "Escape Room",
            "🔐",
            "Solve pharmacy puzzles and escape.",
            100
        )

    elif page == "Build the Patient":

        placeholder_game(
            "Build the Patient",
            "🧬",
            "Build a patient profile and treatment strategy.",
            80
        )

    elif page == "Daily Challenge":

        placeholder_game(
            "Daily Challenge",
            "🔥",
            "Complete today's pharmacy challenge.",
            50
        )
