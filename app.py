import streamlit as st
import datetime
import time

# ==========================================
# PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Momenta | Backed by Brain Science",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Native Dark Mode with Lavender & Sage Accents
st.markdown("""
<style>
    /* Color Palette Variables - DARK MODE */
    :root {
        --sage-green: #7BB08A; /* Brighter sage for dark bg */
        --lavender: #B5A1D9;   /* Brighter lavender for dark bg */
        --text-main: #FFFFFF;
        --text-muted: #CBD5E1;
        --bg-card: #1E293B;    /* Slate-800 for cards/boxes */
    }
    
    /* Text Colors */
    p, li, span, div.stMarkdown {
        color: var(--text-main) !important;
    }
    
    /* Gradient Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-main) !important;
        font-weight: 800 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        letter-spacing: -0.02em;
    }
    
    .gradient-text {
        background: -webkit-linear-gradient(45deg, var(--sage-green), var(--lavender));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Catchphrase */
    .catchphrase {
        font-size: 1.4rem;
        color: var(--text-muted) !important; 
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* All Buttons (Login, Submit, etc.) */
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, var(--sage-green), var(--lavender)) !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    /* Force button text to be white ALWAYS */
    div.stButton > button *, div[data-testid="stFormSubmitButton"] > button * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.5) !important;
        transform: translateY(-1px) !important;
        opacity: 0.90 !important;
    }
    
    /* Text Inputs & Text Areas - Dark theme with Sage border */
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="base-input"] > input,
    div[data-baseweb="textarea"] > textarea,
    div[data-baseweb="select"] > div {
        background-color: #0F172A !important; /* Very dark slate */
        color: var(--text-main) !important;
        border: 1px solid var(--sage-green) !important;
        border-radius: 6px;
    }
    
    /* Placeholder text inside inputs */
    input::placeholder, textarea::placeholder {
        color: #64748B !important;
    }
    
    /* Expander/Cards */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        color: var(--text-main) !important;
        border-radius: 8px;
        border: 1px solid #334155;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: 1px solid #334155 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        color: var(--text-muted) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--sage-green), var(--lavender)) !important;
        border: none !important;
    }
    /* Active tab text color */
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Custom Info Box */
    .info-box {
        background-color: var(--bg-card);
        padding: 25px;
        border-radius: 12px;
        border-top: 5px solid var(--lavender);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        color: var(--text-main);
    }
    .info-box h3 {
        color: var(--text-main) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'users' not in st.session_state:
    st.session_state.users = {'demo_mom': 'password123'} # Pre-loaded demo account
if 'family_members' not in st.session_state:
    st.session_state.family_members = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'journals' not in st.session_state:
    st.session_state.journals = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'community_posts' not in st.session_state:
    # Seeded with some fake data for the networking tab
    st.session_state.community_posts = [
        {"user": "Sarah J.", "time": "2 hours ago", "content": "Just finished a 5-minute breathing exercise in the car before picking up the kids. Small wins! 🌿"},
        {"user": "Elena M.", "time": "5 hours ago", "content": "The new Wordle completely stumped me today. Still, a good brain workout. Anyone else struggling?"}
    ]

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success("Successfully logged in!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Invalid username or password.")

def signup(username, password):
    if username in st.session_state.users:
        st.error("Username already exists. Please choose another.")
    elif len(username) < 3 or len(password) < 6:
        st.error("Username must be at least 3 characters and password at least 6 characters.")
    else:
        st.session_state.users[username] = password
        st.success("Account created! Please log in.")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

def simple_cbt_bot(user_message):
    """A simulated CBT bot that responds based on keywords."""
    msg = user_message.lower()
    if any(word in msg for word in ["stress", "overwhelm", "too much", "busy"]):
        return "It sounds like you're carrying a heavy load right now. In CBT, we look at how to break large stressors into smaller, manageable pieces. What is ONE small thing you can control right now?"
    elif any(word in msg for word in ["tired", "exhausted", "sleep"]):
        return "Being a working mom is incredibly demanding on your nervous system. Your brain needs rest to form new neural pathways (neuroplasticity). Can you find a 10-minute window for yourself today just to breathe?"
    elif any(word in msg for word in ["kid", "child", "husband", "family"]):
        return "Family dynamics can trigger automatic negative thoughts. Let's reframe: Instead of thinking 'I have to do everything perfectly,' try 'I am doing my best, and good enough is perfectly fine.' How does that feel?"
    elif any(word in msg for word in ["sad", "depressed", "down"]):
        return "I hear you. It's completely valid to feel that way. What is a small, healthy habit that usually brings you a tiny bit of joy? A hot cup of tea? A short walk?"
    else:
        return "Thank you for sharing that with me. What specific thought crossed your mind just before you started feeling this way?"

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================

st.markdown("<h1 style='text-align: center; font-size: 4rem;'>Your mind deserves <span class='gradient-text'>a moment</span></h1>", unsafe_allow_html=True)
st.markdown("""
    <p class='catchphrase'>
        Built for busy moms. Backed by brain science.<br>
        <span style='font-size: 1.1rem; color: #94A3B8;'>Momenta helps you manage stress, build healthy habits, and nurture your family.</span>
    </p>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # ------------------------------------------
    # HOME PAGE (Logged Out)
    # ------------------------------------------
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>The Science of Neuroplasticity</h3>
            <p><strong>Neuroplasticity</strong> is your brain's incredible ability to reorganize itself by forming new neural connections throughout life. For busy, working moms, the constant juggle can lead to chronic stress, which physically changes the brain and makes us more reactive.</p>
            <p>At <strong>Momenta</strong>, we use cognitive principles to help you:</p>
            <ul>
                <li><strong>Rewire Stress Responses:</strong> Shift from a state of 'fight or flight' to calm and controlled.</li>
                <li><strong>Build Healthy Habits:</strong> Small, consistent actions create strong, positive neural pathways.</li>
                <li><strong>Reclaim Cognitive Bandwidth:</strong> Offload the mental burden of family management into organized systems.</li>
            </ul>
            <p><em>Join a community of mothers actively reshaping their minds and lives.</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Placeholder for an inviting image
        st.markdown("<div style='text-align:center; font-size: 5rem;'>🌱 🧠 🧘‍♀️</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Get Started")
        tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])
        
        with tab_login:
            with st.form("login_form"):
                log_user = st.text_input("Username", placeholder="e.g. demo_mom")
                log_pass = st.text_input("Password", type="password", placeholder="e.g. password123")
                submit_login = st.form_submit_button("Log In")
                if submit_login:
                    login(log_user, log_pass)
                    
        with tab_signup:
            with st.form("signup_form"):
                sign_user = st.text_input("Choose a Username")
                sign_pass = st.text_input("Choose a Password", type="password")
                submit_signup = st.form_submit_button("Sign Up")
                if submit_signup:
                    signup(sign_user, sign_pass)

