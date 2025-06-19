import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini once
genai.configure(api_key=GEMINI_API_KEY)

# Load Bengali bullying word list from external file
with open("bengali_bully_words.txt", "r", encoding="utf-8") as file:
    bengali_bully_words = [line.strip() for line in file if line.strip()]

# Bengali polite words (expand if needed)
bengali_polite_words = [
    "অনুগ্রহ করে", "দয়া করে", "আপনি", "ধন্যবাদ", "শুভেচ্ছা", "মন্তব্য", 
    "আজ্ঞে", "ক্ষমা করবেন", "ভালোবাসা", "নমস্কার", "আপনার", "প্রিয়", "সামাজিক", "ভদ্র"
]

# Scoring logic using Gemini
def get_call_score_and_reason(prompt_text):
    model = genai.GenerativeModel('gemini-1.5-flash')

    scoring_prompt = f"""
    Analyze the following Bengali call transcript and assign a score from 0 to 5 based on these rules:

    1. **Politeness (+2)**:
       - Phrases like "অনুগ্রহ করে", "আপনি", "দয়া করে", "আজ্ঞে", "আসসালামু আলাইকুম", "ওয়ালাইকুম আসসালাম" "ওয়া আলাইকুমুস সালাম" etc. = +2.

    2. **Gratitude (+1)**:
       - Saying "ধন্যবাদ", "শুভেচ্ছা", "ওয়েলকাম", or similar = +1.

    3. **Bullying / Aggression (−2)**:
       - If there's insulting, threatening, mocking, or harsh words I hope you know bengali bully words (like "মূর্খ", "জঞ্জাল", "কুলাঙ্গার", etc.) = −2.

    4. **Negative Tone (−1)**:
       - Slightly rude, dismissive, sarcastic, or disrespectful = −1.

    Rules:
    - Final score must be **between 0 and 5**.
    - Combine the above effects. If both polite and aggressive words exist, adjust accordingly.
    - Consider tone and word usage together, not just word presence.

    Return only:
    - **Score** (e.g., 4)
    - **Reason in Bengali** explaining the score in 1-2 sentences.

    Transcript:
    {prompt_text}
    """

    response = model.generate_content(scoring_prompt)
    return response.text
