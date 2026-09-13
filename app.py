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
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SUPABASE
# =========================================================

def get_supabase():

    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        return None

    try:
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

    elif xp < 1200:
        return 2, "🔎 Drug Seeker", 1200

    elif xp < 2500:
        return 3, "⚗️ Pharma Strategist", 2500

    elif xp < 4500:
        return 4, "🩺 Clinical Specialist", 4500

    elif xp < 7000:
        return 5, "🧠 Therapeutics Master", 7000

    else:
        return 6, "🏆 PharmaQuest Elite", 10000


# =========================================================
# LOAD PROFILE
# =========================================================

def load_profile():

    if not supabase or not st.session_state.user:
        return None

    try:

        user_id = st.session_state.user.id

        result = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", user_id)
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

    try:

        data = {
            "id": user.id,
            "username": username,
            "xp": 0,
            "level": 1,
            "streak": 0,
            "badges": 0,
            "missions_completed": 0,
        }

        result = (
            supabase
            .table("profiles")
            .insert(data)
            .execute()
        )

        if result.data:
            return result.data[0]

    except Exception:
        pass

    return None


# =========================================================
# SAVE PROGRESS
# =========================================================

def save_progress(xp_add=0, mission_complete=False):

    if not supabase or not st.session_state.user:
        return

    profile = st.session_state.profile

    if not profile:
        return

    try:

        current_xp = profile.get("xp", 0)
        new_xp = current_xp + xp_add

        missions = profile.get(
            "missions_completed",
            0
        )

        if mission_complete:
            missions += 1

        level, title, _ = get_level_info(new_xp)

        update_data = {
            "xp": new_xp,
            "level": level,
            "missions_completed": missions,
        }

        result = (
            supabase
            .table("profiles")
            .update(update_data)
            .eq("id", st.session_state.user.id)
            .execute()
        )

        if result.data:
            st.session_state.profile = result.data[0]

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
                rgba(255, 183, 197, 0.30),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 5%,
                rgba(151, 230, 220, 0.30),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(255, 220, 150, 0.20),
                transparent 30%
            ),
            #fbfbfe;
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
                #fff8fb 0%,
                #fff5f7 45%,
                #f0fffc 100%
            );

        border-right: 1px solid #eee7ef;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    section[data-testid="stSidebar"] .stButton button {

        width: 100%;

        border: none;

        border-radius: 14px;

        padding: 0.68rem 0.8rem;

        background: transparent;

        color: #40364c;

        text-align: left;

        font-weight: 650;

        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton button:hover {

        background: #f7dfea;

        color: #b42362;

        transform: translateX(3px);
    }


    /* =====================================================
       LOGIN PAGE
    ===================================================== */

    .login-wrapper {

        max-width: 1050px;

        margin: 2.5rem auto 0 auto;
    }

    .login-brand {

        text-align: center;

        margin-bottom: 1.5rem;
    }

    .login-logo {

        font-size: 4.2rem;

        line-height: 1;

        margin-bottom: 0.6rem;
    }

    .login-title {

        font-size: 3.1rem;

        font-weight: 950;

        letter-spacing: -1px;

        background:
            linear-gradient(
                90deg,
                #e05282,
                #a855f7,
                #0ea5a4
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }

    .login-subtitle {

        color: #7b7182;

        font-size: 1.02rem;

        margin-top: 0.35rem;
    }

    .login-card {

        background: rgba(255,255,255,0.96);

        border: 1px solid #eee7ef;

        border-radius: 28px;

        padding: 2.2rem;

        box-shadow:
            0 25px 70px rgba(80,50,90,0.10);
    }


    /* =====================================================
       HERO
    ===================================================== */

    .home-hero {

        border-radius: 28px;

        padding: 2.5rem;

        color: white;

        background:
            linear-gradient(
                120deg,
                #e05282,
                #a855f7 52%,
                #14b8a6
            );

        box-shadow:
            0 18px 45px rgba(168,85,247,0.18);

        margin-bottom: 1.3rem;
    }

    .home-hero h1 {

        font-size: 2.7rem;

        font-weight: 900;

        margin-bottom: 0.4rem;
    }

    .home-hero p {

        font-size: 1.05rem;

        opacity: 0.95;
    }


    /* =====================================================
       STAT CARDS
    ===================================================== */

    .stat-card {

        background: white;

        border: 1px solid #eee9f0;

        border-radius: 21px;

        padding: 1.25rem;

        box-shadow:
            0 10px 30px rgba(70,50,90,0.07);
    }

    .stat-icon {

        font-size: 1.7rem;

        margin-bottom: 0.3rem;
    }

    .stat-number {

        font-size: 1.65rem;

        font-weight: 900;

        color: #342d3e;
    }

    .stat-label {

        color: #887e8e;

        font-size: 0.84rem;
    }


    /* =====================================================
       SECTION
    ===================================================== */

    .section-title {

        font-size: 1.9rem;

        font-weight: 900;

        color: #352c3e;

        margin-top: 2rem;

        margin-bottom: 0.2rem;
    }

    .section-subtitle {

        color: #817687;

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

        height: 245px;

        width: 100%;

        border: none !important;

        border-radius: 25px !important;

        color: white !important;

        text-align: left !important;

        white-space: pre-wrap !important;

        padding: 1.5rem !important;

        font-size: 1.05rem !important;

        font-weight: 700 !important;

        box-shadow:
            0 14px 32px rgba(60,45,80,0.13);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    div.st-key-card_drug button {
        background:
            linear-gradient(
                135deg,
                #ef6691,
                #d946ef
            ) !important;
    }

    div.st-key-card_case button {
        background:
            linear-gradient(
                135deg,
                #22b8a7,
                #3b82f6
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
                #818cf8,
                #6366f1
            ) !important;
    }

    div.st-key-card_build button {
        background:
            linear-gradient(
                135deg,
                #34d399,
                #14b8a6
            ) !important;
    }

    div.st-key-card_quiz button {
        background:
            linear-gradient(
                135deg,
                #fbbf24,
                #f97316
            ) !important;
    }

    div.st-key-card_daily button {
        background:
            linear-gradient(
                135deg,
                #fb7185,
                #e11d48
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
            0 23px 45px rgba(60,45,80,0.22);
    }


    /* =====================================================
       GAME HEADER
    ===================================================== */

    .game-header {

        background: white;

        border: 1px solid #eee9f0;

        border-radius: 25px;

        padding: 2rem;

        box-shadow:
            0 12px 32px rgba(70,50,90,0.07);

        margin-bottom: 1.5rem;
    }

    .game-header h1 {

        color: #352c3e;

        font-weight: 900;
    }

    .game-header p {

        color: #817687;
    }


    /* =====================================================
       PROGRESS
    ===================================================== */

    .progress-panel {

        margin-top: 1.4rem;

        padding: 1.5rem;

        background: white;

        border-radius: 22px;

        border: 1px solid #eee9f0;

        box-shadow:
            0 10px 30px rgba(70,50,90,0.06);
    }

    .progress-bar {

        height: 13px;

        border-radius: 20px;

        background: #eeeaf1;

        overflow: hidden;

        margin-top: 0.7rem;
    }

    .progress-fill {

        height: 100%;

        border-radius: 20px;

        background:
            linear-gradient(
                90deg,
                #e05282,
                #a855f7,
                #14b8a6
            );
    }


    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton button[kind="primary"] {

        border: none;

        border-radius: 13px;

        font-weight: 800;

        background:
            linear-gradient(
                90deg,
                #e05282,
                #a855f7
            );
    }


    /* =====================================================
       INPUTS
    ===================================================== */

    .stTextInput input,
    .stTextArea textarea {

        border-radius: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    # IMPORTANT:
    # All HTML is contained inside ONE markdown block.
    # This prevents raw HTML from appearing on screen.

    st.markdown(
        """
        <div class="login-wrapper">

            <div class="login-brand">

                <div class="login-logo">💊</div>

                <div class="login-title">
                    PharmaQuest
                </div>

                <div class="login-subtitle">
                    Learn Pharmacy • Solve Cases • Build Clinical Confidence
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        # =================================================
        # LOGIN
        # =================================================

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
                        "Supabase is not connected. "
                        "Check your Streamlit Secrets."
                    )

                else:

                    try:

                        result = (
                            supabase
                            .auth
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

                            st.success(
                                "Welcome to PharmaQuest!"
                            )

                            st.rerun()

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

        # =================================================
        # SIGNUP
        # =================================================

        else:

            st.markdown(
                "### ✨ Create your account"
            )

            st.write(
                "Create your own account and save your progress."
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

                        result = (
                            supabase
                            .auth
                            .sign_up(
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

                                st.success(
                                    "Account created successfully!"
                                )

                                st.rerun()

                            else:

                                st.success(
                                    "Account created! "
                                    "Please confirm your email, "
                                    "then return here and log in."
                                )

                        else:

                            st.error(
                                "Could not create account."
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
                    font-size:1.4rem;
                    font-weight:900;
                    color:#40364c;
                ">
                    PharmaQuest
                </div>

                <div style="
                    color:#8a7e8e;
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
                padding:14px;
                border-radius:18px;
                background:
                    linear-gradient(
                        135deg,
                        #e05282,
                        #a855f7
                    );
                color:white;
                margin-bottom:18px;
            ">

                <div style="
                    font-size:0.72rem;
                    opacity:0.85;
                ">
                    CURRENT JOURNEY
                </div>

                <div style="
                    font-size:1.05rem;
                    font-weight:800;
                    margin-top:5px;
                ">
                    {title}
                </div>

                <div style="
                    margin-top:6px;
                    font-size:0.82rem;
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
                and build your clinical confidence.
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

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ⚡
                </div>

                <div class="stat-number">
                    {xp}
                </div>

                <div class="stat-label">
                    Total XP
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🎯
                </div>

                <div class="stat-number">
                    {missions}
                </div>

                <div class="stat-label">
                    Missions Completed
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🔥
                </div>

                <div class="stat-number">
                    {profile.get("streak", 0)}
                </div>

                <div class="stat-label">
                    Day Streak
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🏆
                </div>

                <div class="stat-number">
                    {profile.get("badges", 0)}
                </div>

                <div class="stat-label">
                    Badges
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
            Investigate • Practice • Solve • Earn XP
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # ROW 1
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "🕵️\n\nDRUG DETECTIVE\n\n"
            "Investigate clues and identify mysterious medicines.\n\n"
            "+50 XP",
            key="card_drug",
            use_container_width=True
        ):

            st.session_state.page = "Drug Detective"
            st.rerun()

    with c2:

        if st.button(
            "🩺\n\nPATIENT CASE\n\n"
            "Solve fictional clinical cases and choose the best therapy.\n\n"
            "+75 XP",
            key="card_case",
            use_container_width=True
        ):

            st.session_state.page = "Patient Case"
            st.rerun()

    with c3:

        if st.button(
            "🗣️\n\nAI PATIENT\n\n"
            "Interview an AI patient and discover the clinical story.\n\n"
            "+60 XP",
            key="card_patient",
            use_container_width=True
        ):

            st.session_state.page = "AI Patient"
            st.rerun()

    with c4:

        if st.button(
            "⚔️\n\nPHARMA BATTLE\n\n"
            "Test your pharmacy knowledge in competitive challenges.\n\n"
            "+100 XP",
            key="card_battle",
            use_container_width=True
        ):

            st.session_state.page = "Pharma Battle"
            st.rerun()

    # =====================================================
    # ROW 2
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "🔐\n\nESCAPE ROOM\n\n"
            "Solve pharmacy puzzles before time runs out.\n\n"
            "+100 XP",
            key="card_escape",
            use_container_width=True
        ):

            st.session_state.page = "Escape Room"
            st.rerun()

    with c2:

        if st.button(
            "🧬\n\nBUILD THE PATIENT\n\n"
            "Construct the patient profile and treatment plan.\n\n"
            "+80 XP",
            key="card_build",
            use_container_width=True
        ):

            st.session_state.page = "Build the Patient"
            st.rerun()

    with c3:

        if st.button(
            "❓\n\nAI QUIZ\n\n"
            "Challenge yourself with AI-generated pharmacy MCQs.\n\n"
            "+40 XP",
            key="card_quiz",
            use_container_width=True
        ):

            st.session_state.page = "AI Quiz"
            st.rerun()

    with c4:

        if st.button(
            "🔥\n\nDAILY CHALLENGE\n\n"
            "Complete today's pharmacy challenge and keep your streak alive.\n\n"
            "+50 XP",
            key="card_daily",
            use_container_width=True
        ):

            st.session_state.page = "Daily Challenge"
            st.rerun()

    # =====================================================
    # LEVEL PROGRESS
    # =====================================================

    if level == 1:
        current_level_start = 0

    elif level == 2:
        current_level_start = 500

    elif level == 3:
        current_level_start = 1200

    elif level == 4:
        current_level_start = 2500

    elif level == 5:
        current_level_start = 4500

    else:
        current_level_start = 7000

    progress_range = max(
        next_xp - current_level_start,
        1
    )

    progress = min(
        max(
            (xp - current_level_start)
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
                color:#40364c;
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
                Investigate clues, think clinically,
                and identify the mysterious medicine.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Pharmacy topic",
        placeholder="Example: antibiotics, diabetes, cardiovascular drugs"
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
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.markdown(
                        "### 🔍 Mystery Case"
                    )

                    st.write(
                        response.text
                    )

                    if st.button(
                        "✅ I solved the case!",
                        type="primary"
                    ):

                        save_progress(
                            xp_add=50,
                            mission_complete=True
                        )

                        st.success(
                            "Great work! +50 XP added."
                        )

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
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
        placeholder="Example: hypertension, diabetes, asthma"
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
                Create a fictional pharmacy clinical case for a
                Pharm-D student.

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
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.markdown(
                        "### 🩺 Clinical Case"
                    )

                    st.write(
                        response.text
                    )

                    if st.button(
                        "🎯 Complete Case",
                        type="primary"
                    ):

                        save_progress(
                            xp_add=75,
                            mission_complete=True
                        )

                        st.success(
                            "Case completed! +75 XP."
                        )

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
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
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                st.markdown(
                    "### 🗣️ Patient"
                )

                st.write(
                    response.text
                )

            except Exception as e:

                st.error(
                    f"AI error: {str(e)}"
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
        placeholder="Example: pharmacology, medicinal chemistry"
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

                Clearly identify the correct answer
                after each question.

                Keep the questions educational.
                """

                try:

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.markdown(
                        "### 🧠 Your Quiz"
                    )

                    st.write(
                        response.text
                    )

                    if st.button(
                        "🏆 Complete Quiz",
                        type="primary"
                    ):

                        save_progress(
                            xp_add=40,
                            mission_complete=True
                        )

                        st.success(
                            "Quiz completed! +40 XP."
                        )

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
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

            <h1>
                {icon} {title}
            </h1>

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
        "The mission is connected to your "
        "PharmaQuest account and XP system."
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

    if level == 1:
        start = 0

    elif level == 2:
        start = 500

    elif level == 3:
        start = 1200

    elif level == 4:
        start = 2500

    elif level == 5:
        start = 4500

    else:
        start = 7000

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

    st.progress(
        progress
    )


# =========================================================
# PROFILE PAGE
# =========================================================

def profile_page():

    profile = st.session_state.profile

    level, title, _ = get_level_info(
        profile.get(
            "xp",
            0
        )
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