else:
    # ------------------------------------------
    # DASHBOARD (Logged In)
    # ------------------------------------------
    st.sidebar.markdown(f"### Welcome, {st.session_state.current_user}!")
    if st.sidebar.button("Log Out"):
        logout()
        
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Daily Brain Tip:** Hydration is key for neuroplasticity. Drink a glass of water right now!")

    # Dashboard Tabs
    tab_family, tab_journal, tab_cbt, tab_schedule, tab_games, tab_network = st.tabs([
        "👨‍👩‍👧 Family Manager", 
        "📔 Journaling", 
        "🤖 CBT Chatbot", 
        "📅 Scheduling", 
        "🧩 Brain Games", 
        "🌐 Momenta Network"
    ])

    # --- TAB 1: FAMILY MANAGER ---
    with tab_family:
        st.header("Family Manager & Mental Offloading")
        st.markdown("Offload your mental to-do list here to reduce cognitive overload.")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Add Family Member")
            with st.form("add_member_form"):
                member_name = st.text_input("Name")
                member_desig = st.selectbox("Designation", ["Child", "Spouse", "Self", "Pet", "Other"])
                add_mem = st.form_submit_button("Add Member")
                if add_mem and member_name:
                    st.session_state.family_members.append({"name": member_name, "designation": member_desig})
                    st.rerun()
                    
            st.markdown("**Current Members:**")
            for m in st.session_state.family_members:
                st.markdown(f"- **{m['name']}** ({m['designation']})")

        with col2:
            st.subheader("Assign Tasks")
            if not st.session_state.family_members:
                st.info("Add a family member on the left to start assigning tasks.")
            else:
                with st.form("add_task_form"):
                    task_desc = st.text_input("Task Description (e.g., Pack lunch, Sign permission slip)")
                    assignee = st.selectbox("Assign To", [m['name'] for m in st.session_state.family_members])
                    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "One-time"])
                    add_task = st.form_submit_button("Add Task")
                    if add_task and task_desc:
                        st.session_state.tasks.append({
                            "id": str(time.time()),
                            "desc": task_desc, 
                            "assignee": assignee, 
                            "frequency": frequency,
                            "done": False
                        })
                        st.rerun()
                
                st.markdown("### To-Do List")
                if not st.session_state.tasks:
                    st.write("No tasks assigned yet. You're all caught up!")
                else:
                    for task in st.session_state.tasks:
                        col_chk, col_text, col_tag = st.columns([0.1, 0.7, 0.2])
                        with col_chk:
                            # Use a unique key for each checkbox
                            is_done = st.checkbox("", value=task['done'], key=f"chk_{task['id']}")
                            if is_done != task['done']:
                                task['done'] = is_done
                                # Optional: trigger rerun to strike-through immediately
                        with col_text:
                            if task['done']:
                                st.markdown(f"~~{task['desc']}~~ *(assigned to {task['assignee']})*")
                            else:
                                st.markdown(f"**{task['desc']}** *(assigned to {task['assignee']})*")
                        with col_tag:
                            st.caption(f"[{task['frequency']}]")

    # --- TAB 2: JOURNALING ---
    with tab_journal:
        st.header("Mindful Journaling")
        st.markdown("Writing helps process emotions and promotes structural changes in the brain's emotional centers.")
        
        with st.form("journal_form"):
            journal_entry = st.text_area("How are you feeling today?", height=150, placeholder="Take a deep breath and write...")
            save_journal = st.form_submit_button("Save Entry")
            if save_journal and journal_entry:
                st.session_state.journals.insert(0, {
                    "date": datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p"),
                    "content": journal_entry
                })
                st.success("Journal saved! 🌿")
                
        st.markdown("---")
        st.subheader("Past Entries")
        if not st.session_state.journals:
            st.info("Your journal entries will appear here.")
        else:
            for entry in st.session_state.journals:
                with st.expander(f"📝 {entry['date']}"):
                    st.write(entry['content'])

    # --- TAB 3: CBT CHATBOT ---
    with tab_cbt:
        st.header("CBT Support Chatbot")
        st.markdown("This chatbot uses Cognitive Behavioral Therapy principles to help you reframe stressful thoughts. *(Note: This is a supportive tool, not a replacement for professional therapy).*")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        # Chat Input
        user_input = st.chat_input("Tell me what's on your mind...")
        if user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
                
            # Generate and add bot response
            with st.spinner("Thinking..."):
                time.sleep(1) # Simulate thought process
                bot_response = simple_cbt_bot(user_input)
                
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.write(bot_response)
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # --- TAB 4: SCHEDULING ---
    with tab_schedule:
        st.header("Centralized Scheduling")
        st.markdown("""
        Integrating your family schedule reduces the mental energy spent on planning. 
        Below is a demonstration of an embedded Google Calendar. 
        """)
        
        # Displaying a public Google Calendar as an example via Iframe
        st.components.v1.iframe(
            src="https://calendar.google.com/calendar/embed?src=en.usa%23holiday%40group.v.calendar.google.com&ctz=America%2FNew_York",
            width=800,
            height=600,
            scrolling=True
        )
        
        with st.expander("How to link YOUR Google Calendar"):
            st.markdown("""
            To display your personal or family calendar here:
            1. Open Google Calendar on a computer.
            2. Go to Settings (gear icon) > Settings for my calendars.
            3. Click your calendar, scroll down to "Integrate calendar".
            4. Copy the "Embed code" (it starts with `<iframe src=...`).
            5. In a fully deployed version of this app, you would paste that `src` link into the code!
            """)

    # --- TAB 5: MINI GAMES ---
    with tab_games:
        st.header("Brain Training Games")
        st.markdown("Engaging in novel tasks like puzzles stimulates neurogenesis (the creation of new neurons). Take a 5-minute break!")
        
        game_choice = st.radio("Choose a game to play:", ["Sudoku", "2048 (Logic Puzzle)"], horizontal=True)
        
        if game_choice == "Sudoku":
            st.components.v1.iframe(
                src="https://sudoku.com/",
                width=800,
                height=600,
                scrolling=True
            )
        elif game_choice == "2048 (Logic Puzzle)":
            st.components.v1.iframe(
                src="https://play2048.co/",
                width=800,
                height=600,
                scrolling=True
            )

    # --- TAB 6: NETWORKING FEED ---
    with tab_network:
        st.header("Momenta Network")
        st.markdown("Connect, share, and validate experiences with other busy moms. A strong social support system is scientifically proven to lower cortisol (stress hormone) levels.")
        
        # Post input
        with st.form("post_form"):
            new_post = st.text_area("Share a thought, a win, or a struggle...", placeholder="What's on your mind?")
            submit_post = st.form_submit_button("Post to Community")
            if submit_post and new_post:
                st.session_state.community_posts.insert(0, {
                    "user": st.session_state.current_user,
                    "time": "Just now",
                    "content": new_post
                })
                st.success("Posted!")
                st.rerun()
                
        st.markdown("---")
        
        # Feed Display - Updated for Dark Mode
        for post in st.session_state.community_posts:
            st.markdown(f"""
            <div style="background-color: #1E293B; padding: 15px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 10px;">
                <div style="color: #7BB08A; font-weight: bold; margin-bottom: 5px;">
                    👤 {post['user']} <span style="color: #94A3B8; font-size: 0.8em; font-weight: normal;">• {post['time']}</span>
                </div>
                <div style="color: #FFFFFF; font-size: 1.05em;">
                    {post['content']}
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #94A3B8;">
                    💬 Reply &nbsp;&nbsp; ❤️ Like
                </div>
            </div>
            """, unsafe_allow_html=True)

