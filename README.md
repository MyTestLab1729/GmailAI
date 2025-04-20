# GmailAI
![GmailAILogo](https://raw.githubusercontent.com/tempgit6969/GmailAILogo/main/WhatsApp%20Image%202025-04-20%20at%2018.08.10_67815e29.jpg)
---

# 📩 GmailAI Auto-Responder

This project is a **Python-based Gmail Auto-Responder** powered by **Google's Gemini AI**.  
It automatically **fetches unread emails** from your Gmail inbox, **generates smart replies** using Gemini, and **sends beautiful HTML email responses** — all with dark mode support! 🌙✨

---

## 🚀 Features
- Automatically fetch unread emails from Gmail.
- Understand and extract the sender name and email body.
- Generate a professional reply using **Google Gemini 2.0 Flash** API.
- Send a colorful, modern HTML email with **dark mode compatibility**.
- Only responds to **Gmail senders** (`@gmail.com`) for better security.
- Runs continuously in a loop (every 10 seconds).
  
---

## 🛠 Setup Instructions

### 1. Clone or Upload the Code
Upload the Python file to your server or clone your project repo.

### 2. Create and Activate Virtual Environment (optional but recommended)
```bash
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Python Libraries
```bash
pip install beautifulsoup4 google-generativeai
```

### 4. Prepare Your Credentials
Create a `.env` file (or directly inside the code, set):
- Your **Gmail address** (EMAIL)
- Your **Gmail App Password** (APP_PASSWORD)
- Your **Gemini API Key** (GEMINI_API_KEY)

> 🔥 Note: Never use your normal Gmail password! Generate a secure **App Password** from your Google Account.

### 5. Update the Config
Edit these lines in the script:
```python
EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-app-password"
GEMINI_API_KEY = "your-gemini-api-key"
```

### 6. Configure EC2 Security Group (if hosting on AWS)
- Open **Port 22** for SSH access (your IP only).
- No need to open **Port 443**.
- Outbound ports must allow **465 or 587** (for SMTP Gmail).

---

## 🔥 How It Works

1. Connects to Gmail via IMAP.
2. Fetches unread emails.
3. Extracts sender name and email body.
4. Uses Gemini AI to generate a reply.
5. Sends a beautifully styled HTML email back to the sender.

---

## 📸 Email Template Preview

- Gradient Header with Logo
- Responsive Body with Professional Font
- Dark Mode Support
- Call-to-Action Button
- Social Media Icons in Footer

> ✅ Looks clean and professional in **Gmail Web**, **Mobile App**, and **Dark Mode**.

---

## 🧹 Future Improvements
- Add logging instead of print statements.
- Add support for attachments.
- Admin dashboard to monitor replies.

---

## ⚡ Quick Start
After setting up everything, simply run:

```bash
python3 your_script_name.py
```
And your bot will check for new emails **every 10 seconds**!

---

## ⚠️ Important Notes
- Google may block IMAP by default. **Enable IMAP** and **Allow Less Secure Apps** (or use OAuth 2.0 for production).
- EC2 default blocks outbound SMTP on port 25 — **use port 465 or 587** through Gmail SMTP.
- Be mindful of API rate limits with Google Generative AI.

---

## 📬 Contact
If you face any issues or want to collaborate:  
**Email**: atrajit.sarkar@iitdalumni.com  
**GitHub**: [atrajit-sarkar](https://github.com/atrajit-sarkar)

---

Would you also like me to create a sample **`.env` file** and **requirements.txt** file too? 🚀  
It will make your project look even more professional!  📂✨
