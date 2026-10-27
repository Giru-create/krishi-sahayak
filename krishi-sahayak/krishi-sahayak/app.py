import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Krishi Sahayak",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 Krishi Sahayak")
st.write("An accessible AI assistant for smallholder farmers.")

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("Add your GEMINI_API_KEY in a .env file or Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are Krishi Sahayak, an accessible agricultural assistant for smallholder farmers in India.

Rules:
- Use very simple English.
- Use short sentences.
- Give practical and safe general guidance.
- Always advise the farmer to confirm fertilizer, pesticide, or serious disease decisions with a local agriculture officer.
- If the question is unclear, ask one short clarifying question.
- Format the answer as:
Possible cause:
What to check now:
Next steps:
"""

question = st.text_area(
    "Ask your farming question",
    placeholder="Example: My tomato leaves are turning yellow. What should I do?"
)

if st.button("Get advice"):
    if question.strip() == "":
        st.warning("Please type a question first.")
    else:
        with st.spinner("Krishi Sahayak is thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    {"role": "user", "parts": [
                        {"text": SYSTEM_PROMPT},
                        {"text": question}
                    ]}
                ]
            )
            answer = response.text
            st.session_state["answer"] = answer

if "answer" in st.session_state:
    st.subheader("Advice")
    st.write(st.session_state["answer"])