# import streamlit as st
# import datetime
# import time

# # ==========================================
# # PAGE CONFIGURATION & THEME
# # ==========================================
# st.set_page_config(
#     page_title="Momenta | Backed by Brain Science",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for Sage Green and Lavender Theme
# st.markdown("""
# <style>
#     /* Color Palette Variables */
#     :root {
#         --sage-green: #9CA986;
#         --light-sage: #C2CDB6;
#         --lavender: #E6E6FA;
#         --dark-lavender: #C3B1E1;
#         --text-dark: #2F4F4F;
#         --bg-color: #FAFAFA;
#     }
    
#     /* Backgrounds */
#     .stApp {
#         background-color: var(--bg-color);
#         color: var(--text-dark);
#     }
    
#     /* Headers */
#     h1, h2, h3, h4, h5, h6 {
#         color: var(--sage-green) !important;
#         font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
#     }
    
#     /* Catchphrase */
#     .catchphrase {
#         font-size: 1.6rem;
#         color: var(--dark-lavender);
#         font-style: italic;
#         text-align: center;
#         margin-bottom: 2rem;
#         font-weight: 500;
#     }
    
#     /* Buttons */
#     .stButton>button {
#         background-color: var(--lavender);
#         color: var(--text-dark);
#         border: 2px solid var(--dark-lavender);
#         border-radius: 10px;
#         transition: all 0.3s ease;
#     }
#     .stButton>button:hover {
#         background-color: var(--sage-green);
#         color: white;
#         border-color: var(--sage-green);
#     }
    
