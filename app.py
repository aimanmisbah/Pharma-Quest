import streamlit as st
from google import genai
from supabase import create_client
import json
import re


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

    # Patient Case
    "patient_case_data": None,
    "patient_feedback": None,

    # AI Patient
    "patient_condition": None,
    "patient_messages": [],

    # Quiz
    "quiz_data": None,
    "quiz_answers": {},
    "quiz_submitted": False,

    # Generic missions
    "generic_mission": None,
    "generic_feedback": None,
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


def ask_ai(prompt):

    client = get_gemini()

    if not client:
        raise Exception(
            "Gemini API is not configured. "
            "Please check GEMINI_API_KEY in Streamlit Secrets."
        )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    if not response or not response.text:
        raise Exception("Gemini returned an empty response.")

    return response.text.strip()


# ============================================================
# LEVEL SYSTEM
# ============================================================

def get_level_info(xp):

    if xp < 500:
        return 1, "Pharma Initiate", 500

    if xp < 1200:
        return 2, "Drug Seeker", 1200

    if xp < 2500:
        return 3, "Pharma Strategist", 2500

    if xp < 4500:
        return 4, "Clinical Specialist", 4500

    if xp < 7000:
        return 5, "Therapeutics Master", 7000

    return 6, "PharmaQuest Elite", 10000


# ============================================================
# PROFILE
# ============================================================

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
        pass

    return None


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

    if not supabase or not st.session_state.user:
        return

    profile = st.session_state.profile

    if not profile:
        return

    try:

        current_xp = int(profile.get("xp", 0))
        missions = int(
            profile.get("missions_completed", 0)
        )

        new_xp = current_xp + xp_add

        if mission_complete:
            missions += 1

        level, _, _ = get_level_info(new_xp)

        update_data = {
            "xp": new_xp,
            "level": level,
            "missions_completed": missions
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
            f"Could not save progress: {e}"
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

    st.rerun()


# ============================================================
# PROFESSIONAL CSS
#
# IMPORTANT:
# This CSS contains ONLY styling.
# All visible interface text below is produced with
# normal Streamlit components, so HTML code cannot appear
# as visible text.
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #f5f3ff 48%,
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


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 43px;
    border-radius: 11px;
    border: 1px solid transparent;
    background: transparent;
    color: #334155;
    font-weight: 600;
    text-align: left;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #f3f0ff;
    border-color: #ddd6fe;
    color: #6d28d9;
}


/* HERO */

.hero-container {
    padding: 2.5rem;
    border-radius: 25px;
    background:
        linear-gradient(
            135deg,
            #6d28d9,
            #9333ea 48%,
            #db2777
        );
    color: white;
    box-shadow:
        0 20px 50px rgba(109, 40, 217, 0.20);
    margin-bottom: 1.5rem;
}

.hero-container h1 {
    color: white;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.hero-container p {
    color: rgba(255,255,255,0.9);
    font-size: 1.05rem;
}


/* STAT CARDS */

.stat-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.3rem;
    min-height: 120px;
    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);
}

.stat-card:hover {
    border-color: #c4b5fd;
    box-shadow:
        0 12px 30px rgba(109,40,217,0.10);
}

.stat-label {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stat-value {
    color: #1e293b;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 7px;
}


/* GAME CARDS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px !important;
    border: 1px solid #e2e8f0 !important;
    background: rgba(255,255,255,0.96);
    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);
    transition: 0.2s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #c4b5fd !important;
    box-shadow:
        0 15px 35px rgba(109,40,217,0.10);
}


/* BUTTONS */

.stButton button {
    border-radius: 11px;
    font-weight: 700;
    min-height: 42px;
}

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
}


/* INPUTS */

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid #cbd5e1;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.12);
}


/* MISSION HEADER */

.mission-panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 22px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow:
        0 10px 30px rgba(15,23,42,0.05);
}


/* LOGIN */

.login-panel {
    background: white;
    padding: 2.3rem;
    border-radius: 22px;
    border: 1px solid #e5e7eb;
    box-shadow:
        0 15px 40px rgba(15,23,42,0.08);
}


/* ANSWER BOX */

.answer-panel {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.3rem;
}


