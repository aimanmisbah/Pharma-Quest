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
    "drug_result": None,
    "case_result": None,
    "patient_result": None,
    "quiz_result": None,
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

    /* =====================================================
       GENERAL
       ===================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #f5f3ff 50%,
                #fff7ed 100%
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


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid transparent;
        background: transparent;
        color: #334155;
        font-weight: 600;
        text-align: left;
        min-height: 42px;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #f3f0ff;
        border-color: #ddd6fe;
        color: #6d28d9;
    }


    /* =====================================================
       LOGIN
       ===================================================== */

    .login-spacer {
        height: 70px;
    }


    /* =====================================================
       HOME HERO
       ===================================================== */

    .hero-box {
        background:
            linear-gradient(
                135deg,
                #6d28d9,
                #9333ea 45%,
                #db2777
            );

        padding: 2.4rem;
        border-radius: 24px;
        color: white;
        box-shadow:
            0 20px 50px rgba(109, 40, 217, 0.20);

        margin-bottom: 1.5rem;
    }


    /* =====================================================
       STAT CARDS
       ===================================================== */

    .stat-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1.25rem;
        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.05);
        min-height: 125px;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .stat-value {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 5px;
    }


    /* =====================================================
       GAME CARD CONTAINERS
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
        background: rgba(255,255,255,0.94);
        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #c4b5fd !important;
        box-shadow:
            0 15px 35px rgba(109, 40, 217, 0.10);
    }


    /* =====================================================
       CARD BUTTONS
       ===================================================== */

    .stButton button {
        border-radius: 11px;
        font-weight: 700;
        min-height: 42px;
    }


    /* =====================================================
       PRIMARY BUTTON
       ===================================================== */

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


    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-heading {
        font-size: 1.65rem;
        font-weight: 800;
        color: #1e293b;
        margin-top: 1.8rem;
        margin-bottom: 0.2rem;
    }

    .section-description {
        color: #64748b;
        margin-bottom: 1rem;
    }


    /* =====================================================
       GAME HEADER
       ===================================================== */

    .game-title-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 22px;
        padding: 2rem;
        box-shadow:
            0 10px 30px rgba(15,23,42,0.05);

        margin-bottom: 1.5rem;
    }


    /* =====================================================
       PROGRESS
       ===================================================== */

    .progress-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.4rem;
        margin-top: 1.5rem;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.markdown(
        "<div class='login-spacer'></div>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 1.3, 1]
    )

    with center:

        st.markdown(
            "## 💊 PharmaQuest"
        )

        st.caption(
            "Learn Pharmacy • Solve Cases • Build Clinical Confidence"
        )

        st.divider()

        if st.session_state.login_mode == "login":

            st.subheader("Welcome back 👋")

            st.write(
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

            st.write("")

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

            st.subheader("Create your account ✨")

            st.write(
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

            st.write("")

            if st.button(
                "Create my PharmaQuest account",
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

                                st.success(
                                    "Account created successfully!"
                                )

                                st.rerun()

                            else:

                                st.success(
                                    "Account created successfully. "
                                    "Please confirm your email, then log in."
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

        st.title("💊 PharmaQuest")

        st.caption(
            "Pharmacy Learning Arena"
        )

        st.divider()

        st.write(
            f"**{username}**"
        )

        st.caption(
            f"{title} • Level {level}"
        )

        st.progress(
            min(
                (xp % 500) / 500,
                1
            )
        )

        st.caption(
            f"{xp} XP"
        )

        st.divider()

        st.caption("MAIN")

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

        st.divider()

        st.caption("PLAY & PRACTICE")

        games = [
            ("🕵️  Drug Detective", "Drug Detective"),
            ("🩺  Patient Case", "Patient Case"),
            ("🗣️  AI Patient", "AI Patient"),
            ("⚔️  Pharma Battle", "Pharma Battle"),
            ("🔐  Escape Room", "Escape Room"),
            ("🧬  Build the Patient", "Build the Patient"),
        ]

        for label, page in games:

            if st.button(
                label,
                use_container_width=True
            ):

                st.session_state.page = page
                st.rerun()

        st.divider()

        st.caption("LEARN")

        if st.button(
            "🧠  AI Quiz",
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

        st.divider()

        st.caption("ACCOUNT")

        if st.button(
            "🏆  My Profile",
            use_container_width=True
        ):

            st.session_state.page = "Profile"
            st.rerun()

        if st.button(
            "🚪  Logout",
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

    with st.container(
        border=True
    ):

        st.markdown(
            f"### {icon}  {title}"
        )

        st.write(
            description
        )

        st.caption(
            f"Reward: +{xp} XP"
        )

        if st.button(
            "Open mission →",
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

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="hero-box">
            <h1>Welcome back, {username} 👋</h1>
            <p>
                Build your pharmacy knowledge through clinical
                cases, investigations and interactive challenges.
            </p>
            <p>
                <strong>{title}</strong> • Level {level}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="stat-box">
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
                <div class="stat-label">Streak</div>
                <div class="stat-value">🔥 {streak}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Badges</div>
                <div class="stat-value">🏆 {badges}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # MISSION SECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">Choose your mission</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Select a learning activity and strengthen your clinical skills.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ROW 1
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        game_card(
            "🕵️",
            "Drug Detective",
            "Investigate clinical clues and identify the mystery medicine.",
            50,
            "Drug Detective"
        )

    with c2:

        game_card(
            "🩺",
            "Patient Case",
            "Analyze a fictional patient case and make a therapeutic decision.",
            75,
            "Patient Case"
        )

    with c3:

        game_card(
            "🗣️",
            "AI Patient",
            "Interview a simulated patient and practice clinical questioning.",
            60,
            "AI Patient"
        )

    # --------------------------------------------------------
    # ROW 2
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        game_card(
            "⚔️",
            "Pharma Battle",
            "Challenge your pharmacology and therapeutics knowledge.",
            100,
            "Pharma Battle"
        )

    with c2:

        game_card(
            "🔐",
            "Escape Room",
            "Solve pharmacy puzzles and unlock the next stage.",
            100,
            "Escape Room"
        )

    with c3:

        game_card(
            "🧬",
            "Build the Patient",
            "Construct a patient profile and develop a treatment strategy.",
            80,
            "Build the Patient"
        )

    # --------------------------------------------------------
    # ROW 3
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        game_card(
            "🧠",
            "AI Quiz",
            "Generate pharmacy MCQs and test your understanding.",
            40,
            "AI Quiz"
        )

    with c2:

        game_card(
            "🔥",
            "Daily Challenge",
            "Complete a daily pharmacy challenge and maintain your streak.",
            50,
            "Daily Challenge"
        )

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.markdown(
        '<div class="progress-box">',
        unsafe_allow_html=True
    )

    st.subheader(
        f"Level {level} — {title}"
    )

    current_level_start = {
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
        next_xp - current_level_start,
        1
    )

    progress = (
        xp - current_level_start
    ) / progress_range

    progress = max(
        0,
        min(progress, 1)
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
            <h1>{icon} {title}</h1>
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
        "🕵️",
        "Drug Detective",
        "Investigate clues, connect the evidence and identify the mystery medicine."
    )

    topic = st.text_input(
        "Investigation topic",
        placeholder="Example: antibiotics, diabetes, cardiovascular drugs"
    )

    if st.button(
        "🔎 Start investigation",
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
You are creating an educational pharmacy mystery
game for Pharm-D students.

Topic:
{topic}

Create a Drug Detective mystery.

Include:
1. Three clinical clues.
2. One mechanism-of-action clue.
3. One adverse-effect clue.
4. One patient-related clue.
5. Ask the student to identify the medicine.

Do NOT reveal the answer immediately.

Keep it educational and fictional.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                    st.session_state.drug_result = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.drug_result:

        st.divider()

        st.subheader(
            "🔍 Mystery Case"
        )

        st.write(
            st.session_state.drug_result
        )

        if st.button(
            "✅ Complete investigation",
            type="primary"
        ):

            save_progress(
                xp_add=50,
                mission_complete=True
            )

            st.session_state.drug_result = None

            st.success(
                "Investigation completed. +50 XP"
            )


# ============================================================
# PATIENT CASE
# ============================================================

def patient_case():

    game_header(
        "🩺",
        "Patient Case",
        "Analyze a fictional patient and choose the most appropriate therapeutic approach."
    )

    topic = st.text_input(
        "Clinical topic",
        placeholder="Example: hypertension, diabetes, asthma"
    )

    if st.button(
        "🩺 Generate clinical case",
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
                    "Gemini API key is not configured."
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
- medical history
- current medicines
- relevant laboratory or vital information
- important clinical clues
- three possible therapeutic decisions

Ask the student what they would recommend.

Do not reveal the correct answer immediately.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.session_state.case_result = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.case_result:

        st.divider()

        st.subheader(
            "🩺 Clinical Case"
        )

        st.write(
            st.session_state.case_result
        )

        if st.button(
            "🎯 Complete case",
            type="primary"
        ):

            save_progress(
                xp_add=75,
                mission_complete=True
            )

            st.session_state.case_result = None

            st.success(
                "Case completed. +75 XP"
            )


# ============================================================
# AI PATIENT
# ============================================================

def ai_patient():

    game_header(
        "🗣️",
        "AI Patient",
        "Practice asking clinical questions through a simulated patient conversation."
    )

    condition = st.text_input(
        "Patient condition",
        placeholder="Example: diabetes"
    )

    question = st.text_input(
        "Ask your patient",
        placeholder="Example: When did your symptoms begin?"
    )

    if st.button(
        "🗣️ Talk to patient",
        type="primary"
    ):

        if not condition:

            st.warning(
                "Enter a patient condition."
            )

        elif not question:

            st.warning(
                "Ask the patient a question."
            )

        else:

            client = get_gemini()

            if not client:

                st.error(
                    "Gemini API key is not configured."
                )

            else:

                prompt = f"""
Act as a fictional pharmacy patient.

Condition:
{condition}

Student question:
{question}

Respond naturally as the patient.

Do not act as a doctor.
Do not provide a definitive diagnosis.
Keep the response realistic and educational.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.session_state.patient_result = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.patient_result:

        st.divider()

        st.subheader(
            "🗣️ Patient response"
        )

        st.write(
            st.session_state.patient_result
        )


# ============================================================
# AI QUIZ
# ============================================================

def ai_quiz():

    game_header(
        "🧠",
        "AI Quiz",
        "Generate pharmacy MCQs and challenge your understanding."
    )

    topic = st.text_input(
        "Quiz topic",
        placeholder="Example: pharmacology, medicinal chemistry"
    )

    if st.button(
        "🧠 Generate quiz",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a quiz topic."
            )

        else:

            client = get_gemini()

            if not client:

                st.error(
                    "Gemini API key is not configured."
                )

            else:

                prompt = f"""
Create 5 pharmacy MCQs for a Pharm-D student.

Topic:
{topic}

For each question:
- Give four options A, B, C and D.
- Give the correct answer.
- Give a one-sentence explanation.

Keep the questions educational and clinically relevant.
"""

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.session_state.quiz_result = response.text

                except Exception as e:

                    st.error(
                        f"AI error: {str(e)}"
                    )

    if st.session_state.quiz_result:

        st.divider()

        st.subheader(
            "🧠 Your Quiz"
        )

        st.write(
            st.session_state.quiz_result
        )

        if st.button(
            "🏆 Complete quiz",
            type="primary"
        ):

            save_progress(
                xp_add=40,
                mission_complete=True
            )

            st.session_state.quiz_result = None

            st.success(
                "Quiz completed. +40 XP"
            )


# ============================================================
# PROFESSIONAL PLACEHOLDER GAME
# ============================================================

def placeholder_game(
    icon,
    title,
    description,
    xp,
    features
):

    game_header(
        icon,
        title,
        description
    )

    st.subheader(
        "Mission briefing"
    )

    st.write(
        "This learning module is connected to your "
        "PharmaQuest account and is ready for gameplay."
    )

    st.divider()

    st.subheader(
        "What you'll practice"
    )

    for feature in features:

        st.write(
            f"✓ {feature}"
        )

    st.divider()

    st.info(
        f"Demo mission reward: +{xp} XP"
    )

    if st.button(
        f"🎯 Complete demo mission (+{xp} XP)",
        type="primary"
    ):

        save_progress(
            xp_add=xp,
            mission_complete=True
        )

        st.success(
            f"Mission completed. +{xp} XP added."
        )


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
        "📊",
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
        "🏆",
        "My Profile",
        "Your personal PharmaQuest learning identity."
    )

    st.subheader(
        username
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

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    if page == "Home":

        home_page()

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    elif page == "Progress":

        progress_page()

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    elif page == "Profile":

        profile_page()

    # --------------------------------------------------------
    # DRUG DETECTIVE
    # --------------------------------------------------------

    elif page == "Drug Detective":

        drug_detective()

    # --------------------------------------------------------
    # PATIENT CASE
    # --------------------------------------------------------

    elif page == "Patient Case":

        patient_case()

    # --------------------------------------------------------
    # AI PATIENT
    # --------------------------------------------------------

    elif page == "AI Patient":

        ai_patient()

    # --------------------------------------------------------
    # AI QUIZ
    # --------------------------------------------------------

    elif page == "AI Quiz":

        ai_quiz()

    # --------------------------------------------------------
    # PHARMA BATTLE
    # --------------------------------------------------------

    elif page == "Pharma Battle":

        placeholder_game(
            "⚔️",
            "Pharma Battle",
            "Challenge your pharmacy knowledge through competitive rounds.",
            100,
            [
                "Pharmacology questions",
                "Therapeutics challenges",
                "Timed decision making",
                "Clinical knowledge testing"
            ]
        )

    # --------------------------------------------------------
    # ESCAPE ROOM
    # --------------------------------------------------------

    elif page == "Escape Room":

        placeholder_game(
            "🔐",
            "Escape Room",
            "Solve pharmacy puzzles and unlock your way to the final stage.",
            100,
            [
                "Decode medication clues",
                "Solve clinical puzzles",
                "Identify hidden evidence",
                "Complete the final pharmacy challenge"
            ]
        )

    # --------------------------------------------------------
    # BUILD THE PATIENT
    # --------------------------------------------------------

    elif page == "Build the Patient":

        placeholder_game(
            "🧬",
            "Build the Patient",
            "Construct a patient profile and develop a safe treatment strategy.",
            80,
            [
                "Select patient characteristics",
                "Identify relevant clinical information",
                "Review medication history",
                "Build a treatment strategy"
            ]
        )

    # --------------------------------------------------------
    # DAILY CHALLENGE
    # --------------------------------------------------------

    elif page == "Daily Challenge":

        placeholder_game(
            "🔥",
            "Daily Challenge",
            "Complete today's pharmacy challenge and keep your learning streak alive.",
            50,
            [
                "One focused daily challenge",
                "Quick clinical reasoning",
                "Pharmacy knowledge review",
                "Maintain your learning streak"
            ]
        )