#     /* Expander/Cards */
#     .streamlit-expanderHeader {
#         background-color: var(--light-sage);
#         border-radius: 5px;
#     }
    
#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         background-color: var(--lavender);
#         border-radius: 4px 4px 0 0;
#         padding: 10px 20px;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: var(--sage-green);
#         color: white !important;
#     }
    
#     /* Custom Info Box */
#     .info-box {
#         background-color: white;
#         padding: 20px;
#         border-radius: 10px;
#         border-left: 5px solid var(--sage-green);
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#         margin-bottom: 20px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # SESSION STATE INITIALIZATION
# # ==========================================
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'current_user' not in st.session_state:
#     st.session_state.current_user = None
# if 'users' not in st.session_state:
#     st.session_state.users = {'demo_mom': 'password123'} # Pre-loaded demo account
# if 'family_members' not in st.session_state:
#     st.session_state.family_members = []
# if 'tasks' not in st.session_state:
#     st.session_state.tasks = []
# if 'journals' not in st.session_state:
#     st.session_state.journals = []
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'community_posts' not in st.session_state:
#     # Seeded with some fake data for the networking tab
#     st.session_state.community_posts = [
#         {"user": "Sarah J.", "time": "2 hours ago", "content": "Just finished a 5-minute breathing exercise in the car before picking up the kids. Small wins! 🌿"},
#         {"user": "Elena M.", "time": "5 hours ago", "content": "The new Wordle completely stumped me today. Still, a good brain workout. Anyone else struggling?"}
#     ]

