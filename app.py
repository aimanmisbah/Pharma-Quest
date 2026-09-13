import streamlit as st
from google import genai
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PharmaQuest",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "user": None,
    "profile": None,
    "page": "Home",
    "login_mode": "login",

    # Drug Detective
    "drug_case": None,
    "drug_feedback": None,
    "drug_answered": False,

    # Patient Case
    "patient_case": None,
    "patient_feedback": None,
    "patient_answered": False,

    # AI Patient
    "patient_condition": None,
    "patient_history": [],

    # Quiz
    "quiz_questions": None,
    "quiz_answers": {},
    "quiz_submitted": False,
    "quiz_score": None,

    # Demo games
    "battle_answered": False,
    "escape_answered": False,
    "build_answered": False,
    "daily_answered": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SUPABASE
# ============================================================

def get_supabase():

    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

        return create_client(url, key)

    except Exception:
        return None


supabase = get_supabase()


# ============================================================
# GEMINI
# ============================================================

def get_gemini():

    try:

        api_key = st.secrets["GEMINI_API_KEY"]

        if not api_key:
            return None

        return genai.Client(api_key=api_key)

    except Exception:
        return None


# ============================================================
# GEMINI REQUEST
# ============================================================

def ask_gemini(prompt):

    client = get_gemini()

    if not client:
        raise Exception(
            "GEMINI_API_KEY is missing from Streamlit Secrets."
        )

    # Current Gemini Interactions API
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text


# ============================================================
# LEVEL SYSTEM
# ============================================================

def get_level_info(xp):

    if xp < 500:
        return 1, "Pharma Initiate", 500

    elif xp < 1200:
        return 2, "Drug Seeker", 1200

    elif xp < 2500:
        return 3, "Pharma Strategist", 2500

    elif xp < 4500:
        return 4, "Clinical Specialist", 4500

    elif xp < 7000:
        return 5, "Therapeutics Master", 7000

    else:
        return 6, "PharmaQuest Elite", 10000


# ============================================================
# LOAD PROFILE
# ============================================================

def load_profile():

    if not supabase:
        return None

    if not st.session_state.user:
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
        pass

    return None


# ============================================================
# CREATE PROFILE
# ============================================================

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


# ============================================================
# SAVE PROGRESS
# ============================================================

def save_progress(xp_add=0, mission_complete=False):

    if not supabase:
        return

    if not st.session_state.user:
        return

    profile = st.session_state.profile

    if not profile:
        return

    try:

        current_xp = profile.get("xp", 0)
        current_missions = profile.get(
            "missions_completed",
            0
        )

        new_xp = current_xp + xp_add

        if mission_complete:
            current_missions += 1

        level, _, _ = get_level_info(new_xp)

        update_data = {
            "xp": new_xp,
            "level": level,
            "missions_completed": current_missions,
        }

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

    except Exception as e:

        st.error(
            f"Could not save progress: {str(e)}"
        )


# ============================================================
# LOGOUT
# ============================================================

def logout():

    try:

        if supabase:
            supabase.auth.sign_out()

    except Exception:
        pass

    st.session_state.user = None
    st.session_state.profile = None
    st.session_state.page = "Home"
    st.session_state.login_mode = "login"

    st.rerun()


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #f5f3ff 45%,
            #ffffff 100%
        );
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


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #faf9ff 100%
        );

    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

section[data-testid="stSidebar"] .stButton {
    margin-bottom: 5px;
}

section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 43px;

    border-radius: 12px;

    background: transparent;

    border: 1px solid transparent;

    color: #334155;

    font-weight: 650;

    text-align: left;

    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #f3f0ff;

    border-color: #ddd6fe;

    color: #6d28d9;

    transform: translateX(2px);
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.sidebar-brand {
    padding: 10px 4px 14px 4px;
}

.sidebar-brand-icon {
    width: 48px;
    height: 48px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #c026d3
        );

    color: white;

    font-size: 25px;

    box-shadow:
        0 8px 20px rgba(124,58,237,0.20);

    margin-bottom: 10px;
}

.sidebar-brand-title {
    font-size: 21px;
    font-weight: 850;
    color: #1e293b;
}

.sidebar-brand-subtitle {
    font-size: 12px;
    color: #64748b;
    margin-top: 2px;
}


/* ============================================================
   USER PANEL
   ============================================================ */

.user-panel {
    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 16px;

    padding: 14px;

    margin-bottom: 12px;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.04);
}

.user-name {
    font-size: 15px;
    font-weight: 800;
    color: #1e293b;
}

.user-rank {
    font-size: 12px;
    color: #64748b;
    margin-top: 3px;
}


/* ============================================================
   LOGIN
   ============================================================ */

.login-card {
    background: #ffffff;

    border: 1px solid #e5e7eb;

    border-radius: 24px;

    padding: 2.2rem;

    box-shadow:
        0 20px 55px rgba(15,23,42,0.08);
}

.login-brand {
    text-align: center;
    margin-bottom: 20px;
}

.login-icon {
    width: 70px;
    height: 70px;

    margin: 0 auto 15px auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #c026d3
        );

    font-size: 34px;

    box-shadow:
        0 12px 30px rgba(124,58,237,0.22);
}