/* BADGES */

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: #f3e8ff;
    color: #7e22ce;
    font-weight: 700;
    font-size: 0.8rem;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.write("")

    left, center, right = st.columns(
        [1, 1.25, 1]
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

            st.subheader("Welcome back")

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
                        "Check Streamlit Secrets."
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
                            f"Login failed: {e}"
                        )

            st.divider()

            if st.button(
                "Create a new account",
                use_container_width=True
            ):

                st.session_state.login_mode = "signup"

                st.rerun()

        else:

            st.subheader("Create your account")

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

            confirm = st.text_input(
                "Confirm password",
                type="password",
                key="signup_confirm"
            )

            if st.button(
                "Create my PharmaQuest account",
                type="primary",
                use_container_width=True
            ):

                if not username or not email or not password:

                    st.error(
                        "Please complete all fields."
                    )

                elif password != confirm:

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
                                    "Confirm your email, then sign in."
                                )

                        else:

                            st.error(
                                "Could not create account."
                            )

                    except Exception as e:

                        st.error(
                            f"Signup failed: {e}"
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

    xp = int(
        profile.get("xp", 0)
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

        progress = min(
            (xp % 500) / 500,
            1
        )

        st.progress(progress)

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

    with st.container(border=True):

        st.markdown(
            f"## {icon}"
        )

        st.subheader(title)

        st.write(description)

        st.caption(
            f"REWARD  •  +{xp} XP"
        )

        if st.button(
            "Enter mission  →",
            key=f"mission_{page}",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = page
            st.rerun()


# ============================================================
# HOME
# ============================================================

def home_page():

    profile = st.session_state.profile

    username = profile.get(
        "username",
        "Future Pharmacist"
    )

    xp = int(
        profile.get("xp", 0)
    )

    missions = int(
        profile.get(
            "missions_completed",
            0
        )
    )

    streak = int(
        profile.get(
            "streak",
            0
        )
    )

    badges = int(
        profile.get(
            "badges",
            0
        )
    )

    level, title, next_xp = get_level_info(xp)

    # HERO

    st.markdown(
        "## Welcome back, "
        + username
        + " 👋"
    )

    st.caption(
        "Your pharmacy learning arena"
    )

    st.markdown(
        """
        <div class="hero-container">
        <h1>Build clinical confidence.</h1>
        <p>
        Investigate medicines, solve patient cases,
        interview simulated patients and test your
        pharmacy knowledge with AI-powered missions.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # STATS

    c1, c2, c3, c4 = st.columns(4)

    stats = [
        ("TOTAL XP", str(xp)),
        ("MISSIONS", str(missions)),
        ("STREAK", f"🔥 {streak}"),
        ("BADGES", f"🏆 {badges}")
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4],
        stats
    ):

        with col:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    st.subheader("Choose your mission")

    st.caption(
        "Every mission is designed to make you actively think, answer and learn."
    )

    # ROW 1

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
            "Analyze a fictional patient and make a therapeutic recommendation.",
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

    # ROW 2

    c1, c2, c3 = st.columns(3)

    with c1:

        game_card(
            "⚔️",
            "Pharma Battle",
            "Test your pharmacology knowledge through rapid clinical challenges.",
            100,
            "Pharma Battle"
        )

    with c2:

        game_card(
            "🔐",
            "Escape Room",
            "Solve pharmacy clues and unlock the final challenge.",
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

    # ROW 3

    c1, c2 = st.columns(2)

    with c1:

        game_card(
            "🧠",
            "AI Quiz",
            "Answer pharmacy MCQs and receive immediate correction.",
            40,
            "AI Quiz"
        )

    with c2:

        game_card(
            "🔥",
            "Daily Challenge",
            "Complete a focused pharmacy challenge and earn XP.",
            50,
            "Daily Challenge"
        )

    st.write("")

    st.subheader(
        f"Level {level} • {title}"
    )

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

    st.progress(progress)

    st.caption(
        f"{xp} / {next_xp} XP toward the next level"
    )


# ============================================================
# MISSION HEADER
# ============================================================

def mission_header(
    icon,
    title,
    description
):

    st.markdown(
        f"## {icon} {title}"
    )

    st.caption(
        description
    )

    st.divider()


# ============================================================
# DRUG DETECTIVE
# ============================================================

def drug_detective():

    mission_header(
        "🕵️",
        "Drug Detective",
        "Investigate the evidence, submit your hypothesis and receive AI feedback."
    )

    topic = st.text_input(
        "What should we investigate?",
        placeholder="Example: antibiotics, asthma, hypertension, diabetes"
    )

    if st.button(
        "🔎 Generate mystery",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a pharmacy topic first."
            )

        else:

            prompt = f"""
You are creating a pharmacy educational mystery
for a Pharm-D student.

Topic: {topic}

Create ONE fictional Drug Detective case.

Return ONLY valid JSON:

{{
  "case": "short patient scenario",
  "clue1": "clinical clue",
  "clue2": "mechanism clue",
  "clue3": "adverse effect clue",
  "clue4": "patient-related clue",
  "question": "What medicine is most likely?"
  "answer": "correct medicine",
  "explanation": "educational explanation"
}}

Do not make the case dangerous.
Do not use a real patient's information.
"""

            try:

                raw = ask_ai(prompt)

                match = re.search(
                    r"\{.*\}",
                    raw,
                    re.DOTALL
                )

                if not match:
                    raise Exception(
                        "AI did not return the expected format."
                    )

                data = json.loads(
                    match.group()
                )

                st.session_state.drug_case = data
                st.session_state.drug_feedback = None

            except Exception as e:

                st.error(
                    f"Could not generate mission: {e}"
                )

    data = st.session_state.drug_case

    if data:

        st.subheader("Case file")

        st.info(
            data.get("case", "")
        )

        st.write(
            f"**Evidence 01 — Clinical:** "
            f"{data.get('clue1', '')}"
        )

        st.write(
            f"**Evidence 02 — Mechanism:** "
            f"{data.get('clue2', '')}"
        )

        st.write(
            f"**Evidence 03 — Adverse effect:** "
            f"{data.get('clue3', '')}"
        )

        st.write(
            f"**Evidence 04 — Patient:** "
            f"{data.get('clue4', '')}"
        )

        st.divider()

        st.subheader(
            "Your hypothesis"
        )

        answer = st.text_input(
            data.get(
                "question",
                "What medicine is most likely?"
            ),
            key="drug_answer"
        )

        if st.button(
            "Submit hypothesis",
            type="primary"
        ):

            if not answer:

                st.warning(
                    "Submit your answer first."
                )

            else:

                prompt = f"""
You are grading a pharmacy student.

Mystery:
{data.get('case')}

Correct medicine:
{data.get('answer')}

Student answer:
{answer}

Evaluate the student's answer.

Return:
1. Correct / Partially correct / Incorrect
2. Why
3. Key learning point

Be encouraging but academically accurate.
"""

                try:

                    feedback = ask_ai(prompt)

                    st.session_state.drug_feedback = feedback

                except Exception as e:

                    st.error(
                        f"Could not grade answer: {e}"
                    )

    if st.session_state.drug_feedback:

        st.divider()

        st.subheader(
            "🎓 Investigator feedback"
        )

        st.success(
            st.session_state.drug_feedback
        )

        st.info(
            f"Correct answer: {data.get('answer')}"
        )

        st.write(
            f"**Explanation:** {data.get('explanation', '')}"
        )

        if st.button(
            "🏆 Complete mission (+50 XP)",
            type="primary"
        ):

            save_progress(
                xp_add=50,
                mission_complete=True
            )

            st.session_state.drug_case = None
            st.session_state.drug_feedback = None

            st.success(
                "Mission completed. +50 XP"
            )


# ============================================================
# PATIENT CASE
# ============================================================

def patient_case():

    mission_header(
        "🩺",
        "Patient Case",
        "Review the patient, make a recommendation and receive clinical reasoning feedback."
    )

    topic = st.text_input(
        "Clinical topic",
        placeholder="Example: hypertension, asthma, diabetes"
    )

    if st.button(
        "🩺 Generate patient case",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a clinical topic."
            )

        else:

            prompt = f"""
Create one fictional educational pharmacy case
for a Pharm-D student.

Topic: {topic}

Return ONLY valid JSON:

{{
 "patient": "age, sex and short background",
 "complaint": "chief complaint",
 "history": "relevant medical history",
 "medicines": "current medicines",
 "findings": "important vitals/labs",
 "question": "what should the pharmacist recommend?",
 "ideal_answer": "best educational recommendation",
 "reasoning": "clinical reasoning"
}}

Keep it educational and fictional.
"""

            try:

                raw = ask_ai(prompt)

                match = re.search(
                    r"\{.*\}",
                    raw,
                    re.DOTALL
                )

                if not match:
                    raise Exception(
                        "Unexpected AI response."
                    )

                st.session_state.patient_case_data = json.loads(
                    match.group()
                )

                st.session_state.patient_feedback = None

            except Exception as e:

                st.error(
                    f"Could not generate case: {e}"
                )

    data = st.session_state.patient_case_data

    if data:

        st.subheader("Patient profile")

        st.write(
            f"**Patient:** {data.get('patient', '')}"
        )

        st.write(
            f"**Chief complaint:** {data.get('complaint', '')}"
        )

        st.write(
            f"**Medical history:** {data.get('history', '')}"
        )

        st.write(
            f"**Current medicines:** {data.get('medicines', '')}"
        )

        st.write(
            f"**Clinical findings:** {data.get('findings', '')}"
        )

        st.divider()

        st.subheader(
            "Your clinical decision"
        )

        st.write(
            data.get(
                "question",
                "What should the pharmacist recommend?"
            )
        )

        answer = st.text_area(
            "Write your recommendation",
            placeholder="Explain what you would recommend and why...",
            height=150,
            key="case_answer"
        )

        if st.button(
            "Submit clinical decision",
            type="primary"
        ):

            if not answer:

                st.warning(
                    "Write your recommendation first."
                )

            else:

                prompt = f"""
You are evaluating a Pharm-D student.

Patient case:
{data.get('patient')}

History:
{data.get('history')}

Medicines:
{data.get('medicines')}

Findings:
{data.get('findings')}

Ideal educational answer:
{data.get('ideal_answer')}

Student response:
{answer}

Give structured feedback:

Score out of 10:
What the student did well:
What was missing:
Clinical reasoning:
Final verdict:

Do not be unnecessarily harsh.
"""

                try:

                    st.session_state.patient_feedback = ask_ai(
                        prompt
                    )

                except Exception as e:

                    st.error(
                        f"Could not evaluate answer: {e}"
                    )

    if st.session_state.patient_feedback:

        st.divider()

        st.subheader(
            "🎓 Clinical feedback"
        )

        st.write(
            st.session_state.patient_feedback
        )

        with st.expander(
            "View model learning answer"
        ):

            st.write(
                data.get(
                    "ideal_answer",
                    ""
                )
            )

            st.write(
                f"**Reasoning:** "
                f"{data.get('reasoning', '')}"
            )

        if st.button(
            "🏆 Complete case (+75 XP)",
            type="primary"
        ):

            save_progress(
                xp_add=75,
                mission_complete=True
            )

            st.session_state.patient_case_data = None
            st.session_state.patient_feedback = None

            st.success(
                "Clinical case completed. +75 XP"
            )


# ============================================================
# AI PATIENT
# ============================================================

def ai_patient():

    mission_header(
        "🗣️",
        "AI Patient",
        "Interview a simulated patient. You ask the questions; the patient responds."
    )

    condition = st.text_input(
        "Patient condition",
        placeholder="Example: asthma, diabetes, hypertension"
    )

    if st.button(
        "Start patient interview",
        type="primary"
    ):

        if not condition:

            st.warning(
                "Enter a condition first."
            )

        else:

            st.session_state.patient_condition = condition
            st.session_state.patient_messages = []

            st.success(
                "Patient interview started."
            )

    if st.session_state.patient_condition:

        st.info(
            f"Simulated patient condition: "
            f"{st.session_state.patient_condition}"
        )

        for message in st.session_state.patient_messages:

            if message["role"] == "student":

                st.chat_message(
                    "user"
                ).write(
                    message["text"]
                )

            else:

                st.chat_message(
                    "assistant"
                ).write(
                    message["text"]
                )

        question = st.chat_input(
            "Ask your patient a question..."
        )

        if question:

            st.session_state.patient_messages.append(
                {
                    "role": "student",
                    "text": question
                }
            )

            conversation = "\n".join(
                [
                    f"{m['role']}: {m['text']}"
                    for m in st.session_state.patient_messages
                ]
            )

            prompt = f"""
Act as a fictional pharmacy patient.

Condition:
{st.session_state.patient_condition}

Conversation:
{conversation}

Answer ONLY as the patient.

Rules:
- Respond naturally.
- Give information appropriate to the question.
- Do not diagnose the patient.
- Do not act as the pharmacist.
- Do not provide a treatment plan.
- Keep the answer realistic.
"""

            try:

                response = ask_ai(prompt)

                st.session_state.patient_messages.append(
                    {
                        "role": "patient",
                        "text": response
                    }
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"AI patient error: {e}"
                )

        if st.button(
            "🏆 Finish interview (+60 XP)",
            type="primary"
        ):

            if len(st.session_state.patient_messages) < 2:

                st.warning(
                    "Ask a few questions before completing the interview."
                )

            else:

                save_progress(
                    xp_add=60,
                    mission_complete=True
                )

                st.session_state.patient_condition = None
                st.session_state.patient_messages = []

                st.success(
                    "Interview completed. +60 XP"
                )


# ============================================================
# AI QUIZ
# ============================================================

def ai_quiz():

    mission_header(
        "🧠",
        "AI Quiz",
        "Answer pharmacy MCQs and receive correction with explanations."
    )

    topic = st.text_input(
        "Quiz topic",
        placeholder="Example: pharmacology, antibiotics, autonomic drugs"
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
                "Enter a quiz topic."
            )

        else:

            prompt = f"""
Create 5 pharmacy MCQs for a Pharm-D student.

Topic:
{topic}

Difficulty:
{difficulty}

Return ONLY valid JSON as:

[
 {{
  "question": "...",
  "options": [
    "A. ...",
    "B. ...",
    "C. ...",
    "D. ..."
  ],
  "answer": "A",
  "explanation": "..."
 }}
]

Make the questions academically useful.
"""

            try:

                raw = ask_ai(prompt)

                match = re.search(
                    r"\[.*\]",
                    raw,
                    re.DOTALL
                )

                if not match:
                    raise Exception(
                        "AI did not return valid quiz data."
                    )

                st.session_state.quiz_data = json.loads(
                    match.group()
                )

                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False

            except Exception as e:

                st.error(
                    f"Could not generate quiz: {e}"
                )

    quiz = st.session_state.quiz_data

    if quiz:

        st.divider()

        st.subheader(
            "Your challenge"
        )

        for i, question in enumerate(
            quiz
        ):

            st.write(
                f"### Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            selected = st.radio(
                "Choose one answer",
                question["options"],
                key=f"quiz_{i}",
                label_visibility="collapsed"
            )

            st.session_state.quiz_answers[i] = selected

            st.divider()

        if st.button(
            "Submit quiz",
            type="primary"
        ):

            score = 0

            for i, question in enumerate(quiz):

                selected = st.session_state.quiz_answers.get(
                    i,
                    ""
                )

                correct_letter = question["answer"].upper()

                if selected.startswith(
                    correct_letter + "."
                ):

                    score += 1

            st.session_state.quiz_submitted = True

            st.success(
                f"You scored {score} / {len(quiz)}"
            )

        if st.session_state.quiz_submitted:

            st.subheader(
                "Answer review"
            )

            for i, question in enumerate(quiz):

                selected = st.session_state.quiz_answers.get(
                    i,
                    ""
                )

                correct = question["answer"].upper()

                if selected.startswith(
                    correct + "."
                ):

                    st.success(
                        f"Question {i + 1}: Correct"
                    )

                else:

                    st.error(
                        f"Question {i + 1}: Incorrect"
                    )

                st.write(
                    f"Correct answer: "
                    f"{correct}"
                )

                st.caption(
                    question["explanation"]
                )

            score = sum(
                1
                for i, q in enumerate(quiz)
                if st.session_state.quiz_answers.get(
                    i,
                    ""
                ).startswith(
                    q["answer"].upper() + "."
                )
            )

            xp = 40 + (score * 5)

            if st.button(
                f"🏆 Complete quiz (+{xp} XP)",
                type="primary"
            ):

                save_progress(
                    xp_add=xp,
                    mission_complete=True
                )

                st.session_state.quiz_data = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False

                st.success(
                    f"Quiz completed. +{xp} XP"
                )


# ============================================================
# GENERIC AI MISSION
# ============================================================

def generic_ai_mission(
    icon,
    title,
    description,
    xp,
    mission_type
):

    mission_header(
        icon,
        title,
        description
    )

    topic = st.text_input(
        "Mission topic",
        placeholder="Example: antibiotics, diabetes, asthma"
    )

    if st.button(
        "Generate mission",
        type="primary"
    ):

        if not topic:

            st.warning(
                "Enter a topic first."
            )

        else:

            prompt = f"""
Create one interactive pharmacy educational mission.

Mission type:
{mission_type}

Topic:
{topic}

Create:
- a realistic fictional scenario
- 4 useful clues
- one clear student task
- a correct educational answer
- a short explanation

Do NOT immediately reveal the answer.
"""

            try:

                st.session_state.generic_mission = ask_ai(
                    prompt
                )

                st.session_state.generic_feedback = None

            except Exception as e:

                st.error(
                    f"Could not generate mission: {e}"
                )

    if st.session_state.generic_mission:

        st.subheader(
            "Mission briefing"
        )

        st.write(
            st.session_state.generic_mission
        )

        answer = st.text_area(
            "Your answer",
            placeholder="Write your reasoning or answer here...",
            height=150
        )

        if st.button(
            "Submit answer",
            type="primary"
        ):

            prompt = f"""
You are grading a pharmacy student.

Mission:
{st.session_state.generic_mission}

Student answer:
{answer}

Give:
- Score out of 10
- Correct / Partially correct / Incorrect
- What was good
- What should be improved
- Correct learning point

Be educational.
"""

            try:

                st.session_state.generic_feedback = ask_ai(
                    prompt
                )

            except Exception as e:

                st.error(
                    f"Could not grade answer: {e}"
                )

    if st.session_state.generic_feedback:

        st.divider()

        st.subheader(
            "🎓 AI feedback"
        )

        st.write(
            st.session_state.generic_feedback
        )

        if st.button(
            f"🏆 Complete mission (+{xp} XP)",
            type="primary"
        ):

            save_progress(
                xp_add=xp,
                mission_complete=True
            )

            st.session_state.generic_mission = None
            st.session_state.generic_feedback = None

            st.success(
                f"Mission completed. +{xp} XP"
            )


# ============================================================
# PROGRESS PAGE
# ============================================================

def progress_page():

    profile = st.session_state.profile

    xp = int(
        profile.get("xp", 0)
    )

    missions = int(
        profile.get(
            "missions_completed",
            0
        )
    )

    level, title, next_xp = get_level_info(xp)

    mission_header(
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
# PROFILE
# ============================================================

def profile_page():

    profile = st.session_state.profile

    username = profile.get(
        "username",
        "Student"
    )

    xp = int(
        profile.get("xp", 0)
    )

    level, title, _ = get_level_info(xp)

    mission_header(
        "🏆",
        "My Profile",
        "Your personal PharmaQuest learning identity."
    )

    st.subheader(
        username
    )

    st.caption(
        title
    )

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            f"**Level:** {level}"
        )

        st.write(
            f"**XP:** {xp}"
        )

        st.write(
            f"**Missions:** "
            f"{profile.get('missions_completed', 0)}"
        )

    with c2:

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

        generic_ai_mission(
            "⚔️",
            "Pharma Battle",
            "Challenge your pharmacology and therapeutics knowledge.",
            100,
            "competitive pharmacology battle"
        )

    elif page == "Escape Room":

        generic_ai_mission(
            "🔐",
            "Escape Room",
            "Solve pharmacy clues and unlock the final stage.",
            100,
            "pharmacy clinical escape room"
        )

    elif page == "Build the Patient":

        generic_ai_mission(
            "🧬",
            "Build the Patient",
            "Construct a patient profile and develop a safe treatment strategy.",
            80,
            "patient-building and treatment planning challenge"
        )

    elif page == "Daily Challenge":

        generic_ai_mission(
            "🔥",
            "Daily Challenge",
            "Complete today's focused pharmacy challenge.",
            50,
            "short daily pharmacy challenge"
        )