# # ==========================================
# # HELPER FUNCTIONS
# # ==========================================
# def login(username, password):
#     if username in st.session_state.users and st.session_state.users[username] == password:
#         st.session_state.logged_in = True
#         st.session_state.current_user = username
#         st.success("Successfully logged in!")
#         time.sleep(1)
#         st.rerun()
#     else:
#         st.error("Invalid username or password.")

# def signup(username, password):
#     if username in st.session_state.users:
#         st.error("Username already exists. Please choose another.")
#     elif len(username) < 3 or len(password) < 6:
#         st.error("Username must be at least 3 characters and password at least 6 characters.")
#     else:
#         st.session_state.users[username] = password
#         st.success("Account created! Please log in.")

# def logout():
#     st.session_state.logged_in = False
#     st.session_state.current_user = None
#     st.rerun()

# def simple_cbt_bot(user_message):
#     """A simulated CBT bot that responds based on keywords."""
#     msg = user_message.lower()
#     if any(word in msg for word in ["stress", "overwhelm", "too much", "busy"]):
#         return "It sounds like you're carrying a heavy load right now. In CBT, we look at how to break large stressors into smaller, manageable pieces. What is ONE small thing you can control right now?"
#     elif any(word in msg for word in ["tired", "exhausted", "sleep"]):
#         return "Being a working mom is incredibly demanding on your nervous system. Your brain needs rest to form new neural pathways (neuroplasticity). Can you find a 10-minute window for yourself today just to breathe?"
#     elif any(word in msg for word in ["kid", "child", "husband", "family"]):
#         return "Family dynamics can trigger automatic negative thoughts. Let's reframe: Instead of thinking 'I have to do everything perfectly,' try 'I am doing my best, and good enough is perfectly fine.' How does that feel?"
#     elif any(word in msg for word in ["sad", "depressed", "down"]):
#         return "I hear you. It's completely valid to feel that way. What is a small, healthy habit that usually brings you a tiny bit of joy? A hot cup of tea? A short walk?"
#     else:
#         return "Thank you for sharing that with me. What specific thought crossed your mind just before you started feeling this way?"