.login-title {
    font-size: 30px;
    font-weight: 850;
    color: #1e293b;
}

.login-subtitle {
    color: #64748b;
    font-size: 14px;
    margin-top: 5px;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {
    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #5b21b6,
            #7c3aed 45%,
            #c026d3
        );

    padding: 2.6rem;

    border-radius: 26px;

    color: white;

    box-shadow:
        0 22px 50px rgba(91,33,182,0.20);

    margin-bottom: 1.5rem;
}

.hero-box::after {
    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    right: -70px;
    top: -90px;

    border-radius: 50%;

    background: rgba(255,255,255,0.10);
}

.hero-box h1 {
    position: relative;
    z-index: 2;

    font-size: 2.2rem;
    font-weight: 850;

    margin-bottom: 8px;
}

.hero-box p {
    position: relative;
    z-index: 2;

    font-size: 1rem;

    opacity: 0.94;

    max-width: 760px;
}


/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-box {
    background: #ffffff;

    border: 1px solid #e5e7eb;

    border-radius: 18px;

    padding: 1.25rem;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    min-height: 115px;

    transition: all 0.2s ease;
}

.stat-box:hover {
    transform: translateY(-3px);

    box-shadow:
        0 15px 35px rgba(15,23,42,0.08);
}

.stat-icon {
    font-size: 22px;
    margin-bottom: 6px;
}

.stat-label {
    color: #64748b;

    font-size: 0.76rem;

    font-weight: 750;

    text-transform: uppercase;

    letter-spacing: 0.05em;
}

.stat-value {
    color: #1e293b;

    font-size: 1.75rem;

    font-weight: 850;

    margin-top: 4px;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-heading {
    font-size: 1.65rem;

    font-weight: 850;

    color: #1e293b;

    margin-top: 2rem;

    margin-bottom: 4px;
}

.section-description {
    color: #64748b;

    margin-bottom: 1.2rem;
}


/* ============================================================
   GAME CARDS
   ============================================================ */

.game-card {
    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 20px;

    padding: 1.35rem;

    min-height: 245px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.045);

    transition: all 0.22s ease;
}

.game-card:hover {
    transform: translateY(-5px);

    border-color: #c4b5fd;

    box-shadow:
        0 18px 38px rgba(91,33,182,0.11);
}

.game-icon {
    width: 52px;
    height: 52px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 15px;

    background: #f3f0ff;

    border: 1px solid #ddd6fe;

    font-size: 25px;

    margin-bottom: 15px;
}

.game-title {
    font-size: 1.18rem;

    font-weight: 850;

    color: #1e293b;

    margin-bottom: 7px;
}

.game-description {
    color: #64748b;

    font-size: 0.91rem;

    line-height: 1.55;

    min-height: 64px;
}

.game-reward {
    color: #7c3aed;

    font-size: 0.82rem;

    font-weight: 750;

    margin-top: 12px;

    margin-bottom: 10px;
}


/* ============================================================
   GAME HEADER
   ============================================================ */

.game-title-box {
    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 22px;

    padding: 2rem;

    box-shadow:
        0 10px 30px rgba(15,23,42,0.05);

    margin-bottom: 1.5rem;
}

.game-title-icon {
    width: 58px;
    height: 58px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            #f3f0ff,
            #fae8ff
        );

    border: 1px solid #ddd6fe;

    font-size: 28px;

    margin-bottom: 14px;
}

.game-title-box h1 {
    color: #1e293b;

    font-size: 2rem;

    font-weight: 850;

    margin-bottom: 6px;
}

.game-title-box p {
    color: #64748b;

    font-size: 0.98rem;
}


/* ============================================================
   MISSION BOX
   ============================================================ */

.mission-box {
    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 20px;

    padding: 1.5rem;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.045);

    margin-bottom: 1.2rem;
}

.mission-label {
    color: #7c3aed;

    font-size: 0.75rem;

    font-weight: 800;

    letter-spacing: 0.08em;

    text-transform: uppercase;

    margin-bottom: 7px;
}

.mission-question {
    color: #1e293b;

    font-size: 1.1rem;

    font-weight: 750;

    line-height: 1.55;
}


/* ============================================================
   FEEDBACK
   ============================================================ */

.feedback-good {
    background: #ecfdf5;

    border: 1px solid #a7f3d0;

    color: #065f46;

    border-radius: 16px;

    padding: 1rem 1.2rem;

    margin-top: 1rem;
}

.feedback-bad {
    background: #fff7ed;

    border: 1px solid #fed7aa;

    color: #9a3412;

    border-radius: 16px;

    padding: 1rem 1.2rem;

    margin-top: 1rem;
}


/* ============================================================
   PROGRESS
   ============================================================ */

.progress-box {
    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 1.4rem;

    margin-top: 1.5rem;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.04);
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input,
.stTextArea textarea {
    border-radius: 11px !important;

    border: 1px solid #cbd5e1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #8b5cf6 !important;

    box-shadow:
        0 0 0 2px rgba(139,92,246,0.12) !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton button {
    border-radius: 11px;

    min-height: 42px;

    font-weight: 750;

    transition: all 0.18s ease;
}

.stButton button:hover {
    transform: translateY(-1px);
}


/* PRIMARY */

.stButton button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #a855f7
        );

    border: none;

    color: white;
}

