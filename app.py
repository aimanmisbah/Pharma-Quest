
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
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(99,102,241,0.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 95% 10%,
            rgba(6,182,212,0.10),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #f8fafc 100%
        );
}


.block-container {

    max-width: 1450px;

    padding-top: 2rem;
    padding-bottom: 4rem;
}


#MainMenu {
    visibility: hidden;
}


footer {
    visibility: hidden;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f1f5ff 55%,
            #eefcff 100%
        );

    border-right:
        1px solid #e2e8f0;
}


.sidebar-brand {

    padding:
        15px 5px 22px 5px;
}


.sidebar-logo {

    width: 64px;
    height: 64px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 21px;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed,
            #06b6d4
        );

    box-shadow:
        0 15px 30px
        rgba(79,70,229,0.25);

    font-size: 32px;

    margin-bottom: 15px;
}


.sidebar-title {

    color: #172554;

    font-size: 20px;

    font-weight: 950;

    letter-spacing: -0.5px;
}


.sidebar-subtitle {

    margin-top: 4px;

    color: #94a3b8;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1px;
}


/* ==========================================================
   COMMAND CENTER
   ========================================================== */

.command-center {

    position: relative;

    overflow: hidden;

    min-height: 350px;

    padding: 45px 52px;

    border-radius: 34px;

    background:

        radial-gradient(
            circle at 88% 18%,
            rgba(34,211,238,0.25),
            transparent 23%
        ),

        radial-gradient(
            circle at 10% 95%,
            rgba(168,85,247,0.28),
            transparent 27%
        ),

        linear-gradient(
            135deg,
            #111827,
            #312e81 55%,
            #0e7490
        );

    box-shadow:

        0 30px 70px
        rgba(15,23,42,0.20),

        inset 0 1px 1px
        rgba(255,255,255,0.18);
}


.command-center:before {

    content: "";

    position: absolute;

    width: 320px;
    height: 320px;

    right: -130px;
    top: -130px;

    border-radius: 50%;

    border:
        1px solid
        rgba(255,255,255,0.12);
}


.command-center:after {

    content: "";

    position: absolute;

    width: 180px;
    height: 180px;

    right: 100px;
    bottom: -120px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.05);
}


.command-content {

    position: relative;

    z-index: 5;

    max-width: 800px;
}


.command-tag {

    display: inline-block;

    padding:
        8px 15px;

    border-radius: 999px;

    background:
        rgba(255,255,255,0.10);

    border:
        1px solid
        rgba(255,255,255,0.16);

    color: #a5f3fc;

    font-size: 10px;

    font-weight: 900;

    letter-spacing: 1.5px;
}


.command-title {

    margin-top: 20px;

    color: white;

    font-size: 46px;

    line-height: 1.08;

    font-weight: 950;

    letter-spacing: -2px;
}


