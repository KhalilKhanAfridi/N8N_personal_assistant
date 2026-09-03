import streamlit as st
import requests

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Assistant | AI Chat",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

WEBHOOK_URL = "https://khalilkhanafridi.app.n8n.cloud/webhook/59209596-e40b-459c-9c56-ee770cce2a32"

CAPABILITIES = [
    ("❓", "Answer questions", "Get answers on a wide range of topics."),
    ("📅", "Calendar", "Arrange events and meetings for you."),
    ("📧", "Email", "Read, summarize, and reply to your emails."),
    ("✅", "Tasks", "Manage your tasks and to‑do lists."),
    ("📝", "Notes", "Take quick notes on your behalf."),
    ("💰", "Budgeting", "Track your expenses and spending."),
]

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    :root {
        --primary: #4F46E5;
        --primary-dark: #4338CA;
        --bg-soft: #F8F9FC;
        --border: #E5E7EB;
        --text-muted: #6B7280;
    }

    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 900px;}

    /* Header */
    .app-header {
        text-align: center;
        padding: 1.25rem 1rem 1.75rem 1rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
        color: #111827;
    }
    .app-header p {
        color: var(--text-muted);
        font-size: 1.02rem;
        margin: 0;
    }

    /* Capability cards */
    .cap-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.9rem;
        margin-bottom: 0.5rem;
    }
    @media (max-width: 700px) {
        .cap-grid { grid-template-columns: repeat(1, 1fr); }
    }
    .cap-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
    }
    .cap-card .cap-icon {font-size: 1.35rem; margin-bottom: 0.4rem; line-height: 1;}
    .cap-card .cap-title {font-weight: 600; font-size: 0.95rem; color: #111827 !important; margin-bottom: 0.2rem;}
    .cap-card .cap-desc {font-size: 0.83rem; color: #4B5563 !important; line-height: 1.4;}

    /* Section labels */
    .section-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 1.6rem 0 0.75rem 0;
    }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.5rem 0.9rem;
        margin-bottom: 0.6rem;
    }
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] li {
        color: #111827 !important;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 2.5rem 1rem;
        border: 1px dashed var(--border);
        border-radius: 14px;
        color: #4B5563 !important;
        background: var(--bg-soft);
    }
    .empty-state h4 {color: #111827 !important; margin-bottom: 0.4rem;}
    .empty-state p {color: #4B5563 !important;}

    /* Footer */
    .app-footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid var(--border);
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🤝 Personal Assistant")
        st.caption("Your AI-powered automation companion.")
        st.divider()
        st.markdown("**About**")
        st.write(
            "This assistant connects to an automation workflow that can "
            "answer questions, manage your calendar, email, tasks, notes, "
            "and budget — all from one chat."
        )
        st.divider()
        st.markdown("**Session**")
        st.write(f"Messages this session: {len(st.session_state.get('messages', []))}")
        if st.button("🗑️ Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="app-header">
        <h1>🤝 Your Personal Assistant</h1>
        <p>Automate your day-to-day tasks and get intelligent answers through a simple chat interface.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">What I can help with</div>', unsafe_allow_html=True)

    cards_html = "".join(
        f"""
        <div class="cap-card">
            <div class="cap-icon">{icon}</div>
            <div class="cap-title">{title}</div>
            <div class="cap-desc">{desc}</div>
        </div>
        """
        for icon, title, desc in CAPABILITIES
    )
    st.markdown(f'<div class="cap-grid">{cards_html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CHAT
# ─────────────────────────────────────────────────────────────
def render_chat():
    st.markdown('<div class="section-label">💬 Chat</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <h4>Ready when you are</h4>
            <p>Ask a question or give an instruction below to get started.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    user_message = st.chat_input("Type your message...")

    if user_message:
        with st.chat_message("user"):
            st.markdown(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        WEBHOOK_URL,
                        json={"message": user_message},
                        timeout=30,
                    )
                    response.raise_for_status()
                    ai_response = response.json()[0]["output"]
                except requests.exceptions.RequestException:
                    ai_response = None
                    st.error("Something went wrong while reaching the assistant. Please try again.")
                except (KeyError, IndexError, ValueError):
                    ai_response = None
                    st.error("The assistant returned an unexpected response. Please try again.")

            if ai_response:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
def render_footer():
    st.markdown("""
    <div class="app-footer">
        Built with Streamlit • AI-powered automation
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    render_sidebar()
    render_header()
    render_chat()
    render_footer()


if __name__ == "__main__":
    main()