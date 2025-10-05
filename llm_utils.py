import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in your environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

def classify_message(message: str) -> str:
    prompt = (
        "You are an AI assistant tasked with classifying messages as scam or not scam.\n"
        f"Message: '{message}'\n"
        "Respond with only 'scam', 'not scam', or 'uncertain'."
    )

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")  # <-- correct model name
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        result_text = response.text.strip().lower()
        if 'scam' in result_text and 'not' not in result_text:
            return 'scam'
        elif 'not scam' in result_text or 'not' in result_text:
            return 'not scam'
        else:
            return 'uncertain'
    except Exception as e:
        if "429" in str(e):
            print("Quota exceeded. Waiting 60 seconds before retrying...")
            time.sleep(60)
            return classify_message(message)
        print(f"API call failed: {e}")
        return "uncertain"

def extract_scam_type(message: str) -> str:
    prompt = (
        "You are an AI assistant. Identify the type of scam in the following message.\n"
        f"Message: '{message}'\n"
        "Possible scam types: phishing, otp fraud, fake reward, fake authority, unknown.\n"
        "Respond with only the scam type."
    )
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        scam_type = response.text.strip().lower()
        valid_types = {"phishing", "otp fraud", "fake reward", "fake authority", "unknown"}
        for vt in valid_types:
            if vt in scam_type:
                return vt
        return "unknown"
    except Exception as e:
        print(f"API call failed (scam type): {e}")
        return "unknown"

def generate_explanation(message: str) -> str:
    prompt = (
        "You are an AI assistant explaining scam classifications.\n"
        f"Message: '{message}'\n"
        "Explain in 1-2 sentences why this message is a scam or not scam."
    )
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt, generation_config={"temperature": 0.0})
        explanation = response.text.strip()
        return explanation
    except Exception as e:
        print(f"API call failed (explanation): {e}")
        return "No explanation available."

if __name__ == "__main__":
    print("Available models:")
    for m in genai.list_models():
        print(m.name)
        print(m.name)