# # ==========================================
# # MAIN APPLICATION LOGIC
# # ==========================================

# st.markdown("<h1 style='text-align: center; font-size: 4rem;'>Momenta</h1>", unsafe_allow_html=True)
# st.markdown("<p class='catchphrase'>Built for busy moms. Backed by brain science.</p>", unsafe_allow_html=True)

# if not st.session_state.logged_in:
#     # ------------------------------------------
#     # HOME PAGE (Logged Out)
#     # ------------------------------------------
    
#     col1, col2 = st.columns([1.5, 1])
    
#     with col1:
#         st.markdown("""
#         <div class="info-box">
#             <h3>The Science of Neuroplasticity</h3>
#             <p><strong>Neuroplasticity</strong> is your brain's incredible ability to reorganize itself by forming new neural connections throughout life. For busy, working moms, the constant juggle can lead to chronic stress, which physically changes the brain and makes us more reactive.</p>
#             <p>At <strong>Momenta</strong>, we use cognitive principles to help you:</p>
#             <ul>
#                 <li><strong>Rewire Stress Responses:</strong> Shift from a state of 'fight or flight' to calm and controlled.</li>
#                 <li><strong>Build Healthy Habits:</strong> Small, consistent actions create strong, positive neural pathways.</li>
#                 <li><strong>Reclaim Cognitive Bandwidth:</strong> Offload the mental burden of family management into organized systems.</li>
#             </ul>
#             <p><em>Join a community of mothers actively reshaping their minds and lives.</em></p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Placeholder for an inviting image (Streamlit handles images natively, but we use an emoji/text here for simplicity)
#         st.markdown("<div style='text-align:center; font-size: 5rem;'>🌱 🧠 🧘‍♀️</div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("### Get Started")
#         tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])
        
#         with tab_login:
#             with st.form("login_form"):
#                 log_user = st.text_input("Username", placeholder="e.g. demo_mom")
#                 log_pass = st.text_input("Password", type="password", placeholder="e.g. password123")
#                 submit_login = st.form_submit_button("Log In")
#                 if submit_login:
#                     login(log_user, log_pass)
                    
#         with tab_signup:
#             with st.form("signup_form"):
#                 sign_user = st.text_input("Choose a Username")
#                 sign_pass = st.text_input("Choose a Password", type="password")
#                 submit_signup = st.form_submit_button("Sign Up")
#                 if submit_signup:
#                     signup(sign_user, sign_pass)

# else:
#     # ------------------------------------------
#     # DASHBOARD (Logged In)
#     # ------------------------------------------
#     st.sidebar.markdown(f"### Welcome, {st.session_state.current_user}!")
#     if st.sidebar.button("Log Out"):
#         logout()
        
#     st.sidebar.markdown("---")
#     st.sidebar.info("💡 **Daily Brain Tip:** Hydration is key for neuroplasticity. Drink a glass of water right now!")

#     # Dashboard Tabs
#     tab_family, tab_journal, tab_cbt, tab_schedule, tab_games, tab_network = st.tabs([
#         "👨‍👩‍👧 Family Manager", 
#         "📔 Journaling", 
#         "🤖 CBT Chatbot", 
#         "📅 Scheduling", 
#         "🧩 Brain Games", 
#         "🌐 Momenta Network"
#     ])

