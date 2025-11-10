import re
import random
import string
import smtplib
import time
from email.mime.text import MIMEText
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# --- SAMPLE ORGANIZATIONAL DATA ---
HR_DOCS = {
    "leave": "Employees can take 12 paid leaves per year and must apply 2 days in advance.",
    "salary": "Salaries are credited on the last working day of every month.",
    "policy": "Employees must follow the IT security policy and maintain confidentiality.",
}
IT_DOCS = {
    "password": "To reset your password, visit the IT portal and click 'Forgot Password'.",
    "email": "For email setup, contact the IT helpdesk at it.support@company.com.",
}
ORG_EVENTS = {
    "event": "Annual Day is celebrated in December every year with cultural events and awards.",
}

# Combine all text into a corpus for search
CORPUS = []
for category in (HR_DOCS, IT_DOCS, ORG_EVENTS):
    for k, v in category.items():
        CORPUS.append(v)

# --- PROFANITY FILTER ---
BAD_WORDS = ["badword", "stupid", "idiot"]

def clean_text(text):
    """Remove punctuation and lowercase text."""
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    return text

def mask_profanity(text):
    """Replace bad words with asterisks."""
    for w in BAD_WORDS:
        pattern = re.compile(rf"\\b{w}\\b", re.IGNORECASE)
        text = pattern.sub(w[0] + "*" * (len(w) - 1), text)
    return text

# --- SIMPLE NLP SEARCH ENGINE ---
def get_best_answer(query):
    """Return best matching sentence using TF-IDF similarity."""
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    vectors = vectorizer.fit_transform([query] + CORPUS)
    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    best_idx = scores.argmax()
    return CORPUS[best_idx]

# --- DOCUMENT PROCESSING ---
def extract_text_from_file(file_path):
    """Extract text from a simple .txt file (for demo)."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "Error reading document."

def summarize_text(text, max_sentences=2):
    """Simple summarization by taking first few lines."""
    lines = text.split(".")
    summary = ". ".join(lines[:max_sentences]) + "."
    return summary

# --- 2FA (EMAIL OTP) ---
OTP_STORE = {}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[email] = (otp, time.time())
    # Try to send email (use Gmail SMTP for demo)
    try:
        sender = "your_email@gmail.com"
        password = "your_app_password"
        msg = MIMEText(f"Your OTP is {otp}. It is valid for 5 minutes.")
        msg["Subject"] = "Your 2FA OTP"
        msg["From"] = sender
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"OTP sent to {email}")
    except Exception:
        print(f"[Demo Mode] OTP for {email}: {otp}")
    return otp

def verify_otp(email, entered_otp):
    if email in OTP_STORE:
        otp, created = OTP_STORE[email]
        if time.time() - created > 300:
            print("OTP expired.")
            return False
        return entered_otp == otp
    return False

# --- MAIN CHAT LOOP ---
def start_chat():
    print(\"\\n=== Intelligent Enterprise Assistant ===\")
    email = input(\"Enter your email for verification: \")
    otp = send_otp(email)
    entered = input(\"Enter the OTP sent to your email: \")
    if not verify_otp(email, entered):
        print(\"Invalid OTP. Exiting.\")
        return

    print(\"\\n✅ Verification Successful. You can now chat with the Assistant!\")
    print(\"Type 'exit' to quit.\\n\")

    while True:
        query = input(\"You: \")
        if query.lower() == "exit":
            print(\"Goodbye!\")
            break
        query = mask_profanity(query)
        if "upload" in query or "document" in query:
            path = input(\"Enter path of .txt document to process: \")
            content = extract_text_from_file(path)
            print(\"Summary:\", summarize_text(content))
            continue
        answer = get_best_answer(clean_text(query))
        print(\"Bot:\", answer)

# Run chatbot
if __name__ == \"__main__\":
    start_chat()