.command-title span {

    display: block;

    margin-top: 4px;

    background:

        linear-gradient(
            90deg,
            #67e8f9,
            #a78bfa,
            #f0abfc
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.command-text {

    max-width: 690px;

    margin-top: 18px;

    color: #cbd5e1;

    font-size: 15px;

    line-height: 1.65;
}


/* ==========================================================
   FLOATING PHARMACY ICONS
   ========================================================== */

.floating-icon {

    position: absolute;

    z-index: 3;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 22px;

    background:
        rgba(255,255,255,0.10);

    border:
        1px solid
        rgba(255,255,255,0.18);

    backdrop-filter: blur(12px);

    box-shadow:
        0 20px 40px
        rgba(0,0,0,0.20);
}


.float-one {

    width: 78px;
    height: 78px;

    right: 100px;
    top: 60px;

    font-size: 36px;

    transform: rotate(9deg);
}


.float-two {

    width: 60px;
    height: 60px;

    right: 220px;
    top: 165px;

    font-size: 27px;

    transform: rotate(-8deg);
}


.float-three {

    width: 58px;
    height: 58px;

    right: 55px;
    bottom: 55px;

    font-size: 26px;

    transform: rotate(-12deg);
}


/* ==========================================================
   HERO MINI STATUS
   ========================================================== */

.hero-status {

    position: relative;

    z-index: 5;

    display: flex;

    gap: 12px;

    margin-top: 28px;
}


.hero-status-card {

    display: flex;

    align-items: center;

    gap: 10px;

    padding:
        11px 15px;

    border-radius: 16px;

    background:
        rgba(255,255,255,0.09);

    border:
        1px solid
        rgba(255,255,255,0.13);
}


.hero-status-icon {

    font-size: 21px;
}


.hero-status-label {

    color: #94a3b8;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 1px;
}


.hero-status-value {

    color: white;

    font-size: 12px;

    font-weight: 900;
}


/* ==========================================================
   LEVEL PANEL
   ========================================================== */

.level-panel {

    margin-top: 20px;

    padding:
        22px 27px;

    border-radius: 24px;

    background: white;

    border:
        1px solid #e2e8f0;

    box-shadow:
        0 15px 35px
        rgba(15,23,42,0.07);

    display: flex;

    align-items: center;

    gap: 30px;
}


.level-badge {

    min-width: 65px;
    height: 65px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #06b6d4
        );

    color: white;

    font-size: 19px;

    font-weight: 950;

    box-shadow:
        0 10px 25px
        rgba(79,70,229,0.25);
}


.level-info {

    min-width: 220px;
}


.level-caption {

    color: #94a3b8;

    font-size: 9px;

    font-weight: 900;

    letter-spacing: 1.3px;
}


.level-name {

    color: #172554;

    font-size: 19px;

    font-weight: 950;
}


.level-description {

    color: #64748b;

    font-size: 11px;
}


.level-progress {

    flex: 1;
}


.level-progress-top {

    display: flex;

    justify-content: space-between;

    color: #475569;

    font-size: 10px;

    font-weight: 900;

    margin-bottom: 8px;
}


.progress-track {

    width: 100%;

    height: 10px;

    border-radius: 999px;

    background: #e2e8f0;

    overflow: hidden;
}


.progress-fill {

    width: 68%;

    height: 100%;

    border-radius: 999px;

    background:
        linear-gradient(
            90deg,
            #4f46e5,
            #06b6d4
        );
}


.level-bottom {

    display: flex;

    justify-content: space-between;

    color: #94a3b8;

    font-size: 9px;

    margin-top: 6px;
}


/* ==========================================================
   SECTION HEADINGS
   ========================================================== */

.section-title {

    margin-top: 32px;

    margin-bottom: 15px;

    color: #172554;

    font-size: 25px;

    font-weight: 950;
}


.section-subtitle {

    margin-top: -10px;

    margin-bottom: 17px;

    color: #94a3b8;

    font-size: 12px;

    font-weight: 600;
}


/* ==========================================================
   STAT CARDS
   ========================================================== */

.stat-card {

    min-height: 150px;

    padding: 22px;

    border-radius: 23px;

    background: white;

    border:
        1px solid
        rgba(148,163,184,0.15);

    box-shadow:
        0 12px 30px
        rgba(15,23,42,0.07);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.stat-card:hover {

    transform:
        translateY(-5px);

    box-shadow:
        0 20px 40px
        rgba(79,70,229,0.12);
}


.stat-icon {

    font-size: 27px;
}


.stat-number {

    margin-top: 6px;

    color: #172554;

    font-size: 28px;

    font-weight: 950;
}


.stat-name {

    color: #475569;

    font-size: 9px;

    font-weight: 900;

    letter-spacing: 1px;
}


.stat-description {

    margin-top: 5px;

    color: #94a3b8;

    font-size: 10px;
}


/* ==========================================================
   MISSION CARDS
   ========================================================== */

.mission-card {

    min-height: 250px;

    margin-bottom: 20px;

    padding: 22px;

    border-radius: 25px;

    background: white;

    border:
        1px solid
        rgba(148,163,184,0.14);

    box-shadow:
        0 12px 30px
        rgba(15,23,42,0.07);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.mission-card:hover {

    transform:
        translateY(-7px);

    box-shadow:
        0 25px 50px
        rgba(79,70,229,0.14);
}


.mission-header {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;
}


.mission-icon {

    width: 58px;
    height: 58px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #ecfeff
        );

    font-size: 30px;
}


.mission-type {

    padding:
        6px 9px;

    border-radius: 999px;

    background: #f1f5f9;

    color: #64748b;

    font-size: 7px;

    font-weight: 950;

    letter-spacing: 1px;
}


.mission-name {

    margin-top: 17px;

    color: #172554;

    font-size: 18px;

    font-weight: 950;
}


.mission-description {

    min-height: 58px;

    margin-top: 8px;

    color: #64748b;

    font-size: 11px;

    line-height: 1.55;
}


.mission-action {

    margin-top: 15px;

    color: #4f46e5;

    font-size: 9px;

    font-weight: 950;

    letter-spacing: 1px;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {

    min-height: 45px;

    border-radius: 14px;

    border: none;

    font-weight: 850;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 8px 20px
        rgba(79,70,229,0.15);
}


</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            💊
        </div>

        <div class="sidebar-title">
            MISSION CONTROL
        </div>

        <div class="sidebar-subtitle">
            PHARMACY TRAINING HUB
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "SELECT TRAINING MODE",
        [
            "🏠 Home",
            "🕵️ Drug Detective",
            "🩺 Patient Case",
            "🗣️ AI Patient",
            "⚔️ Pharma Battle",
            "🔐 Escape Room",
            "🧬 Build the Patient",
            "❓ AI Quiz",
            "🔥 Daily Challenge",
            "🏆 My Profile"
        ]
    )

    st.markdown("---")

    st.markdown("""
    <div style="
        padding:16px;
        border-radius:18px;
        background:white;
        border:1px solid #e2e8f0;
        box-shadow:0 8px 20px rgba(15,23,42,0.05);
    ">

        <div style="
            font-size:9px;
            color:#94a3b8;
            font-weight:900;
            letter-spacing:1px;
        ">
            CURRENT RANK
        </div>

        <div style="
            margin-top:5px;
            font-size:17px;
            font-weight:900;
            color:#312e81;
        ">
            🌱 Drug Explorer
        </div>

        <div style="
            margin-top:10px;
            height:6px;
            border-radius:10px;
            background:#e2e8f0;
            overflow:hidden;
        ">

            <div style="
                width:68%;
                height:100%;
                border-radius:10px;
                background:linear-gradient(
                    90deg,
                    #4f46e5,
                    #06b6d4
                );
            "></div>

        </div>

        <div style="
            margin-top:7px;
            font-size:10px;
            color:#64748b;
        ">
            ⭐ 1,250 / 1,800 XP
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    # --------------------------------------------------------
    # MAIN COMMAND CENTER
    # --------------------------------------------------------

    st.markdown("""
    <div class="command-center">

        <div class="command-content">

            <div class="command-tag">
                ⚡ PHARMACY COMMAND CENTER
            </div>

            <div class="command-title">
                Ready for your next
                <span>pharmacy mission?</span>
            </div>

            <div class="command-text">
                Train your pharmacy knowledge through challenges,
                clinical cases, patient conversations and AI-powered
                missions designed to make learning more active.
            </div>

            <div class="hero-status">

                <div class="hero-status-card">

                    <div class="hero-status-icon">
                        🧪
                    </div>

                    <div>
                        <div class="hero-status-label">
                            CURRENT RANK
                        </div>

                        <div class="hero-status-value">
                            Drug Explorer
                        </div>
                    </div>

                </div>


                <div class="hero-status-card">

                    <div class="hero-status-icon">
                        ⭐
                    </div>

                    <div>
                        <div class="hero-status-label">
                            EXPERIENCE
                        </div>

                        <div class="hero-status-value">
                            1,250 XP
                        </div>
                    </div>

                </div>


                <div class="hero-status-card">

                    <div class="hero-status-icon">
                        🔥
                    </div>

                    <div>
                        <div class="hero-status-label">
                            STREAK
                        </div>

                        <div class="hero-status-value">
                            7 Days
                        </div>
                    </div>

                </div>

            </div>

        </div>


        <div class="floating-icon float-one">
            💊
        </div>

        <div class="floating-icon float-two">
            🧬
        </div>

        <div class="floating-icon float-three">
            ⚕️
        </div>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # LEVEL
    # --------------------------------------------------------

    st.markdown("""
    <div class="level-panel">

        <div class="level-badge">
            05
        </div>

        <div class="level-info">

            <div class="level-caption">
                CURRENT LEVEL
            </div>

            <div class="level-name">
                Drug Explorer
            </div>

            <div class="level-description">
                550 XP until Clinical Challenger
            </div>

        </div>

        <div class="level-progress">

            <div class="level-progress-top">
                <span>LEVEL PROGRESS</span>
                <span>1,250 / 1,800 XP</span>
            </div>

            <div class="progress-track">
                <div class="progress-fill"></div>
            </div>

            <div class="level-bottom">
                <span>⭐ Keep going!</span>
                <span>68%</span>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Your Progress</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Build your pharmacy skills one mission at a time.</div>',
        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(4)


    stats = [

        ("🔥", "7", "DAY STREAK", "You're on fire!"),

        ("🏆", "4", "BADGES", "Keep collecting"),

        ("🧠", "23", "MISSIONS", "Completed"),

        ("⚡", "1,250", "TOTAL XP", "Experience earned")

    ]


    for col, data in zip(
        [c1, c2, c3, c4],
        stats
    ):

        icon, number, name, description = data

        with col:

            st.markdown(
                f"""
                <div class="stat-card">

                    <div class="stat-icon">
                        {icon}
                    </div>

                    <div class="stat-number">
                        {number}
                    </div>

                    <div class="stat-name">
                        {name}
                    </div>

                    <div class="stat-description">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # MISSIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Choose Your Mission</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">How will you train today?</div>',
        unsafe_allow_html=True
    )


    missions = [

        (
            "🕵️",
            "Drug Detective",
            "Investigate clues and identify the mystery medicine.",
            "DEDUCTION"
        ),

        (
            "🩺",
            "Patient Case",
            "Think like a clinical pharmacist and solve the case.",
            "CLINICAL"
        ),

        (
            "🗣️",
            "AI Patient",
            "Practice counselling with realistic patient personalities.",
            "COUNSELLING"
        ),

        (
            "⚔️",
            "Pharma Battle",
            "Answer rapid-fire questions and test your knowledge.",
            "BATTLE"
        ),

        (
            "🔐",
            "Escape Room",
            "Solve the pharmacy mystery before time runs out.",
            "MYSTERY"
        ),

        (
            "🧬",
            "Build the Patient",
            "Explore how treatment decisions affect a fictional patient.",
            "SIMULATION"
        ),

        (
            "❓",
            "AI Quiz",
            "Create a personalized pharmacy quiz with AI.",
            "KNOWLEDGE"
        ),

        (
            "🔥",
            "Daily Challenge",
            "Complete today's challenge and earn bonus XP.",
            "DAILY"
        )

    ]


    columns = st.columns(4)


    for i, mission in enumerate(missions):

        icon, title, description, category = mission

        with columns[i % 4]:

            st.markdown(
                f"""
                <div class="mission-card">

                    <div class="mission-header">

                        <div class="mission-icon">
                            {icon}
                        </div>

                        <div class="mission-type">
                            {category}
                        </div>

                    </div>

                    <div class="mission-name">
                        {title}
                    </div>

                    <div class="mission-description">
                        {description}
                    </div>

                    <div class="mission-action">
                        START MISSION →
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# DRUG DETECTIVE
# ============================================================

elif page == "🕵️ Drug Detective":

    st.title("🕵️ Drug Detective")

    st.write(
        "Investigate the clues and identify the mystery medicine."
    )

    topic = st.text_input(
        "Choose a pharmacy topic",
        placeholder="Example: antibiotics, diabetes, cardiovascular drugs"
    )


    if st.button("🔎 START INVESTIGATION"):

        api_key = os.environ.get("GEMINI_API_KEY")


        if not api_key:

            st.error(
                "Gemini API key is not connected."
            )

        else:

            try:

                from google import genai

                client = genai.Client(
                    api_key=api_key
                )


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


                with st.spinner(
                    "🧠 Creating your mystery..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )


                st.markdown(
                    "### 🔍 CASE FILE"
                )

                st.write(
                    response.text
                )


            except Exception as e:

                st.error(
                    "Gemini could not generate the case."
                )

                st.code(
                    str(e)
                )


# ============================================================
# PATIENT CASE
# ============================================================

elif page == "🩺 Patient Case":

    st.title("🩺 Patient Case")

    st.info(
        "This is a fictional educational clinical pharmacy simulation."
    )


    condition = st.text_input(
        "Choose a condition",
        placeholder="Example: hypertension, asthma, diabetes"
    )


    if st.button("🩺 GENERATE CASE"):

        api_key = os.environ.get(
            "GEMINI_API_KEY"
        )


        if not api_key:

            st.error(
                "Gemini API key is not connected."
            )

        else:

            try:

                from google import genai

                client = genai.Client(
                    api_key=api_key
                )


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


                with st.spinner(
                    "🩺 Preparing the patient..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )


                st.markdown(
                    "### 🧑‍⚕️ PATIENT FILE"
                )

                st.write(
                    response.text
                )


            except Exception as e:

                st.error(
                    "Gemini error"
                )

                st.code(
                    str(e)
                )


# ============================================================
# AI PATIENT
# ============================================================

elif page == "🗣️ AI Patient":

    st.title("🗣️ AI Patient")

    st.write(
        "Practice your pharmacy counselling communication."
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
        "What would you say to the patient?"
    )


    if st.button("💬 TALK TO PATIENT"):

        api_key = os.environ.get(
            "GEMINI_API_KEY"
        )


        if not api_key:

            st.error(
                "Gemini API key is not connected."
            )


        elif not message:

            st.warning(
                "Enter something to say to the patient."
            )


        else:

            try:

                from google import genai

                client = genai.Client(
                    api_key=api_key
                )


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


                with st.spinner(
                    "🗣️ Patient is responding..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )


                st.markdown(
                    "### 🧑 PATIENT"
                )

                st.write(
                    response.text
                )


            except Exception as e:

                st.error(
                    "Gemini error"
                )

                st.code(
                    str(e)
                )


# ============================================================
# AI QUIZ
# ============================================================

elif page == "❓ AI Quiz":

    st.title("❓ AI Pharmacy Quiz")

    st.write(
        "Create a personalized pharmacy challenge."
    )


    topic = st.text_input(
        "Quiz topic",
        placeholder="Example: pharmacology of autonomic nervous system"
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

        api_key = os.environ.get(
            "GEMINI_API_KEY"
        )


        if not api_key:

            st.error(
                "Gemini API key is not connected."
            )


        else:

            try:

                from google import genai

                client = genai.Client(
                    api_key=api_key
                )


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
"""


                with st.spinner(
                    "🧠 Building your quiz..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )


                st.markdown(
                    "### 📚 YOUR CHALLENGE"
                )

                st.write(
                    response.text
                )


            except Exception as e:

                st.error(
                    "Gemini error"
                )

                st.code(
                    str(e)
                )


# ============================================================
# OTHER MISSIONS
# ============================================================

else:

    st.title(page)

    st.markdown("""
    <div style="
        padding:35px;
        margin-top:20px;
        border-radius:25px;
        background:white;
        border:1px solid #e2e8f0;
        box-shadow:0 15px 35px rgba(15,23,42,0.07);
        text-align:center;
    ">

        <div style="
            font-size:55px;
        ">
            🚀
        </div>

        <div style="
            margin-top:12px;
            font-size:26px;
            font-weight:950;
            color:#172554;
        ">
            Mission Loading
        </div>

        <div style="
            margin-top:8px;
            color:#64748b;
            font-size:14px;
        ">
            This mission is part of the PharmaQuest roadmap.
            More game mechanics are coming soon.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.progress(0.35)

    st.caption(
        "🚀 PharmaQuest is under active development."
    )