.stButton button[kind="primary"]:hover {
    background:
        linear-gradient(
            135deg,
            #6d28d9,
            #9333ea
        );

    color: white;
}


/* ============================================================
   ANSWER AREA
   ============================================================ */

.answer-box {
    background: #faf9ff;

    border: 1px solid #ddd6fe;

    border-radius: 18px;

    padding: 1.2rem;

    margin-top: 1rem;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 800px) {

    .hero-box {
        padding: 1.6rem;
    }

    .hero-box h1 {
        font-size: 1.7rem;
    }

    .game-title-box {
        padding: 1.4rem;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    left, center, right = st.columns([1, 1.25, 1])

    with center:

        st.markdown(
            """
            <div class="login-brand">
                <div class="login-icon">💊</div>
                <div class="login-title">PharmaQuest</div>
                <div class="login-subtitle">
                    Learn Pharmacy • Solve Cases • Build Clinical Confidence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):

            if st.session_state.login_mode == "login":

                st.subheader("Welcome back")

                st.caption(
                    "Sign in to continue your pharmacy learning journey."
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
                    "Sign in to PharmaQuest",
                    type="primary",
                    use_container_width=True
                ):

                    if not email or not password:

                        st.error(
                            "Please enter your email and password."
                        )

                    elif not supabase:

                        st.error(
                            "Supabase is not connected. Check your Streamlit Secrets."
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

                                st.rerun()

                            else:

                                st.error(
                                    "Login failed."
                                )

                        except Exception as e:

                            st.error(
                                f"Login failed: {str(e)}"
                            )

                st.divider()

                st.write(
                    "Don't have an account?"
                )

                if st.button(
                    "Create a new account",
                    use_container_width=True
                ):

                    st.session_state.login_mode = "signup"

                    st.rerun()

            else:

                st.subheader("Create your account")

                st.caption(
                    "Create your own profile and save your learning progress."
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
                    "Create my account",
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
                                        "Account created. "
                                        "Please confirm your email and then log in."
                                    )

                            else:

                                st.error(
                                    "Could not create the account."
                                )

                        except Exception as e:

                            st.error(
                                f"Signup failed: {str(e)}"
                            )

                st.divider()

                if st.button(
                    "← Back to login",
                    use_container_width=True
                ):

                    st.session_state.login_mode = "login"

                    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

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

        # IMPORTANT:
        # This HTML is inside st.markdown and unsafe_allow_html=True.
        # Therefore it will render as HTML instead of appearing as code.

        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon">💊</div>
                <div class="sidebar-brand-title">PharmaQuest</div>
                <div class="sidebar-brand-subtitle">
                    Pharmacy Learning Arena
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="user-panel">
                <div class="user-name">👋 {username}</div>
                <div class="user-rank">
                    {title} • Level {level}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            f"{xp} XP"
        )

        st.progress(
            min((xp % 500) / 500, 1)
        )

        st.divider()

        st.caption("MAIN")

        if st.button(
            "⌂   Home Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "Home"
            st.rerun()

        if st.button(
            "◈   My Progress",
            use_container_width=True
        ):

            st.session_state.page = "Progress"
            st.rerun()

        st.divider()

        st.caption("PLAY & PRACTICE")

        games = [
            ("⌕   Drug Detective", "Drug Detective"),
            ("✚   Patient Case", "Patient Case"),
            ("◉   AI Patient", "AI Patient"),
            ("⚔   Pharma Battle", "Pharma Battle"),
            ("▣   Escape Room", "Escape Room"),
            ("◈   Build the Patient", "Build the Patient"),
        ]

        for label, page in games:

            if st.button(
                label,
                use_container_width=True,
                key=f"side_{page}"
            ):

                st.session_state.page = page
                st.rerun()

        st.divider()

        st.caption("LEARN")

        if st.button(
            "✦   AI Quiz",
            use_container_width=True
        ):

            st.session_state.page = "AI Quiz"
            st.rerun()

        if st.button(
            "🔥   Daily Challenge",
            use_container_width=True
        ):

            st.session_state.page = "Daily Challenge"
            st.rerun()

        st.divider()

        st.caption("ACCOUNT")

        if st.button(
            "♛   My Profile",
            use_container_width=True
        ):

            st.session_state.page = "Profile"
            st.rerun()

        if st.button(
            "↪   Logout",
            use_container_width=True
        ):

            logout()


# ============================================================
# GAME CARD
# ============================================================

def game_card(
    icon,
    title,
    description,
    xp,
    page
):

    st.markdown(
        f"""
        <div class="game-card">

            <div class="game-icon">
                {icon}
            </div>

            <div class="game-title">
                {title}
            </div>

            <div class="game-description">
                {description}
            </div>

            <div class="game-reward">
                ✦ +{xp} XP
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Open mission  →",
        key=f"open_{page}",
        use_container_width=True
    ):

        st.session_state.page = page
        st.rerun()


# ============================================================
# HOME DASHBOARD
# ============================================================

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

    streak = profile.get(
        "streak",
        0
    )

    badges = profile.get(
        "badges",
        0
    )

    level, title, next_xp = get_level_info(xp)

    # HERO

    st.markdown(
        f"""
        <div class="hero-box">

            <h1>Welcome back, {username}</h1>

            <p>
                Build your pharmacy knowledge through
                clinical cases, investigations and
                interactive challenges.
            </p>

            <p>
                <strong>{title}</strong>
                &nbsp; • &nbsp;
                Level {level}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # STATS

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-icon">✦</div>
                <div class="stat-label">Total XP</div>
                <div class="stat-value">{xp}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-icon">✓</div>
                <div class="stat-label">Missions</div>
                <div class="stat-value">{missions}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-icon">🔥</div>
                <div class="stat-label">Streak</div>
                <div class="stat-value">{streak}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-icon">♛</div>
                <div class="stat-label">Badges</div>
                <div class="stat-value">{badges}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # MISSIONS

    st.markdown(
        '<div class="section-heading">Choose your mission</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Practice pharmacy knowledge through focused clinical challenges.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        game_card(
            "⌕",
            "Drug Detective",
            "Investigate clinical clues and identify the mystery medicine.",
            50,
            "Drug Detective"
        )

    with c2:

        game_card(
            "✚",
            "Patient Case",
            "Analyze a fictional patient and make a therapeutic decision.",
            75,
            "Patient Case"
        )

    with c3:

        game_card(
            "◉",
            "AI Patient",
            "Interview a simulated patient and practice clinical questioning.",
            60,
            "AI Patient"
        )

    c1, c2, c3 = st.columns(3)

    with c1:

        game_card(
            "⚔",
            "Pharma Battle",
            "Challenge your pharmacology and therapeutics knowledge.",
            100,
            "Pharma Battle"
        )

    with c2:

        game_card(
            "▣",
            "Escape Room",
            "Solve pharmacy puzzles and unlock the next stage.",
            100,
            "Escape Room"
        )

    with c3:

        game_card(
            "◈",
            "Build the Patient",
            "Construct a patient profile and develop a treatment strategy.",
            80,
            "Build the Patient"
        )

    c1, c2 = st.columns(2)

    with c1:

        game_card(
            "✦",
            "AI Quiz",
            "Generate pharmacy MCQs, answer them and receive corrections.",
            40,
            "AI Quiz"
        )

    with c2:

        game_card(
            "🔥",
            "Daily Challenge",
            "Complete today's pharmacy challenge and maintain your streak.",
            50,
            "Daily Challenge"
        )

    # PROGRESS

    current_start = {
        1: 0,
        2: 500,
        3: 1200,
        4: 2500,
        5: 4500,
        6: 7000
    }.get(level, 0)

    progress_range = max(
        next_xp - current_start,
        1
    )

    progress = (
        xp - current_start
    ) / progress_range

    progress = max(
        0,
        min(progress, 1)
    )

    st.markdown(
        '<div class="progress-box">',
        unsafe_allow_html=True
    )

    st.subheader(
        f"Level {level} — {title}"
    )

    st.progress(progress)

    st.caption(
        f"{xp} / {next_xp} XP toward the next level"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# GAME HEADER
# ============================================================

def game_header(
    icon,
    title,
    description
):

    st.markdown(
        f"""
        <div class="game-title-box">

            <div class="game-title-icon">
                {icon}
            </div>

            <h1>{title}</h1>

            <p>{description}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DRUG DETECTIVE
# ============================================================

def drug_detective():

    game_header(
        "⌕",
        "Drug Detective",
        "Investigate the clues, identify the medicine and receive feedback on your reasoning."
    )

    if not st.session_state.drug_case:

        topic = st.text_input(
            "What pharmacy topic should we investigate?",
            placeholder="Example: antibiotics, diabetes, hypertension"
        )

        if st.button(
            "Start investigation",
            type="primary"
        ):

            if not topic:

                st.warning(
                    "Enter a topic first."
                )

            else:

                prompt = f"""
You are designing a pharmacy educational mystery.

Topic:
{topic}

Create ONE fictional Drug Detective case for a Pharm-D student.

Give:
- Patient situation
- Three clinical clues
- One mechanism-of-action clue
- One adverse-effect clue
- One important patient clue
- A clear question asking which medicine is most likely.

Do NOT reveal the medicine name in the case.

Do not give the answer.

Keep it educational and concise.
"""

                try:

                    with st.spinner(
                        "Creating your investigation..."
                    ):

                        result = ask_gemini(prompt)

                    st.session_state.drug_case = result
                    st.session_state.drug_feedback = None
                    st.session_state.drug_answered = False

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    else:

        st.markdown(
            '<div class="mission-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="mission-label">Case file</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.drug_case
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        if not st.session_state.drug_answered:

            answer = st.text_input(
                "Your diagnosis / medicine answer",
                placeholder="Type the medicine you think is correct...",
                key="drug_student_answer"
            )

            reasoning = st.text_area(
                "Why do you think this is the answer?",
                placeholder="Briefly explain your reasoning...",
                key="drug_reasoning"
            )

            if st.button(
                "Check my answer",
                type="primary"
            ):

                if not answer:

                    st.warning(
                        "Enter your answer first."
                    )

                else:

                    prompt = f"""
You are a pharmacy professor.

Below is a Drug Detective educational case:

CASE:
{st.session_state.drug_case}

STUDENT ANSWER:
{answer}

STUDENT REASONING:
{reasoning}

Evaluate the student's answer.

Your response must include:

1. Correct / Partially Correct / Incorrect
2. Correct medicine
3. Why the answer is correct or incorrect
4. Which clinical clues support the correct answer
5. One short learning point

Be encouraging and educational.

Do not give unsafe personal medical advice.
"""

                    try:

                        with st.spinner(
                            "Checking your reasoning..."
                        ):

                            feedback = ask_gemini(prompt)

                        st.session_state.drug_feedback = feedback
                        st.session_state.drug_answered = True

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"AI error: {str(e)}"
                        )

        else:

            st.subheader(
                "Professor feedback"
            )

            st.markdown(
                st.session_state.drug_feedback
            )

            st.success(
                "Investigation completed."
            )

            if st.button(
                "Claim +50 XP",
                type="primary"
            ):

                save_progress(
                    xp_add=50,
                    mission_complete=True
                )

                st.session_state.drug_case = None
                st.session_state.drug_feedback = None
                st.session_state.drug_answered = False

                st.success(
                    "+50 XP added to your profile."
                )

                st.rerun()

            if st.button(
                "New investigation"
            ):

                st.session_state.drug_case = None
                st.session_state.drug_feedback = None
                st.session_state.drug_answered = False

                st.rerun()


# ============================================================
# PATIENT CASE
# ============================================================

def patient_case():

    game_header(
        "✚",
        "Patient Case",
        "Analyze a fictional patient, make a therapeutic decision and receive clinical feedback."
    )

    if not st.session_state.patient_case:

        topic = st.text_input(
            "Clinical topic",
            placeholder="Example: asthma, hypertension, diabetes"
        )

        if st.button(
            "Generate clinical case",
            type="primary"
        ):

            if not topic:

                st.warning(
                    "Enter a clinical topic first."
                )

            else:

                prompt = f"""
Create a fictional pharmacy clinical case for a Pharm-D student.

Topic:
{topic}

Include:
- age
- sex
- chief complaint
- medical history
- current medicines
- relevant vital signs or laboratory information
- important clinical clues
- three possible therapeutic approaches

Then ask:
"What would you recommend and why?"

Do NOT reveal the correct answer.

Do not give real-person medical advice.
"""

                try:

                    with st.spinner(
                        "Creating clinical case..."
                    ):

                        result = ask_gemini(prompt)

                    st.session_state.patient_case = result
                    st.session_state.patient_feedback = None
                    st.session_state.patient_answered = False

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    else:

        st.markdown(
            '<div class="mission-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="mission-label">Clinical briefing</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.patient_case
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        if not st.session_state.patient_answered:

            decision = st.text_area(
                "Your therapeutic decision",
                placeholder=(
                    "What would you recommend for this fictional patient "
                    "and why?"
                ),
                height=140
            )

            if st.button(
                "Submit clinical decision",
                type="primary"
            ):

                if not decision:

                    st.warning(
                        "Write your clinical decision first."
                    )

                else:

                    prompt = f"""
You are evaluating a Pharm-D student's clinical reasoning.

CASE:
{st.session_state.patient_case}

STUDENT DECISION:
{decision}

Evaluate the decision educationally.

Give:

1. Overall assessment
2. What the student did well
3. What needs improvement
4. A more appropriate therapeutic approach
5. Important safety considerations
6. One key learning point

Use educational language.

This is a fictional educational case.
Do not give personalized medical advice.
"""

                    try:

                        with st.spinner(
                            "Evaluating your clinical reasoning..."
                        ):

                            feedback = ask_gemini(prompt)

                        st.session_state.patient_feedback = feedback
                        st.session_state.patient_answered = True

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"AI error: {str(e)}"
                        )

        else:

            st.subheader(
                "Clinical feedback"
            )

            st.markdown(
                st.session_state.patient_feedback
            )

            if st.button(
                "Claim +75 XP",
                type="primary"
            ):

                save_progress(
                    xp_add=75,
                    mission_complete=True
                )

                st.session_state.patient_case = None
                st.session_state.patient_feedback = None
                st.session_state.patient_answered = False

                st.success(
                    "+75 XP added."
                )

                st.rerun()

            if st.button(
                "Start another case"
            ):

                st.session_state.patient_case = None
                st.session_state.patient_feedback = None
                st.session_state.patient_answered = False

                st.rerun()


# ============================================================
# AI PATIENT
# ============================================================

def ai_patient():

    game_header(
        "◉",
        "AI Patient",
        "Interview a simulated patient and practice asking useful clinical questions."
    )

    if not st.session_state.patient_condition:

        condition = st.text_input(
            "Patient condition",
            placeholder="Example: type 2 diabetes"
        )

        if st.button(
            "Begin patient interview",
            type="primary"
        ):

            if not condition:

                st.warning(
                    "Enter a condition first."
                )

            else:

                st.session_state.patient_condition = condition
                st.session_state.patient_history = []

                st.rerun()

    else:

        st.info(
            f"Simulated patient condition: "
            f"{st.session_state.patient_condition}"
        )

        # Conversation history

        for message in st.session_state.patient_history:

            if message["role"] == "student":

                with st.chat_message("user"):
                    st.write(message["text"])

            else:

                with st.chat_message("assistant"):
                    st.write(message["text"])

        question = st.text_input(
            "Ask the patient",
            placeholder="Example: When did your symptoms start?",
            key=f"patient_question_{len(st.session_state.patient_history)}"
        )

        if st.button(
            "Ask patient",
            type="primary"
        ):

            if not question:

                st.warning(
                    "Ask a question first."
                )

            else:

                conversation = "\n".join(
                    [
                        f"{m['role']}: {m['text']}"
                        for m in st.session_state.patient_history
                    ]
                )

                prompt = f"""
Act as a fictional pharmacy patient.

Condition:
{st.session_state.patient_condition}

Conversation so far:
{conversation}

Student's latest question:
{question}

Answer ONLY as the patient.

Rules:
- Speak naturally.
- Do not act as a doctor.
- Do not diagnose the student.
- Do not give a definitive treatment plan.
- Give realistic patient information.
- If the student asks something the patient would not know, say so.
"""

                try:

                    with st.spinner(
                        "Patient is responding..."
                    ):

                        response = ask_gemini(prompt)

                    st.session_state.patient_history.append(
                        {
                            "role": "student",
                            "text": question
                        }
                    )

                    st.session_state.patient_history.append(
                        {
                            "role": "patient",
                            "text": response
                        }
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

        st.divider()

        if st.button(
            "End interview & get feedback"
        ):

            conversation = "\n".join(
                [
                    f"{m['role']}: {m['text']}"
                    for m in st.session_state.patient_history
                ]
            )

            prompt = f"""
You are a pharmacy communication professor.

Review this simulated patient interview:

{conversation}

Give:
1. What the student did well
2. Important questions they asked
3. Important questions they missed
4. How they could improve patient communication
5. A short clinical interviewing score out of 10

Keep it educational.
"""

            try:

                feedback = ask_gemini(prompt)

                st.subheader(
                    "Interview feedback"
                )

                st.markdown(
                    feedback
                )

                if st.button(
                    "Claim +60 XP",
                    type="primary"
                ):

                    save_progress(
                        xp_add=60,
                        mission_complete=True
                    )

                    st.session_state.patient_condition = None
                    st.session_state.patient_history = []

                    st.success(
                        "+60 XP added."
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    f"AI error: {str(e)}"
                )


# ============================================================
# AI QUIZ
# ============================================================

def ai_quiz():

    game_header(
        "✦",
        "AI Quiz",
        "Answer pharmacy MCQs and receive your score, corrections and explanations."
    )

    if not st.session_state.quiz_questions:

        topic = st.text_input(
            "Quiz topic",
            placeholder="Example: pharmacology, antibiotics, medicinal chemistry"
        )

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        if st.button(
            "Generate quiz",
            type="primary"
        ):

            if not topic:

                st.warning(
                    "Enter a topic first."
                )

            else:

                prompt = f"""
Create exactly 5 pharmacy MCQs for a Pharm-D student.

Topic:
{topic}

Difficulty:
{difficulty}

For EACH question return this exact structure:

QUESTION 1:
Question text

A) option
B) option
C) option
D) option

CORRECT: A

EXPLANATION:
short explanation

Then repeat for questions 2 to 5.

Do not add any other text.
"""

                try:

                    with st.spinner(
                        "Building your quiz..."
                    ):

                        raw = ask_gemini(prompt)

                    questions = parse_quiz(raw)

                    if len(questions) < 5:

                        st.error(
                            "The AI did not return a complete quiz. Please generate again."
                        )

                    else:

                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = None

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    else:

        questions = st.session_state.quiz_questions

        if not st.session_state.quiz_submitted:

            for i, q in enumerate(questions):

                st.markdown(
                    f"""
                    <div class="mission-box">
                        <div class="mission-label">
                            Question {i + 1}
                        </div>
                        <div class="mission-question">
                            {q["question"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                answer = st.radio(
                    "Choose one answer:",
                    [
                        f"A) {q['A']}",
                        f"B) {q['B']}",
                        f"C) {q['C']}",
                        f"D) {q['D']}",
                    ],
                    key=f"quiz_{i}",
                    index=None
                )

                if answer:

                    st.session_state.quiz_answers[i] = answer[0]

            st.write("")

            if st.button(
                "Submit quiz",
                type="primary"
            ):

                if len(
                    st.session_state.quiz_answers
                ) < len(questions):

                    st.warning(
                        "Please answer all five questions."
                    )

                else:

                    score = 0

                    for i, q in enumerate(questions):

                        if (
                            st.session_state.quiz_answers[i]
                            == q["correct"]
                        ):

                            score += 1

                    st.session_state.quiz_score = score
                    st.session_state.quiz_submitted = True

                    st.rerun()

        else:

            score = st.session_state.quiz_score

            st.subheader(
                f"Your score: {score} / {len(questions)}"
            )

            if score == 5:

                st.success(
                    "Excellent! Perfect score."
                )

            elif score >= 3:

                st.info(
                    "Good work. Review the explanations below."
                )

            else:

                st.warning(
                    "Keep practicing. Review each correction carefully."
                )

            for i, q in enumerate(questions):

                selected = st.session_state.quiz_answers[i]
                correct = q["correct"]

                st.markdown(
                    f"### Question {i + 1}"
                )

                st.write(
                    q["question"]
                )

                st.write(
                    f"**Your answer:** {selected}"
                )

                st.write(
                    f"**Correct answer:** {correct}"
                )

                st.info(
                    q["explanation"]
                )

                st.divider()

            if st.button(
                "Claim +40 XP",
                type="primary"
            ):

                save_progress(
                    xp_add=40,
                    mission_complete=True
                )

                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = None

                st.success(
                    "+40 XP added."
                )

                st.rerun()

            if st.button(
                "Generate another quiz"
            ):

                st.session_state.quiz_questions = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = None

                st.rerun()


# ============================================================
# QUIZ PARSER
# ============================================================

def parse_quiz(text):

    questions = []

    blocks = text.split("QUESTION ")

    for block in blocks:

        if not block.strip():
            continue

        try:

            question_part = block.split(
                "A)"
            )[0]

            question = question_part.split(
                ":",
                1
            )[1].strip()

            a_part = block.split("A)", 1)[1]
            a = a_part.split("B)", 1)[0].strip()

            b_part = block.split("B)", 1)[1]
            b = b_part.split("C)", 1)[0].strip()

            c_part = block.split("C)", 1)[1]
            c = c_part.split("D)", 1)[0].strip()

            d_part = block.split("D)", 1)[1]

            d = d_part.split(
                "CORRECT:",
                1
            )[0].strip()

            correct = (
                block.split(
                    "CORRECT:",
                    1
                )[1]
                .split(
                    "EXPLANATION:",
                    1
                )[0]
                .strip()
                .upper()[0]
            )

            explanation = block.split(
                "EXPLANATION:",
                1
            )[1].strip()

            questions.append(
                {
                    "question": question,
                    "A": a,
                    "B": b,
                    "C": c,
                    "D": d,
                    "correct": correct,
                    "explanation": explanation,
                }
            )

        except Exception:
            continue

    return questions


# ============================================================
# PHARMA BATTLE
# ============================================================

def pharma_battle():

    game_header(
        "⚔",
        "Pharma Battle",
        "Challenge your pharmacology knowledge with a rapid clinical question."
    )

    st.markdown(
        """
        <div class="mission-box">
            <div class="mission-label">Battle round</div>
            <div class="mission-question">
                Which class of drugs is commonly used as first-line
                maintenance therapy for many patients with hypertension?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "Choose your answer:",
        [
            "A) Antihypertensive therapy",
            "B) Antibiotics",
            "C) Antifungals",
            "D) Antivirals"
        ],
        index=None,
        key="battle_choice"
    )

    if not st.session_state.battle_answered:

        if st.button(
            "Submit battle answer",
            type="primary"
        ):

            if not answer:

                st.warning(
                    "Choose an answer."
                )

            elif answer.startswith("A)"):

                st.success(
                    "Correct! In this simplified educational question, antihypertensive therapy is the appropriate category."
                )

                st.session_state.battle_answered = True

            else:

                st.error(
                    "Not quite. Review the question and think about treatment of high blood pressure."
                )

                st.session_state.battle_answered = True

    else:

        if st.button(
            "Claim +100 XP",
            type="primary"
        ):

            save_progress(
                xp_add=100,
                mission_complete=True
            )

            st.session_state.battle_answered = False

            st.success(
                "+100 XP added."
            )

            st.rerun()


# ============================================================
# ESCAPE ROOM
# ============================================================

def escape_room():

    game_header(
        "▣",
        "Escape Room",
        "Solve pharmacy puzzles and unlock the next stage."
    )

    st.markdown(
        """
        <div class="mission-box">
            <div class="mission-label">Puzzle 01</div>
            <div class="mission-question">
                A medicine has a very narrow therapeutic index.
                What does this generally mean?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "Choose the best answer:",
        [
            "A) It is always completely harmless",
            "B) The effective and toxic concentrations are relatively close",
            "C) It cannot cause adverse effects",
            "D) It does not require monitoring"
        ],
        index=None,
        key="escape_choice"
    )

    if not st.session_state.escape_answered:

        if st.button(
            "Unlock the door",
            type="primary"
        ):

            if not answer:

                st.warning(
                    "Choose an answer."
                )

            elif answer.startswith("B)"):

                st.success(
                    "Correct. The therapeutic and toxic concentrations are relatively close."
                )

                st.session_state.escape_answered = True

            else:

                st.error(
                    "Incorrect. Think about how close effective and toxic concentrations are."
                )

                st.session_state.escape_answered = True

    else:

        if st.button(
            "Claim +100 XP",
            type="primary"
        ):

            save_progress(
                xp_add=100,
                mission_complete=True
            )

            st.session_state.escape_answered = False

            st.success(
                "+100 XP added."
            )

            st.rerun()


# ============================================================
# BUILD THE PATIENT
# ============================================================

def build_patient():

    game_header(
        "◈",
        "Build the Patient",
        "Construct a fictional patient profile and choose the most important information to investigate."
    )

    age = st.number_input(
        "Patient age",
        min_value=1,
        max_value=100,
        value=45
    )

    symptoms = st.multiselect(
        "Select important symptoms",
        [
            "Fatigue",
            "Shortness of breath",
            "Increased thirst",
            "Frequent urination",
            "Chest discomfort",
            "Headache"
        ]
    )

    medications = st.multiselect(
        "Current medicines",
        [
            "Metformin",
            "Amlodipine",
            "Atorvastatin",
            "Salbutamol",
            "Warfarin",
            "No current medicines"
        ]
    )

    if not st.session_state.build_answered:

        if st.button(
            "Evaluate patient profile",
            type="primary"
        ):

            if not symptoms:

                st.warning(
                    "Select at least one symptom."
                )

            else:

                st.session_state.build_answered = True

                st.success(
                    "Patient profile created successfully."
                )

                st.info(
                    "Next clinical step: review the patient's symptoms, "
                    "history, medicines and relevant investigations before "
                    "making a treatment decision."
                )

    else:

        st.subheader(
            "Patient profile"
        )

        st.write(
            f"**Age:** {age}"
        )

        st.write(
            f"**Symptoms:** {', '.join(symptoms)}"
        )

        st.write(
            f"**Medicines:** {', '.join(medications)}"
        )

        if st.button(
            "Claim +80 XP",
            type="primary"
        ):

            save_progress(
                xp_add=80,
                mission_complete=True
            )

            st.session_state.build_answered = False

            st.success(
                "+80 XP added."
            )

            st.rerun()


# ============================================================
# DAILY CHALLENGE
# ============================================================

def daily_challenge():

    game_header(
        "🔥",
        "Daily Challenge",
        "Complete one focused pharmacy challenge and keep your learning momentum going."
    )

    st.markdown(
        """
        <div class="mission-box">
            <div class="mission-label">Today's challenge</div>
            <div class="mission-question">
                A patient taking an oral medicine reports that they
                regularly forget doses. What is the most appropriate
                first step for a pharmacist?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "Choose the best approach:",
        [
            "A) Immediately double every future dose",
            "B) Explore the reason for missed doses and discuss adherence strategies",
            "C) Tell the patient to stop the medicine",
            "D) Ignore the issue"
        ],
        index=None,
        key="daily_choice"
    )

    if not st.session_state.daily_answered:

        if st.button(
            "Submit challenge",
            type="primary"
        ):

            if not answer:

                st.warning(
                    "Choose an answer."
                )

            elif answer.startswith("B)"):

                st.success(
                    "Correct. Exploring the reason for missed doses is an important first step."
                )

                st.session_state.daily_answered = True

            else:

                st.error(
                    "Not quite. Think about identifying the cause of non-adherence first."
                )

                st.session_state.daily_answered = True

    else:

        if st.button(
            "Claim +50 XP",
            type="primary"
        ):

            save_progress(
                xp_add=50,
                mission_complete=True
            )

            st.session_state.daily_answered = False

            st.success(
                "+50 XP added."
            )

            st.rerun()


# ============================================================
# PROGRESS PAGE
# ============================================================

def progress_page():

    profile = st.session_state.profile

    xp = profile.get(
        "xp",
        0
    )

    missions = profile.get(
        "missions_completed",
        0
    )

    level, title, next_xp = get_level_info(xp)

    game_header(
        "◈",
        "My Progress",
        "Track your development across the PharmaQuest learning arena."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Current level",
            level
        )

    with c2:

        st.metric(
            "Total XP",
            xp
        )

    with c3:

        st.metric(
            "Missions completed",
            missions
        )

    st.divider()

    st.subheader(
        title
    )

    current_start = {
        1: 0,
        2: 500,
        3: 1200,
        4: 2500,
        5: 4500,
        6: 7000
    }.get(
        level,
        0
    )

    progress_range = max(
        next_xp - current_start,
        1
    )

    progress = (
        xp - current_start
    ) / progress_range

    progress = max(
        0,
        min(progress, 1)
    )

    st.progress(progress)

    st.caption(
        f"{xp} / {next_xp} XP"
    )


# ============================================================
# PROFILE PAGE
# ============================================================

def profile_page():

    profile = st.session_state.profile

    username = profile.get(
        "username",
        "Student"
    )

    xp = profile.get(
        "xp",
        0
    )

    level, title, _ = get_level_info(xp)

    game_header(
        "♛",
        "My Profile",
        "Your personal PharmaQuest learning identity."
    )

    st.subheader(
        username
    )

    st.caption(
        "PharmaQuest learner"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            f"**Rank:** {title}"
        )

        st.write(
            f"**Level:** {level}"
        )

        st.write(
            f"**XP:** {xp}"
        )

    with c2:

        st.write(
            f"**Missions:** "
            f"{profile.get('missions_completed', 0)}"
        )

        st.write(
            f"**Badges:** "
            f"{profile.get('badges', 0)}"
        )

        st.write(
            f"**Streak:** "
            f"{profile.get('streak', 0)} days"
        )


# ============================================================
# MAIN APP
# ============================================================

if not st.session_state.user:

    login_page()

else:

    if not st.session_state.profile:

        st.session_state.profile = load_profile()

    if not st.session_state.profile:

        st.error(
            "Your student profile could not be loaded."
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

        pharma_battle()

    elif page == "Escape Room":

        escape_room()

    elif page == "Build the Patient":

        build_patient()

    elif page == "Daily Challenge":

        daily_challenge()
