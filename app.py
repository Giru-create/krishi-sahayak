import os
import base64
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from google import genai


load_dotenv()


st.set_page_config(
    page_title="Krishi Sahayak",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)


# API key: local .env or Streamlit Cloud secrets
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Gemini API key is missing. Add it to .env locally or Streamlit secrets when deployed.")
    st.stop()

client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
You are Krishi Sahayak, a practical agricultural assistant for smallholder farmers in India.

Write like a knowledgeable field officer speaking to a farmer.

Rules:
- Use simple, respectful English.
- Use short sentences.
- Be practical and cautious.
- Format the response using these headings:
What may be happening
Check this first
What to do now
When to seek expert help
- Do not give a confirmed disease diagnosis.
- Do not recommend exact pesticide or fertilizer doses.
- For chemical use, serious disease, or uncertain symptoms, tell the farmer to contact a local agriculture officer.
- If the question is unclear, ask one short clarifying question.
"""


# Theme CSS
st.html("""
<style>
    .stApp {
        background-color: #faf9f6;
        color: #222222;
    }

    .block-container {
        padding-top: 3.2rem;
        padding-bottom: 4rem;
        max-width: 720px;
    }

    h1, h2, h3 {
        font-family: Georgia, 'Times New Roman', serif;
        color: #1f2a24;
        letter-spacing: -0.02em;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: #1f4d36;
        color: #f4f1ea;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    .brand-name {
        font-family: Georgia, serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #1f2a24;
    }

    .page-title {
        font-family: Georgia, serif;
        font-size: 2.15rem;
        font-weight: 700;
        color: #17211c;
        line-height: 1.15;
        margin: 18px 0 10px 0;
    }

    .page-subtitle {
        font-size: 1.02rem;
        color: #55605a;
        max-width: 560px;
        line-height: 1.55;
        margin-bottom: 28px;
    }

    .input-panel {
        background: #ffffff;
        border: 1px solid #e3e0d8;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 1px 3px rgba(31, 42, 36, 0.06);
    }

    .field-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #6b7269;
        margin-bottom: 8px;
    }

    .advice-panel {
        background: #ffffff;
        border: 1px solid #e3e0d8;
        border-top: 4px solid #1f4d36;
        border-radius: 10px;
        padding: 26px;
        margin-top: 26px;
    }

    .advice-heading {
        font-family: Georgia, serif;
        font-size: 1.35rem;
        color: #17211c;
        margin: 0 0 12px 0;
    }

    .advice-note {
        font-size: 0.86rem;
        color: #6b7269;
        margin-top: 14px;
    }

    .site-footer {
        margin-top: 52px;
        padding-top: 18px;
        border-top: 1px solid #e3e0d8;
        color: #6b7269;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
    }

    div[data-testid="stButton"] button {
        background-color: #1f4d36;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.55rem 1.1rem;
    }

    div[data-testid="stButton"] button:hover {
        background-color: #173b29;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 8px;
        border-color: #d8d4ca;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 8px;
    }
</style>
""")


# Header
st.html("""
<div class="brand-row">
    <div class="brand-mark">🌿</div>
    <div class="brand-name">Krishi Sahayak</div>
</div>

<h1 class="page-title">
    Get practical guidance for your crop problem
</h1>

<p class="page-subtitle">
    Describe what you are seeing in your field. Add a photo if possible. Krishi Sahayak gives simple next steps and tells you when to contact a local agriculture officer.
</p>
""")


# Sidebar
with st.sidebar:
    st.header("Before you ask")
    st.markdown(
        """
        Include useful details:

        - Crop name  
        - What part of the plant is affected  
        - When the problem started  
        - Watering routine  
        - Recent weather or fertilizer use  

        **Example:**  
        “Tomato plant. Lower leaves are turning yellow. Soil remains wet. Started three days ago.”
        """
    )

    st.divider()
    st.caption(
        "Krishi Sahayak provides general guidance. "
        "It does not replace advice from a local agriculture officer."
    )


# Input section
st.html("""
<div class="input-panel">
    <div class="field-label">Describe the problem</div>