#     # --- TAB 1: FAMILY MANAGER ---
#     with tab_family:
#         st.header("Family Manager & Mental Offloading")
#         st.markdown("Offload your mental to-do list here to reduce cognitive overload.")
        
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             st.subheader("Add Family Member")
#             with st.form("add_member_form"):
#                 member_name = st.text_input("Name")
#                 member_desig = st.selectbox("Designation", ["Child", "Spouse", "Self", "Pet", "Other"])
#                 add_mem = st.form_submit_button("Add Member")
#                 if add_mem and member_name:
#                     st.session_state.family_members.append({"name": member_name, "designation": member_desig})
#                     st.rerun()
                    
#             st.markdown("**Current Members:**")
#             for m in st.session_state.family_members:
#                 st.markdown(f"- **{m['name']}** ({m['designation']})")

#         with col2:
#             st.subheader("Assign Tasks")
#             if not st.session_state.family_members:
#                 st.info("Add a family member on the left to start assigning tasks.")
#             else:
#                 with st.form("add_task_form"):
#                     task_desc = st.text_input("Task Description (e.g., Pack lunch, Sign permission slip)")
#                     assignee = st.selectbox("Assign To", [m['name'] for m in st.session_state.family_members])
#                     frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "One-time"])
#                     add_task = st.form_submit_button("Add Task")
#                     if add_task and task_desc:
#                         st.session_state.tasks.append({
#                             "id": str(time.time()),
#                             "desc": task_desc, 
#                             "assignee": assignee, 
#                             "frequency": frequency,
#                             "done": False
#                         })
#                         st.rerun()
                
#                 st.markdown("### To-Do List")
#                 if not st.session_state.tasks:
#                     st.write("No tasks assigned yet. You're all caught up!")
#                 else:
#                     for task in st.session_state.tasks:
#                         col_chk, col_text, col_tag = st.columns([0.1, 0.7, 0.2])
#                         with col_chk:
#                             # Use a unique key for each checkbox
#                             is_done = st.checkbox("", value=task['done'], key=f"chk_{task['id']}")
#                             if is_done != task['done']:
#                                 task['done'] = is_done
#                                 # Optional: trigger rerun to strike-through immediately
#                         with col_text:
#                             if task['done']:
#                                 st.markdown(f"~~{task['desc']}~~ *(assigned to {task['assignee']})*")
#                             else:
#                                 st.markdown(f"**{task['desc']}** *(assigned to {task['assignee']})*")
#                         with col_tag:
#                             st.caption(f"[{task['frequency']}]")

#     # --- TAB 2: JOURNALING ---
#     with tab_journal:
#         st.header("Mindful Journaling")
#         st.markdown("Writing helps process emotions and promotes structural changes in the brain's emotional centers.")
        
#         with st.form("journal_form"):
#             journal_entry = st.text_area("How are you feeling today?", height=150, placeholder="Take a deep breath and write...")
#             save_journal = st.form_submit_button("Save Entry")
#             if save_journal and journal_entry:
#                 st.session_state.journals.insert(0, {
#                     "date": datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p"),
#                     "content": journal_entry
#                 })
#                 st.success("Journal saved! 🌿")
                
#         st.markdown("---")
#         st.subheader("Past Entries")
#         if not st.session_state.journals:
#             st.info("Your journal entries will appear here.")
#         else:
#             for entry in st.session_state.journals:
#                 with st.expander(f"📝 {entry['date']}"):
#                     st.write(entry['content'])

#     # --- TAB 3: CBT CHATBOT ---
#     with tab_cbt:
#         st.header("CBT Support Chatbot")
#         st.markdown("This chatbot uses Cognitive Behavioral Therapy principles to help you reframe stressful thoughts. *(Note: This is a supportive tool, not a replacement for professional therapy).*")
        
#         # Display chat history
#         for msg in st.session_state.chat_history:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
                
#         # Chat Input
#         user_input = st.chat_input("Tell me what's on your mind...")
#         if user_input:
#             # Add user message
#             st.session_state.chat_history.append({"role": "user", "content": user_input})
#             with st.chat_message("user"):
#                 st.write(user_input)
                
