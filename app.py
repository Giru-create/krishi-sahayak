import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

load_dotenv()

st.set_page_config(
    page_title="Krishi Sahayak",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing. Please add it to your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are Krishi Sahayak, a friendly agricultural assistant for smallholder farmers in India.

Rules:
- Use simple, respectful English.
- Use short sentences and practical advice.
- Format the answer using these headings:
Possible cause:
What to check now:
Next steps:
- Never give a confirmed disease diagnosis.
- For fertilizer doses, pesticides, or serious crop problems, advise the farmer to contact a local agriculture officer.
- If the question is unclear, ask one short clarifying question.
"""

# Custom styling
st.html("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 760px;
    }

    .app-header {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 1px solid #c8e6c9;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 24px;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1b5e20;
        margin: 0;
    }

    .app-subtitle {
        color: #33691e;
        font-size: 1rem;
        margin-top: 8px;
    }

    .feature-pill {
        display: inline-block;
        background: #ffffff;
        border: 1px solid #c8e6c9;
        color: #2e7d32;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-top: 12px;
    }

    .advice-card {
        background: #ffffff;
        border: 1px solid #dcedc8;
        border-left: 6px solid #2e7d32;
        border-radius: 14px;
        padding: 22px;
        margin-top: 18px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    .footer-note {
        text-align: center;
        color: #607d8b;
        font-size: 0.85rem;
        margin-top: 40px;
    }
</style>
""")

# Header
st.html("""
<div class="app-header">
    <p class="app-title">🌱 Krishi Sahayak</p>
    <p class="app-subtitle">
        Simple crop guidance for farmers — ask a question, get clear next steps.
    </p>
    <span class="feature-pill">Voice-friendly</span>
    <span class="feature-pill">Simple English</span>
    <span class="feature-pill">Crop photo support coming soon</span>
</div>
""")

# Sidebar
with st.sidebar:
    st.header("How to use")
    st.markdown(
        """
        1. Type your crop problem.  
        2. Add details such as crop name, leaf color, or watering routine.  
        3. Click **Get advice**.  
        4. Follow the safe next steps shown.

        **Example:**  
        “My tomato leaves are turning yellow and the soil stays wet.”
        """
    )

    st.divider()
    st.caption(
        "Krishi Sahayak gives general guidance only. "
        "For pesticides, fertilizer doses, or serious disease, contact a local agriculture officer."
    )

# Main input
st.subheader("Ask about your crop")

question = st.text_area(
    "Describe the problem",
    height=120,
    placeholder="Example: My tomato leaves are turning yellow. I water the plants every day.",
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 2])

with col1:
    get_advice = st.button("Get advice", use_container_width=True)

with col2:
    st.caption("Try to include the crop name and what you have noticed.")

# Example questions
st.caption("Quick examples:")
example_cols = st.columns(3)

examples = [
    "Tomato leaves are turning yellow",
    "Wheat leaves have yellow spots",
    "How often should I water brinjal?"
]

for i, example in enumerate(examples):
    with example_cols[i]:
        if st.button(example, use_container_width=True):
            st.session_state["question"] = example
            st.rerun()

if "question" in st.session_state and not question:
    question = st.session_state["question"]

# AI response
if get_advice:
    if question.strip() == "":
        st.warning("Please describe your crop problem first.")
    else:
        with st.spinner("Checking your question..."):
            try:
                full_prompt = SYSTEM_PROMPT + "\n\nFarmer question:\n" + question

                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=full_prompt
                )

                answer = interaction.output_text

                st.html('<div class="advice-card">')
                st.markdown("### 🌾 Advice for you")
                st.markdown(answer)
                st.html("</div>")

                st.download_button(
                    label="Download advice",
                    data=answer,
                    file_name="krishi-sahayak-advice.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("Sorry, Krishi Sahayak could not get advice right now.")
                st.caption(f"Technical details: {e}")

# Footer
st.html("""
<p class="footer-note">
    Built by Grish Kumar · Krishi Sahayak · AI for accessible agriculture
</p>
""")