</div>
""")

question = st.text_area(
    "Describe the problem",
    height=130,
    placeholder="Example: Tomato plant. Lower leaves are turning yellow. Soil remains wet.",
    label_visibility="collapsed"
)

uploaded_image = st.file_uploader(
    "Add a crop photo",
    type=["jpg", "jpeg", "png"],
    help="A clear photo of the affected leaves or plant helps the assistant understand the symptoms."
)

if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="Photo added",
        width=300
    )

submit_col, note_col = st.columns([1, 2])

with submit_col:
    get_advice = st.button("Get guidance", use_container_width=True)

with note_col:
    st.caption("You can ask with text only, photo only, or both.")


# Example prompts
st.markdown("#### Not sure what to write?")

example_1, example_2, example_3 = st.columns(3)

with example_1:
    if st.button("Yellow tomato leaves", use_container_width=True):
        st.session_state["question"] = "Tomato plant. Lower leaves are turning yellow. Soil remains wet."
        st.rerun()

with example_2:
    if st.button("Spots on wheat leaves", use_container_width=True):
        st.session_state["question"] = "Wheat crop. Leaves have small yellow-brown spots."
        st.rerun()

with example_3:
    if st.button("Watering brinjal", use_container_width=True):
        st.session_state["question"] = "How often should I water brinjal plants in hot weather?"
        st.rerun()


if "question" in st.session_state and not question:
    question = st.session_state["question"]


# Generate guidance
if get_advice:
    if question.strip() == "" and uploaded_image is None:
        st.warning("Please describe the problem or add a crop photo.")
    else:
        with st.spinner("Preparing guidance..."):
            try:
                prompt = SYSTEM_PROMPT + "\n\nFarmer's description:\n" + question

                if uploaded_image is not None:
                    image_bytes = uploaded_image.getvalue()
                    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                    prompt += """

A crop photo is attached.
Describe only visible symptoms.
Do not give a confirmed diagnosis.
"""

                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=[
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "data": image_base64,
                                "mime_type": uploaded_image.type
                            }
                        ]
                    )
                else:
                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=prompt
                    )

                answer = response.output_text
                st.session_state["answer"] = answer

                st.html("""
                <div class="advice-panel">
                    <h2 class="advice-heading">Guidance</h2>
                </div>
                """)

                st.markdown(answer)

                st.caption(
                    "This is general guidance, not a confirmed diagnosis. "
                    "For pesticide, fertilizer, or serious crop-health decisions, consult a local agriculture officer."
                )

                # Voice button
                safe_answer = answer.replace("`", "'").replace("${", "$ {")

                voice_html = f"""
                <button
                    onclick="speakAdvice()"
                    style="
                        padding: 10px 16px;
                        border: 1px solid #1f4d36;
                        border-radius: 8px;
                        background: #ffffff;
                        color: #1f4d36;
                        font-size: 14px;
                        font-weight: 600;
                        cursor: pointer;
                    "
                >
                    Listen to this guidance
                </button>


                <script>
                function speakAdvice() {{
                    const text = `{safe_answer}`;
                    const speech = new SpeechSynthesisUtterance(text);
                    speech.lang = "en-IN";
                    speech.rate = 0.95;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(speech);
                }}
                </script>
                """

                components.html(
                    voice_html,
                    height=80,
                    scrolling=False
                )

                st.download_button(
                    label="Download guidance",
                    data=answer,
                    file_name="krishi-sahayak-guidance.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("Krishi Sahayak could not prepare guidance right now. Please try again.")
                st.caption(f"Technical details: {e}")


# Footer
st.html("""
<div class="site-footer">
    <span>Krishi Sahayak</span>
    <span>Built by Grish Kumar</span>
</div>
""")