#             # Generate and add bot response
#             with st.spinner("Thinking..."):
#                 time.sleep(1) # Simulate thought process
#                 bot_response = simple_cbt_bot(user_input)
                
#             st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
#             with st.chat_message("assistant"):
#                 st.write(bot_response)
        
#         if st.button("Clear Chat History"):
#             st.session_state.chat_history = []
#             st.rerun()

#     # --- TAB 4: SCHEDULING ---
#     with tab_schedule:
#         st.header("Centralized Scheduling")
#         st.markdown("""
#         Integrating your family schedule reduces the mental energy spent on planning. 
#         Below is a demonstration of an embedded Google Calendar. 
#         """)
        
#         # Displaying a public Google Calendar as an example via Iframe
#         st.components.v1.iframe(
#             src="https://calendar.google.com/calendar/embed?src=en.usa%23holiday%40group.v.calendar.google.com&ctz=America%2FNew_York",
#             width=800,
#             height=600,
#             scrolling=True
#         )
        
#         with st.expander("How to link YOUR Google Calendar"):
#             st.markdown("""
#             To display your personal or family calendar here:
#             1. Open Google Calendar on a computer.
#             2. Go to Settings (gear icon) > Settings for my calendars.
#             3. Click your calendar, scroll down to "Integrate calendar".
#             4. Copy the "Embed code" (it starts with `<iframe src=...`).
#             5. In a fully deployed version of this app, you would paste that `src` link into the code!
#             """)

#     # --- TAB 5: MINI GAMES ---
#     with tab_games:
#         st.header("Brain Training Games")
#         st.markdown("Engaging in novel tasks like puzzles stimulates neurogenesis (the creation of new neurons). Take a 5-minute break!")
        
#         game_choice = st.radio("Choose a game to play:", ["Sudoku", "2048 (Logic Puzzle)"], horizontal=True)
        
#         if game_choice == "Sudoku":
#             st.components.v1.iframe(
#                 src="https://sudoku.com/",
#                 width=800,
#                 height=600,
#                 scrolling=True
#             )
#         elif game_choice == "2048 (Logic Puzzle)":
#             st.components.v1.iframe(
#                 src="https://play2048.co/",
#                 width=800,
#                 height=600,
#                 scrolling=True
#             )

#     # --- TAB 6: NETWORKING FEED ---
#     with tab_network:
#         st.header("Momenta Network")
#         st.markdown("Connect, share, and validate experiences with other busy moms. A strong social support system is scientifically proven to lower cortisol (stress hormone) levels.")
        
#         # Post input
#         with st.form("post_form"):
#             new_post = st.text_area("Share a thought, a win, or a struggle...", placeholder="What's on your mind?")
#             submit_post = st.form_submit_button("Post to Community")
#             if submit_post and new_post:
#                 st.session_state.community_posts.insert(0, {
#                     "user": st.session_state.current_user,
#                     "time": "Just now",
#                     "content": new_post
#                 })
#                 st.success("Posted!")
#                 st.rerun()
                
#         st.markdown("---")
        
#         # Feed Display
#         for post in st.session_state.community_posts:
#             st.markdown(f"""
#             <div style="background-color: white; padding: 15px; border-radius: 8px; border: 1px solid var(--light-sage); margin-bottom: 10px;">
#                 <div style="color: var(--sage-green); font-weight: bold; margin-bottom: 5px;">
#                     👤 {post['user']} <span style="color: gray; font-size: 0.8em; font-weight: normal;">• {post['time']}</span>
#                 </div>
#                 <div style="color: var(--text-dark); font-size: 1.05em;">
#                     {post['content']}
#                 </div>
#                 <div style="margin-top: 10px; font-size: 0.9em; color: gray;">
#                     💬 Reply &nbsp;&nbsp; ❤️ Like
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
