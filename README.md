# 🌱 Krishi Sahayak — Accessible Farm Assistant

Krishi Sahayak is an accessible AI-powered assistant for smallholder farmers.  
It helps farmers ask crop-related questions and receive simple, practical guidance.

## ✨ Features

- Ask farming questions in simple English
- Get structured advice: possible cause, checks, and next steps
- Upload a crop photo for preliminary visual guidance
- Listen to the AI response using text-to-speech
- Beginner-friendly Streamlit interface

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini / Gemma API
- Web Speech API
- Git and GitHub

## 🚀 How to Run Locally

1. Clone this repository:

```bash
git clone [https://github.com/YOUR_USERNAME/krishi-sahayak.git](https://github.com/YOUR_USERNAME/krishi-sahayak.git)
cd krishi-sahayak
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

4. Run the app:

```bash
streamlit run app.py
```

## ⚠️ Disclaimer

Krishi Sahayak provides general agricultural guidance only.  
For fertilizer doses, pesticide use, or serious crop disease, consult a local agriculture officer or expert.

## 📌 Future Improvements

- Hindi and regional language support
- Offline FAQ mode
- Crop-calendar reminders
- Better image-based disease suggestions
- Expert-reviewed advisory content